from __future__ import annotations

import json
import logging
import os
from typing import Dict, Type, List, Tuple, Callable, Any

import pydash
from couchdb import ResourceConflict, ServerError
from pydantic import BaseModel, Field

import couchdb
from pydantic_db_backend.backend import BackendBase
from pydantic_db_backend_common.exceptions import NotFound, AlreadyExists, RevisionConflict
from pydantic_db_backend_common.pydantic import BackendModel
from pydantic_db_backend_common.indexes import Index, SortingIndex, AggregationIndex
from pydantic_db_backend.utils import CustomJSONEncoder

log = logging.getLogger(__name__)


class CouchDbBackend(BackendBase):
    # _collections: Dict[Type[BaseModel], str] = {}
    _indexes: Dict[str, List[dict]] = {}
    _connections: Dict[str, CouchDbConnectionModel] = {}

    @classmethod
    def startup(cls, alias: str | None = "default", uri: str | None = None):
        super().startup()
        if uri is None:
            uri = os.environ.get('COUCHDB_URI', "")
            if uri == "":
                raise EnvironmentError("COUCHDB_URI not set.")

        cls._connections[alias] = CouchDbConnectionModel(
            alias=alias,
            uri=uri,
            server=couchdb.Server(uri)
        )

    @classmethod
    def to_db(cls, instance: BackendModel, json_dict: bool | None = True) -> dict:
        document = super().to_db(instance)
        document = pydash.omit(document | {"_id": document['uid'], "_rev": document['revision']}, "uid", "revision")
        return document

    @classmethod
    def from_db(cls, model: Type[BackendModel], document: dict, json_dict: bool | None = True) -> BackendModel:
        document = pydash.omit(
            document | {
                "uid": document['_id'],
                "revision": document['_rev']
            },
            "_id", "_rev"
        )
        return super().from_db(model, document)

    # noinspection PyMethodOverriding
    @classmethod
    def create_index(cls, collection_name: str, index: Index, db: couchdb.Database):
        super().create_index(collection_name, index)

        if index.type == "sorting":
            index: SortingIndex

            i = (collection_name, index.name)
            indexes = db.index()

            # noinspection PyUnboundLocalVariable
            if i not in indexes:
                indexes[i] = index.sorting

        elif index.type == "aggregation":
            index: AggregationIndex
            cls.view_from_aggregation_index(db, collection_name, index)


        else:
            pass

    @classmethod
    def view_from_aggregation_index(cls, db: couchdb.Database, collection_name: str, index: AggregationIndex):
        design_document = index.design_document

        in_db = f"_design/{design_document}" in db
        if not in_db:
            field, func = next(iter(index.spec.items()))
            map_function = f"function (doc) {{ emit(doc.{field}, 1); }}"
            view_name = f"{index.view_name}"
            # reduce_function = f"function(keys, values, rereduce) {{ return sum(values); }}"
            data = {
                "_id": f"_design/{design_document}",
                "views": {
                    view_name: {
                        "map": map_function,
                        "reduce": func
                    }
                },
                "language": "javascript",
                "options": {"partitioned": False}
            }
            logging.info(f"creating view {design_document}/{view_name}")
            db.save(data)

    @classmethod
    def get_db(cls, model: Type[BackendModel]) -> couchdb.Database:
        db_name = cls.collection_name(model)

        with cls.alias() as alias:
            con = cls._connections[alias]

            if db_name in con.server:
                db = con.server[db_name]
            else:
                db = con.server.create(db_name)
            cls.indexes(model, dict(db=db))
        return db

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        db = cls.get_db(model)
        entry = db.get(uid)
        if entry is None:
            raise NotFound(uid)
        return cls.from_db(model, entry)

    @classmethod
    def post_document(cls, model: Type[BackendModel], document: dict) -> Dict:
        db = cls.get_db(model)
        try:
            db.save(pydash.omit(document, "_rev"))
        except ResourceConflict as e:
            raise AlreadyExists(uid=document["_id"])
        return db.get(document['_id'])

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        document = cls.to_db(instance)

        document = cls.post_document(instance.__class__, document)
        return cls.from_db(instance.__class__, document)

    @classmethod
    def put_instance(cls, instance: BackendModel, ignore_revision_conflict: bool = False) -> BackendModel:
        db = cls.get_db(instance.__class__)
        if instance.uid in db:
            document = cls.to_db(instance)
            while True:
                try:
                    id, rev = db.save(document)
                    document['_rev'] = rev
                    return cls.from_db(instance.__class__, document)

                except ResourceConflict as e:
                    new_rev = db.get(instance.uid)['_rev']
                    if ignore_revision_conflict:
                        document['_rev'] = new_rev
                        continue
                    raise RevisionConflict(new_rev)

        else:
            return cls.post_instance(instance)

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        db = cls.get_db(model)
        if uid in db:
            del db[uid]
        else:
            raise NotFound(uid=uid)

    @classmethod
    def find(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 25,
        query_filter: dict = None,
        sort: List = None,
        fields: List[str] = None,
        max_results: bool | None = False,
        func: Callable = None
    ) -> Tuple[List[Any], int] | List[Any]:
        # fix 0 limit, since couchdb does not know this
        limit = 9999999 if limit == 0 else limit

        if query_filter is None:
            query_filter = {}

        # convert to json and back again, to have iso datetime strings
        query_filter = json.loads(json.dumps(query_filter, cls=CustomJSONEncoder))

        db = cls.get_db(model)

        find_dict = {
            "selector": query_filter,
            "skip": skip,
            "limit": limit,
        }

        if fields is not None:
            find_dict |= {
                "fields": fields
            }

        if sort is not None:
            find_dict["sort"] = sort

        try:
            find_result = db.find(find_dict)
        except ServerError as e:

            error_code = pydash.get(e, ["args", 0, 0])

            if error_code == 400:
                # @asc:  not what I expected the system to do. Better would be to modify the
                # index cache and initiate a new get_db... and a loop
                cls.indexes(model, dict(db=db), force_index_creation=True)
                find_result = db.find(find_dict)
            else:
                raise e
        result = [func(x) for x in find_result]
        if max_results:
            max_results = cls.get_max_results(model, query_filter)
            return result, max_results
        else:
            return result

    @classmethod
    def get_uids(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 25,
        query_filter: dict = None,
        sort: List = None,
        max_results: bool | None = False
    ) -> Tuple[List[str], int] | List[str]:
        r = cls.find(
            model=model,
            skip=skip,
            limit=limit,
            query_filter=query_filter,
            sort=sort,
            fields=['_id'],
            max_results=max_results,
            func=lambda x: x['_id']
        )
        r: Tuple[List[str], int] | List[str]
        return r

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict = None,
        sort: List = None,
        max_results: bool = False
    ) -> Tuple[List[BackendModel], int] | List[BackendModel]:
        r = cls.find(
            model=model,
            skip=skip,
            limit=limit,
            query_filter=query_filter,
            sort=sort,
            max_results=max_results,
            func=lambda x: cls.from_db(model, x)
        )
        r: Tuple[List[BackendModel], int] | List[BackendModel]
        return r

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        with cls.alias() as alias:
            server = cls._connections[alias].server
            name = cls.collection_name(model)
            if name in server:
                server.delete(name)

        super().delete_collection(model)

    @classmethod
    def get_max_results(cls, model: Type[BackendModel], query_filter: dict) -> int:
        # atm it only works with one field,
        db = cls.get_db(model)

        field = "_".join(list(query_filter.keys()))
        view_name = f"{field}_sum"
        index = cls.get_index_by_name(model, view_name)

        design_document = f"aggregation_{view_name}/{view_name}"
        for row in db.view(design_document, group=True):
            for k, v in query_filter.items():
                if isinstance(v, dict):
                    k = next(iter(v.keys()))
                    if k == "$eq":
                        v = v[k]
                    else:
                        return 0
                if v == row.key:
                    ret = row.value
                    return ret


class CouchDbConnectionModel(BaseModel):
    alias: str
    uri: str
    server: couchdb.Server
    dbs: Dict[str, couchdb.Database] = Field(default_factory=dict)

    class Config():
        arbitrary_types_allowed = True
