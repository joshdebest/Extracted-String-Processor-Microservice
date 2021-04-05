import pymongo
from pymongo import MongoClient


class MongoDB:

    mongodb_client = None
    orion_project_database = None

    def __init__(self):
        try:
            self.mongodb_client = MongoClient(host='', port=)
            self.orion_project_database = self.mongodb_client.orion_project
        except Exception as error:
            print("[ERROR]  When creating MongoDB Client Connection:", error)

    def get_documents_from_database(self):
        try:
            lien_collection = self.orion_project_database.lien_collection
            results = []

            for x in lien_collection.find():
                fetched_data = {"document_id": x.get("document_id"), "data": x.get("data")}

                results.append(fetched_data)
            print("Successfully fetched from MongoDB")
            return results

        except Exception as error:
            print("Failed fetching from MongoDB")
            print(error)
            return False

    def insert_state_lien(self, document_id, extracted_str):
        try:
            mongodb_document = {"document_id": document_id, "data": extracted_str}
            self.orion_project_database.state_lien_collection.insert_one(mongodb_document)
            print("Successfully inserted into MongoDB state lien collection")

        except Exception as error:
            print("Failed inserting into MongoDB")
            print(error)
