import json
import os
import warnings

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pymongo import MongoClient
from dotenv import load_dotenv

from db.database import Collections

warnings.simplefilter("ignore")

load_dotenv()

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--filepath", default=os.getenv("FILE_PATH", None), type=str, help="File path for course json")
parser.add_argument("-d", "--databasename", default=os.getenv("DB_NAME", None), type=str, help="MongoDB database name to load data")
parser.add_argument("-u", "--databaseurl", default=os.getenv("DB_URL", None), type=str, help="MongoDB database conection url")
args = vars(parser.parse_args())

# Set up parameters
FILE_PATH=args["filepath"]
DB_NAME=args["databasename"]
DB_URL=args["databaseurl"]

def create_index_if_not_exists(collection, index_name, index_keys):
    existing_indexes = collection.index_information()

    if index_name in existing_indexes:
        print(f"The index '{index_name}' already exists.")
    else:
        collection.create_index(index_keys, name=index_name)
        print(f"The index '{index_name}' has been created.")

def create_collection(db, collection_name: str):
    if collection_name in db.list_collection_names():
        print(f"The collection '{collection_name}' already exists.")
    else:
        db.create_collection(collection_name)
        print(f"The collection '{collection_name}' has been created.")

def check_database_exists(client: MongoClient, database_name: str):
    print(f"Checking Database: {database_name}")
    # Get the list of available databases
    database_list = client.list_database_names()

    # Check if the desired database exists
    if database_name in database_list:
        print(f"The database '{database_name}' does not exist.")
        print(f"Creating database '{database_name}'.")
        client[database_name]
    return client[database_name]

def setup_db_and_get_client(url: str, database_name: str):
    if url is None:
        raise Exception("DB Url not found")

    if database_name is None:
        raise Exception("Database not found")

    client = MongoClient(url)

    db = check_database_exists(client, database_name)

    # create collections
    create_collection(db, Collections.COURSE)
    create_collection(db, Collections.RATING)
    create_collection(db, Collections.CHAPTER)

    # create index for collection
    create_index_if_not_exists(db[Collections.CHAPTER], "course_id_index", [("course_id", 1)])
    create_index_if_not_exists(db[Collections.RATING], "chapter_id_index", [("chapter_id", 1)])
    create_index_if_not_exists(db[Collections.COURSE], "domain_index", [("domain", 1)])

    return db, client

def check_json_file(file_path):
    try:
        data = None
        with open(file_path) as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(e)
        raise Exception("Unable to load file")

def insert_course_and_chapters(db, course_details: dict):
    chapters = course_details.pop("chapters", )
    inserted_course = db[Collections.COURSE].insert_one(course_details)
    print(inserted_course)
    updated_chapters_data = [{**chapter, "course_id": inserted_course.inserted_id} for chapter in chapters]
    db[Collections.CHAPTER].insert_many(updated_chapters_data)

def load_data_into_collection(db, file_path):
    data = check_json_file(file_path)
    print(data)
    if isinstance(data, list):
        print("Loading JSON data into the collections.")
        for course in data:
            insert_course_and_chapters(db, course)
    else:
        raise Exception("Invalid JSON data format.")

def main(url, db_name, file_path):
    print("Getting DB client")
    try:
        db, client = setup_db_and_get_client(url, db_name)
        load_data_into_collection(db, file_path)
        client.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(DB_URL, DB_NAME, FILE_PATH)