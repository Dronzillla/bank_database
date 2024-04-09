from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv, find_dotenv
import os
import sys


def connect_to_client() -> MongoClient:
    load_dotenv(find_dotenv())
    password = os.environ.get("MONGODB_PWD")
    try:
        connection_str = f"ENTER CONNECTION STRING"
        # Connecting to client
        client = MongoClient(connection_str)
        return client
    except ConnectionFailure as err:
        print(f"{err.args[0]}")
        sys.exit()


def get_database(client: MongoClient, db_name: str) -> Database:
    database = client[db_name]
    return database


def get_database_collection(db: Database, collection_name: str) -> Collection:
    collection = db[collection_name]
    return collection


def main():
    ...
    # For testing
    # client = connect_to_client()
    # database = get_database(client, "hello")
    # collection = get_database_collection(database, "first")


if __name__ == "__main__":
    main()
