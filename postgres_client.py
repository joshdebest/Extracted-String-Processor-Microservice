from datetime import datetime
from decimal import Decimal

from postgres_connection import connection_pool
import psycopg2
import psycopg2.extras


class PostgreSQLClient:

    def __init__(self):
        print('Created PostgreSQLClient')

    def convert_string_to_date(self, string_date):
        if string_date:
            return datetime.strptime(string_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        else:
            return None

    # converts a string to decimal value
    # used for the total amount
    def convert_string_to_decimal(self, string_number):
        try:
            if string_number:
                without_comma = string_number.replace(',', '')
                print("Amount without commas:", without_comma)
                without_dollar_symbol = without_comma.replace('$', '')
                without_dollar_symbol = without_dollar_symbol.replace('S', '')

                print("Amount without $:", without_dollar_symbol)
                return float(without_dollar_symbol)
            else:
                print("Didn't get total amount")
                return None
        except Exception as error:
            print("[ERROR]: convert_string_to_decimal", error)


    def get_doc_type(self, input_document_id):
        try:
            doc_list = {}
            connection = connection_pool.getconn()
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = """SELECT action_type, filing_type_id FROM liens.s3_documents_index WHERE document_id= %s"""
                cursor.execute(query, [input_document_id])
                return_list = cursor.fetchone()
                if return_list:
                    print("Found State")
                    print(return_list["action_type"], return_list["filing_type_id"])
                    action_type = str(return_list["action_type"]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                    filing_type = str(return_list["filing_type_id"]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                    doc_list = {"document_id": input_document_id, "action_type": action_type, "filing_type_id": filing_type}

            connection_pool.putconn(connection)
            return doc_list
        except psycopg2.OperationalError as error:
            print(error)
            print("Failed to insert into update document tracking process for ocr\n")


    def update_mysql_document_tracking_process_completed_string_processing(self, document_id):
        try:
            connection = connection_pool.getconn()
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = """UPDATE document_sequence.processed_document_tracker_sequence SET completed_string_processing = %s WHERE document_id = %s """
                cursor.execute(query, [True, document_id])
            connection.commit()
            connection_pool.putconn(connection)
        except Exception as error:
            print(error)


    # function that inserts data returned from string manipulation into State_Lien table in mySQL
    def insert_state_lien(self, ocr_dict):
        try:
            connection = connection_pool.getconn()
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                insert_area_code_and_postal_code_joint = """ INSERT INTO liens.state_liens (file_number, date_filed, certificate_number, letter_id,
                                   total, dated, ftb_account, corporation_number, FEIN, sos_number, taxable_years, lien_id, document_id) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                cursor.execute(insert_area_code_and_postal_code_joint, (ocr_dict['file_number'],
                                                                        self.convert_string_to_date(ocr_dict['date_filed']),
                                                                        ocr_dict['certificate_number'],
                                                                        ocr_dict['letter_id'],
                                                                        self.convert_string_to_decimal(ocr_dict['total']),
                                                                        self.convert_string_to_date(ocr_dict['dated']),
                                                                        ocr_dict['ftb_account'],
                                                                        ocr_dict['corporation_number'],
                                                                        ocr_dict['FEIN'],
                                                                        ocr_dict['sos_number'],
                                                                        ocr_dict['taxable_years'],
                                                                        ocr_dict['lien_id'],
                                                                        int(ocr_dict['document_id'])))
                connection.commit()

            print("Successful insert into State_Liens table\n")
        except Exception as error:
            print("Failed to insert into State_Liens table\n")
            print(error)
        finally:
            connection_pool.putconn(connection)


    # function that inserts data returned from string manipulation into federal_liens table in mySQL
    def insert_federal_lien(self, ocr_dict):
        try:
            connection = connection_pool.getconn()
            print("OCR Dictionary: ", ocr_dict)
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                insert_federal = """ INSERT INTO liens.federal_liens (total, document_id) VALUES (%s, %s) """
                cursor.execute(insert_federal, (self.convert_string_to_decimal(ocr_dict['total']),
                                                int(ocr_dict['document_id'])
                                                ))
                connection.commit()

            print("Successful insert into federal_liens table\n")
        except Exception as error:
            print("Failed to insert into federal_liens table\n")
            print(error)

        finally:
            connection_pool.putconn(connection)
