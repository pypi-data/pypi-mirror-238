import re
from abc import ABCMeta
from typing import List, Any

from lesscode.db.ds_helper import DSHelper


def to_camel_case(x):
    """转驼峰法命名"""
    return re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)


def to_upper_camel_case(x):
    """转大驼峰法命名"""
    s = re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)
    return s[0].upper() + s[1:]


def to_lower_camel_case(x):
    """转小驼峰法命名"""
    s = re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)
    return s[0].lower() + s[1:]


def model2dict(model):
    def _2dict(obj):
        _data_dict = dict()
        for k, v in vars(obj).items():
            if not k.startswith("_"):
                _data_dict.update({k: v})
        return _data_dict

    return _2dict(model)


class BaseModel(metaclass=ABCMeta):
    _connect_name = ""
    _route_key = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def count(cls, query: dict):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        total = collection.count_documents(query)
        return total

    @classmethod
    def query_one(cls, query, to_model: bool = False):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        res = collection.find_one(query)
        if to_model and res:
            res = dict2model(res, cls)
        return res

    @classmethod
    def query_page(cls, query: dict, page_num: int = 1, page_size: int = 10,
                   sort_list: List[List[Any]] = None, to_model: bool = False):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        total = collection.count_documents(query)
        res = collection.find(query)
        if sort_list:
            res = res.sort(sort_list)
        res = res.skip((page_num - 1) * page_size).limit(page_size)
        if res and to_model:
            res = [dict2model(_, cls) for _ in res]
        else:
            res = list(res)
        return {"data_count": total, "data_list": res}

    @classmethod
    def query_all(cls, query: dict, sort_list: List[List[Any]] = None, to_model: bool = False):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        res = collection.find(query)
        if sort_list:
            res = res.sort(sort_list)
        if res and to_model:
            res = [dict2model(_, cls) for _ in res]
        else:
            res = list(res)
        return res

    def insert_one(self):
        document = dict()
        for k, v in vars(self).items():
            if not k.startswith("_"):
                document.update({k: v})
        collection = self._get_collection()
        return collection.insert_one(document=document)

    @classmethod
    def insert_many(cls, data: List[dict]):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.insert_many(documents=data)

    @classmethod
    def delete_one(cls, query):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.delete_many(query)

    @classmethod
    def update_one(cls, query, update, upsert=False, **kwargs):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.update_one(filter=query, update=update, upsert=upsert, **kwargs)

    @classmethod
    def update_many(cls, query, update, upsert=False, **kwargs):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.update_many(filter=query, update=update, upsert=upsert, **kwargs)

    @classmethod
    def aggregate(cls, pipeline, **kwargs):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.aggregate(pipeline=pipeline, **kwargs)

    @classmethod
    def bulk_write(cls, data: list, ordered: bool = True, **kwargs):
        pool = DSHelper(cls._connect_name).pool
        database_name, collection_name = cls._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection.bulk_write(requests=data, ordered=ordered, **kwargs)

    def _get_collection(self):
        pool = DSHelper(self._connect_name).pool
        database_name, collection_name = self._route_key.split(".")
        collection = pool[database_name][collection_name]
        return collection


def dict2model(data: dict, model):
    if issubclass(model, BaseModel):
        return model(**data)
    else:
        raise Exception(f"{model.__class__.__name__} is not subclass of BaseModel")
