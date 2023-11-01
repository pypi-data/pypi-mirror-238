from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import re
from contextvars import ContextVar
from typing import Type, Dict, List, Tuple

import pydash
from dotenv import load_dotenv
from pydantic import BaseModel

from pydantic_db_backend.utils import CustomJSONEncoder
from pydantic_db_backend_common.indexes import Index
from pydantic_db_backend_common.utils import uid, utcnow
from pydantic_db_backend_common.exceptions import IndexNotExisting
from pydantic_db_backend_common.pydantic import BackendModel

log = logging.getLogger(__name__)

backend_context_var = ContextVar("backend_context_var", default=None)
backend_alias_context_var = ContextVar("backend_alias_context_var", default="default")


class Backend(object):
    @staticmethod
    @contextlib.contextmanager
    def provider(backend: Type[BackendBase]):
        token = backend_context_var.set(backend)
        yield backend
        backend_context_var.reset(token)

    @classmethod
    def backend(cls) -> BackendBase:
        return backend_context_var.get()

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        return cls.backend().post_instance(instance)

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        return cls.backend().get_instance(model, uid)

    @classmethod
    def put_instance(
        cls, instance: BackendModel, ignore_revision_conflict: bool = False
    ) -> BackendModel:
        return cls.backend().put_instance(instance, ignore_revision_conflict)

    @classmethod
    def get_uids(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict | None = None,
        sort: List | None = None,
    ) -> Tuple[List[str], int] | List[str]:
        return cls.backend().get_uids(
            model=model, skip=skip, limit=limit, query_filter=query_filter, sort=sort
        )

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict | None = None,
        sort: List | None = None,
        max_results: bool | None = False,
    ) -> Tuple[List[BackendModel], int] | List[BackendModel]:
        return cls.backend().get_instances(
            model=model,
            skip=skip,
            limit=limit,
            query_filter=query_filter,
            sort=sort,
            max_results=max_results,
        )

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        return cls.backend().delete_uid(model=model, uid=uid)

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        return cls.backend().delete_collection(model)


class BackendBase(object):
    _collections: Dict[Type[BaseModel], str] = {}
    _indexes: Dict[Type[BaseModel], list] = {}

    @classmethod
    def startup(cls, alias: str | None = "default"):
        load_dotenv(".env.local")

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        raise NotImplementedError()

    @staticmethod
    @contextlib.contextmanager
    def alias_provider(alias: str):
        token = backend_alias_context_var.set(alias)
        yield
        backend_alias_context_var.reset(token)

    @staticmethod
    @contextlib.contextmanager
    def alias() -> str:
        yield backend_alias_context_var.get()

    @classmethod
    def collection_name(cls, model: Type[BaseModel]) -> str:
        if model not in cls._collections:
            name = (
                re.sub("([A-Z]+)", r"_\1", model.__name__)
                .lower()
                .removeprefix("_")
                .removesuffix("_model")
            )
            cls._collections[model] = name
        return cls._collections[model]

    @classmethod
    def indexes(
        cls,
        model: Type[BaseModel],
        create_index_kwargs: dict | None,
        force_index_creation: bool = False,
    ) -> List[Index]:
        if model not in cls._indexes or force_index_creation:
            indexes = cls.create_indexes(model, create_index_kwargs)
            cls._indexes[model] = indexes
        return cls._indexes[model]

    @classmethod
    def get_index_by_name(cls, model: Type[BaseModel], name: str) -> Index:
        if model not in cls._indexes:
            raise IndexNotExisting(model_name=model.__name__, name=name)
        model_indexes = cls._indexes[model]
        index = next(filter(lambda x: x.name == name, model_indexes), None)
        if index is None:
            raise IndexNotExisting(model_name=model.__name__, name=name)
        return index

    @classmethod
    def create_indexes(
        cls, model: Type[BaseModel], create_index_kwargs: dict | None
    ) -> List[Index]:
        if not hasattr(model, "Config"):
            return True

        if not hasattr(model.Config, "backend_indexes"):
            return True

        indexes = model.Config.backend_indexes
        for index in indexes:
            cls.create_index(cls.collection_name(model), index, **create_index_kwargs)
        return indexes

    @classmethod
    def create_index(cls, collection_name: str, index: Index, **kwargs):
        log.debug(f"[{collection_name}] Creating {index.type} index {index.name}...")

    @classmethod
    def to_db(cls, instance: BackendModel, json_dict: bool | None = True) -> dict:
        instance.updated_time = utcnow()
        return (
            json.loads(instance.model_dump_json())
            if json_dict
            else instance.model_dump()
        )

    @classmethod
    def from_db(
        cls, model: Type[BackendModel], document: dict, json_dict: bool | None = True
    ) -> BackendModel:
        return (
            model.parse_raw(json.dumps(document))
            if json_dict
            else model.parse_obj(document)
        )

    @classmethod
    def put_instance(
        cls, instance: BackendModel, ignore_revision_conflict: bool = False
    ) -> BackendModel:
        raise NotImplementedError

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        raise NotImplementedError

    @classmethod
    def get_uids(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict | None = None,
        sort: List | None = None,
        max_results: bool | None = False,
    ) -> Tuple[List[str], int] | List[str]:
        raise NotImplementedError

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict = None,
        sort: List = None,
        max_results: bool = False,
    ) -> Tuple[List[BackendModel], int] | List[BackendModel]:
        raise NotImplementedError

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        raise NotImplementedError

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        # delete index info , for recreating it on next collection usage
        if model in cls._indexes:
            del cls._indexes[model]

    @classmethod
    def set_revision(cls, document: dict, field="revision"):
        old_rev, old_checksum = cls.get_revision(document).split("-")
        document_data = pydash.omit(document, field, "updated_time")
        checksum = hashlib.md5(
            json.dumps(document_data, cls=CustomJSONEncoder, sort_keys=True).encode(
                "utf8"
            )
        ).hexdigest()
        if checksum != old_checksum:
            revision = f"{str(int(old_rev)+1)}-{checksum}"
            document[field] = revision

    @classmethod
    def get_revision(cls, document: dict) -> str:
        return pydash.default_to(pydash.get(document, "revision", None), "0-0")
