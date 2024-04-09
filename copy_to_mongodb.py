"""
1. Write a function `sql_db_to_mongo_db` that takes in the path to an existing SQL db file
2. This function should list all table names in the existing SQL db file
3. Using these table names, create relevant collections in MongoDB
4. Get all the data from each SQL table and input it automatically into the relevant MongoDB collection
5. Make sure there are no duplicates in the Mongo DB file
6. Do a safety check for the SQL file existing
"""

from connect_to_mongo import connect_to_client, get_database, get_database_collection
from db_operations import get_sql_table_names, get_sql_column_names, return_table_data


def convert_to_dict(field_types: dict, data_tuples: list[tuple]) -> list[dict]:
    data_dicts = []
    for data_tuple in data_tuples:
        data_dict = {}
        for i, (key, _) in enumerate(field_types.items()):
            data_dict[key] = field_types[key](data_tuple[i])
        data_dicts.append(data_dict)
    return data_dicts


def sql_db_to_mongo_db() -> None:
    """sql_db_to_mongo_db _summary_

    Function to copy sql database data to mongo database.
    """
    # Connect to client
    # Create or get db
    client = connect_to_client()
    db = get_database(client, "records")

    # Get table names from sql db
    table_names = get_sql_table_names()

    # List of mongo Collections
    collections = []
    for table_name in table_names:
        # Get mongo Collection from db
        collection = get_database_collection(db, table_name)
        # Append mongo Collection to list of Collections
        collections.append(collection)

    # Iterate over mongo Collections
    for collection in collections:
        # Get column names
        column_names = get_sql_column_names(collection.name)
        # Get sql data for specific table
        records = return_table_data(collection.name)
        # Map column names and records to create documents for mongo db
        documents = convert_to_dict(column_names, records)
        collection.insert_many(documents)


def test():
    ...
    # print(data_dicts)
    # # print(collection.name)
    # column_names = get_sql_column_names(collection.name)
    # print(column_names)

    # records = return_table_data(collection.name)
    # for record in records:

    #     for column_name in column_names.keys():
    #         record_dict = {column_name: record}
    #         print(record_dict)

    #     # collection.insert_one(record_dict)
    # print(record)


def main():
    sql_db_to_mongo_db()


if __name__ == "__main__":
    main()
