import os

import yaml
from pymongo import MongoClient
from pymongo.collection import Collection


def get_mongo_db_collection(
    cfg_db_name: str, cfg, cfg_collection_name: str = "collection_name"
) -> Collection:
    """Returns properties of specific database from configuration.
    :param cfg_collection_name: name of property containing collection name"""
    client = MongoClient(cfg[cfg_db_name]["connection_string"])
    database_name = cfg[cfg_db_name]["database_name"]
    collection_name = cfg[cfg_db_name][cfg_collection_name]

    return client[database_name][collection_name]


def load_yaml_file(filepath) -> dict:
    # todo - use ConfigStore?
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf8") as ymlfile:
        return yaml.safe_load(ymlfile)
