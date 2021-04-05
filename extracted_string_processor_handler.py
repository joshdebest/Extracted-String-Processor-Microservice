from mongodb import MongoDB
import string_manipulation
from postgresql_client import PostgreSQLClient
from ast import literal_eval


mongodb_controller = MongoDB()
postgresql_client = PostgreSQLClient()

def clean_data_from_mongodb(document_data):
    try:
        print(type(document_data))
        newArray2 = []
        for i in document_data:
            newArray2.append(i.decode('utf-8'))
        print("ARRAY 2 ", newArray2)
    except Exception as error:
        print("Clean up data error", error)
    return newArray2


def start_extraction_string_processor():
    doc_list = mongodb_controller.get_documents_from_database()

    try:

        number_of_docs = 0

        for doc in doc_list:
            try:
                print("Getting type array")
                print(doc.get("document_id"))
                print(clean_data_from_mongodb(doc.get("data")))
                type_array = postgresql_client.get_doc_type(doc.get("document_id"))
                print(type_array)
                print(type_array["action_type"], type_array["filing_type_id"], type_array["document_id"])

                if type_array["action_type"] == "Lien Financing Stmt":
                    if type_array["filing_type_id"] == "Notice of State Tax Lien":
                        number_of_docs = number_of_docs + 1
                        data_array = clean_data_from_mongodb(doc.get("data"))
                        #db_input = string_manipulation.do_string_manipulation(data_array, type_array["filing_type_id"],
                        #                                                      type_array["action_type"], type_array["document_id"])
                        db_input = string_manipulation.process_notice_of_state_lien(data_array, type_array["document_id"])

                        #mysql_client.update_mysql_document_tracking_process_completed_string_processing(doc.get("document_id"))

                        postgresql_client.insert_state_lien(db_input)
                        # mongodb_controller.insert_state_lien(type_array["document_id"], db_input)

                    elif type_array["filing_type_id"] == "Notice of Federal Tax Lien":
                        number_of_docs = number_of_docs + 1
                        #mysql_client.insert_state_lien(db_input)
                        data_array = clean_data_from_mongodb(doc.get("data"))
                        db_input = string_manipulation.process_federal_lien(data_array, type_array["document_id"])
                        postgresql_client.insert_federal_lien(db_input)

                print("Number of Docs:", number_of_docs)

            except Exception as error:
                print("Start extraction (inside loop) [ERROR]", error)

    except Exception as error:
        print("Start extraction (outside loop) [ERROR]", error)

