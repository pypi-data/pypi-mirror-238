import os
import uuid
import pymongo
import mongomock
import pytest

os.environ["HASH_DB_USER"] = "user"
os.environ["HASH_DB_PASS"] = "mongo"
os.environ["HASH_DB_HOST"] = "localhost"
os.environ["HASH_DB_PORT"] = "27017"

with mongomock.patch(servers=(("localhost", 27017),)):
    client = pymongo.MongoClient("localhost")
    from .main import HashClient


def test_exist_false():
    customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
    type = "user"
    hash = HashClient._get_hash({"user": "222"})
    client[customer_uuid][type].insert_one({"_id": hash})
    response = HashClient.exist(customer_uuid, "user", {"user": "123"})
    assert response == False
    client[customer_uuid][type].delete_many({})


def test_exist_true():
    customer_uuid = "c85dc072-7d2e-4f1c-9b8a-b872d0c0be24"
    type = "user"
    hash = HashClient._get_hash({"user": "123"})
    client[customer_uuid][type].insert_one({"_id": hash})
    response = HashClient.exist(customer_uuid, "user", {"user": "123"})
    assert response == True
    client[customer_uuid][type].delete_many({})


def test_exist_many():
    customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
    type = "user"
    hash_1 = HashClient._get_hash({"user": "123"})
    hash_2 = HashClient._get_hash({"user": "456"})
    hash_3 = HashClient._get_hash({"user": "789"})
    client[customer_uuid][type].insert_many([{"_id": hash_1}, {"_id": hash_2}, {"_id": hash_3}])
    response = HashClient.exist_many(customer_uuid, "user", [{"user": "123"}, {"user": "456"}, {"user": "222"}])
    assert isinstance(response, list)
    assert response[0] == True
    assert response[1] == True
    assert response[2] == False
    client[customer_uuid][type].delete_many({})


def test_create():
    customer_uuid = "c85dc072-7d2e-4f1c-9b8a-b872d0c0be24"
    type = "user"
    hash = HashClient._get_hash({"user": "123"})
    response = HashClient.create(customer_uuid, "user", {"user": "123"})
    item = client[customer_uuid][type].find_one(hash)
    assert response == hash
    assert item
    client[customer_uuid][type].delete_many({})


def test_create_many():
    customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
    type = "user"
    hash_1 = HashClient._get_hash({"user": "123"})
    hash_2 = HashClient._get_hash({"user": "456"})
    hash_3 = HashClient._get_hash({"user": "789"})
    response = HashClient.create_many(customer_uuid, "user", [{"user": "123"}, {"user": "456"}, {"user": "789"}])
    item_1 = client[customer_uuid][type].find_one(hash_1)
    item_2 = client[customer_uuid][type].find_one(hash_2)
    item_3 = client[customer_uuid][type].find_one(hash_3)
    assert response == [hash_1, hash_2, hash_3]
    assert item_1
    assert item_2
    assert item_3
    client[customer_uuid][type].delete_many({})


def test_get_many_all():
    customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
    type = "user"
    hash_1 = HashClient._get_hash({"user": "123"})
    hash_2 = HashClient._get_hash({"user": "456"})
    hash_3 = HashClient._get_hash({"user": "789"})
    client[customer_uuid][type].insert_many([{"_id": hash_1}, {"_id": hash_2}, {"_id": hash_3}])
    response = HashClient.get_many(customer_uuid, type, {})
    assert len(response) == 3
    client[customer_uuid][type].delete_many({})


def test_get_many_filtered_by_date():
    customer_uuid = "123"
    type = "user"
    hash_1 = HashClient._get_hash({"user": "123"})
    hash_2 = HashClient._get_hash({"user": "456"})
    hash_3 = HashClient._get_hash({"user": "789"})
    client[customer_uuid][type].insert_many(
        [{"_id": hash_1, "created_at": 123}, {"_id": hash_2, "created_at": 123}, {"_id": hash_3, "created_at": 456}]
    )
    response = HashClient.get_many(customer_uuid, type, filter={"created_at": 200})
    assert len(response) == 1
    client[customer_uuid][type].delete_many({})


def test_get_many_filtered_by_date_and_operator():
    customer_uuid = "123"
    type = "user"
    hash_1 = HashClient._get_hash({"user": "123"})
    hash_2 = HashClient._get_hash({"user": "456"})
    hash_3 = HashClient._get_hash({"user": "789"})
    client[customer_uuid][type].insert_many(
        [{"_id": hash_1, "created_at": 123}, {"_id": hash_2, "created_at": 123}, {"_id": hash_3, "created_at": 456}]
    )
    response = HashClient.get_many(customer_uuid, type, filter={"created_at": 200}, date_comparasion="$lt")
    assert len(response) == 2
    client[customer_uuid][type].delete_many({})


def test_check_customer_uuid_empty():
    customer_uuid = ""
    type = "user"
    obj = {"user": 123}
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_customer_uuid_none():
    customer_uuid = None
    type = "user"
    obj = {"user": 123}
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_type_empty():
    customer_uuid = "123"
    type = ""
    obj = {"user": 123}
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_type_none():
    customer_uuid = "123"
    type = None
    obj = {"user": 123}
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_obj_none():
    customer_uuid = "123"
    type = "user"
    obj = None
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_obj_empty():
    customer_uuid = "123"
    type = "user"
    obj = {}
    with pytest.raises(ValueError):
        HashClient.exist(customer_uuid, type, obj)


def test_check_objs_none():
    customer_uuid = "123"
    type = "user"
    objs = None
    with pytest.raises(TypeError):
        HashClient.exist_many(customer_uuid, type, objs)


def test_check_objs_not_list():
    customer_uuid = "123"
    type = "user"
    objs = {"user": 1}
    with pytest.raises(TypeError):
        HashClient.exist_many(customer_uuid, type, objs)


def test_check_objs_empty():
    customer_uuid = "123"
    type = "user"
    objs = []
    with pytest.raises(ValueError):
        HashClient.exist_many(customer_uuid, type, objs)


def test_check_objs_with_empty_item():
    customer_uuid = "123"
    type = "user"
    objs = [{}]
    with pytest.raises(ValueError):
        HashClient.exist_many(customer_uuid, type, objs)
