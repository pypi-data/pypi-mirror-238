import hashlib
import json
import os
import time
from pymongo import MongoClient


class HashClient:
    _db_user = os.environ["HASH_DB_USER"]
    _db_password = os.environ["HASH_DB_PASS"]
    _db_host = os.environ["HASH_DB_HOST"]
    _db_port = os.environ["HASH_DB_PORT"]
    _db_name = os.environ["HASH_DB_NAME"]
    _db_collection = os.environ["HASH_DB_COLLECTION"]

    _client = MongoClient(f"mongodb://{_db_user}:{_db_password}@{_db_host}:{_db_port}/")
    _database = _client[_db_name]
    _collection = _database[_db_collection]

    @staticmethod
    def exist(customer_uuid: str, type: str, obj) -> bool:
        """Check if an item is hashed in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            obj (Any): object to be checked

        Raises:
            ValueError: parameters not valid

        Returns:
            bool: True if the item exist, False if don't
        """
        HashClient._check_customer_and_type(customer_uuid, type)
        HashClient._check_obj(obj)
        id = HashClient._get_hash(customer_uuid, type, obj)
        item = HashClient._collection.find_one(id)
        if item is None:
            return False
        else:
            return True

    @staticmethod
    def exist_many(customer_uuid: str, type: str, objs: list) -> list[bool]:
        """Check if many item are hashed in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            objs (list): list of objects to be checked

        Raises:
            TypeError: objs is not a list
            ValueError: parameters not valid

        Returns:
            list[bool]: True if the item exist, False if it doesn't
        """
        HashClient._check_objs(objs)
        HashClient._check_customer_and_type(customer_uuid, type)
        ids_to_find = []
        for obj in objs:
            HashClient._check_obj(obj)
            id = HashClient._get_hash(customer_uuid, type, obj)
            ids_to_find.append(id)

        items = HashClient._collection.find(filter={"_id": {"$in": ids_to_find}}, projection="_id")
        items = list(items)

        items = [item["_id"] for item in items]
        results = []
        for id_to_find in ids_to_find:
            if id_to_find in items:
                results.append(True)
            else:
                results.append(False)
        return results

    @staticmethod
    def create(customer_uuid: str, type: str, obj) -> str:
        """Create a hashed item in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            obj (Any): object to be checked

        Raises:
            TypeError: obj is None
            ValueError: customer_uuid or type empty strings
            DuplicateKeyError: obj already exist

        Returns:
            str: id stored "{customer_uuid}/{type}/{hash}"
        """
        HashClient._check_customer_and_type(customer_uuid, type)
        HashClient._check_obj(obj)
        id = HashClient._get_hash(customer_uuid, type, obj)
        document = {
            "_id": id,
            "customer_uuid": str(customer_uuid),
            "type": str(type),
            "obj": obj,
            "created_at": int(time.time()),
        }
        return HashClient._collection.insert_one(document).inserted_id

    @staticmethod
    def create_many(customer_uuid: str, type: str, objs: list) -> list[str]:
        """Create many hashed item in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            objs (list): list of objects to be checked

        Raises:
            TypeError: objs is not a list
            ValueError: customer_uuid or type empty strings
            BulkWriteError: any of the items already exist

        Returns:
            list[str]: list of ids stored "{customer_uuid}/{type}/{hash}"
        """
        HashClient._check_objs(objs)
        HashClient._check_customer_and_type(customer_uuid, type)
        objs_to_add = []
        for obj in objs:
            HashClient._check_obj(obj)
            id = HashClient._get_hash(customer_uuid, type, obj)
            objs_to_add.append(
                {
                    "_id": id,
                    "customer_uuid": str(customer_uuid),
                    "type": str(type),
                    "obj": obj,
                    "created_at": int(time.time()),
                }
            )
        return HashClient._collection.insert_many(objs_to_add).inserted_ids

    @staticmethod
    def get_many(filter: dict = {}, date_comparasion: str = "$gt") -> list[dict]:
        """retrive a list of objects filtered from hash collection

        Args:
            filter (dict, optional): filters to be applied Ex: {"created_at": 10, "customer_uuid": "123", "type": "user"}. Defaults to None.
            date_comparasion (str, optional): in case of filtering by created_at the operator to be used $gt, $lt. Defaults to "$gt".

        Returns:
            list[dict]: list with all the items filtered
        """
        if "created_at" in filter:
            filter["created_at"] = {date_comparasion: filter["created_at"]}
        items = HashClient._collection.find(filter=filter)
        return list(items)

    @staticmethod
    def _check_customer_and_type(customer_uuid, type):
        if not customer_uuid or not str(customer_uuid):
            raise ValueError(f"customer_uuid not valid. Value: {customer_uuid}")
        if not type or not str(type):
            raise ValueError(f"type not valid. Value: {type}")

    @staticmethod
    def _check_obj(obj):
        if not obj:
            raise ValueError(f"Obj not valid. {obj}")

    @staticmethod
    def _check_objs(objs):
        if not isinstance(objs, list):
            raise TypeError(f"Objs of type {objs.__class__} is not valid.")

        if not objs:
            raise ValueError(f"objs is an empty list")

    @staticmethod
    def _get_hash(customer_uuid: str, type: str, obj):
        jsonObj = json.dumps(obj)
        hash = hashlib.md5(jsonObj.encode("utf-8")).hexdigest()
        return f"{customer_uuid}/{type}/{hash}"
