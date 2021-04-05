import mysqlx
from datetime import datetime
from decimal import Decimal

########################################################################################
## READ ME: This code has been updated for postgres, we will no longer be using MySQL ##
########################################################################################

client_connection_credentials = {
    'host': host_url,
    'port': mysql_port_number,
    'user': username,
    'password': password
}

client_options = {
    'pooling': {
        "max_size": mysql_pool_size,
        "max_idle_time": 30000
    }
}


def convert_string_to_date(string_date):
    if string_date:
        return datetime.strptime(string_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    else:
        return None


def convert_string_to_decimal(string_number):
    if string_number:
        remove_comma = string_number.replace(',', '')
        return Decimal(remove_comma)
    else:
        return None


mysql_client = mysqlx.get_client(client_connection_credentials, client_options)


# searches the s3_documents_index table to get the action_type & doc_id of current doc
def get_doc_type(input_document_id):
    doc_list = {}
    try:
        session = mysql_client.get_session()

        my_schema = session.get_schema('orion_dirty_database')
        my_table = my_schema.get_table('s3_documents_index')

        # Find a row in the SQL Table
        res = my_table.select(["action_type", "filing_type_id"]) \
            .where('document_id = :input_document_id') \
            .bind('input_document_id', input_document_id) \
            .execute()

        row = res.fetch_one()
        if row:
            print(row["action_type"], row["filing_type_id"])
            action_type = str(row["action_type"]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
            filing_type = str(row["filing_type_id"]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
            doc_list = {"document_id": input_document_id, "action_type": action_type, "filing_type_id": filing_type}

        session.close()
        return doc_list

    except Exception as error:
        print("get_doc_type", error)


def update_mysql_document_tracking_process_completed_string_processing(document_id):
    try:
        session = mysql_client.get_session()
        my_schema = session.get_schema('orion_dirty_database')
        my_table = my_schema.get_table('processed_document_tracker_sequence')
        my_table.update() \
            .set("completed_string_processing", True) \
            .where('document_id = :input_document_id') \
            .bind('input_document_id', document_id) \
            .execute()
        session.close()
    except Exception as error:
        print(error)


# function that inserts data returned from string manipulation into State_Lien table in mySQL
def insert_state_lien(ocr_dict):
    print(ocr_dict)
    try:
        session = mysql_client.get_session()
        my_schema = session.get_schema('orion_dirty_database')
        database_table = my_schema.get_table('State_Liens')
        database_table.insert(['file_number', 'date_filed', 'taxpayer_name', 'address', 'certificate_number',
                               'letter_id', 'total', 'dated', 'ftb_account', 'corporation_number', 'FEIN',
                               'sos_number', 'taxable_years', 'lien_id', 'document_id']) \
            .values(ocr_dict['file_number'], convert_string_to_date(ocr_dict['date_filed']), ocr_dict['taxpayer_name'], ocr_dict['address'],
                    ocr_dict['certificate_number'], ocr_dict['letter_id'], convert_string_to_decimal(ocr_dict['total']), convert_string_to_date(ocr_dict['dated']),
                    ocr_dict['ftb_account'], ocr_dict['corporation_number'], ocr_dict['FEIN'], ocr_dict['sos_number'],
                    ocr_dict['taxable_years'], ocr_dict['lien_id'],
                    int(ocr_dict['document_id'])) \
            .execute()
        session.close()
        print("Successful insert into State_Liens table\n")
    except Exception as error:
        print("Failed to insert into State_Liens table\n")
        print(error)


# function that inserts data returned from string manipulation into Judgment_Lien table in mySQL
def insert_judgment_lien(ocr_dict):
    try:
        session = mysql_client.get_session()
        my_schema = session.get_schema('orion_dirty_database')
        database_table = my_schema.get_table('Judgment_Liens')
        database_table.insert(
            ['file_number', 'date_filed', 'debtor_org_name', 'debtor_address', 'creditor_org_name', 'creditor_address',
             'court_name', 'action_title', 'action_number', 'date_entered', 'date_of_renewals', 'amount', 'date_of_notice',
             'dated', 'document_id']) \
            .values(ocr_dict['file_number'], convert_string_to_date(ocr_dict['date_filed']), ocr_dict['debtor_org_name'],
                    ocr_dict['debtor_address'],
                    ocr_dict['creditor_org_name'], ocr_dict['creditor_address'], ocr_dict['court_name'],
                    ocr_dict['action_title'],
                    ocr_dict['action_number'], ocr_dict['date_entered'], ocr_dict['date_of_renewals'],
                    convert_string_to_decimal(ocr_dict['amount']),
                    convert_string_to_date(ocr_dict['date_of_notice']),
                    convert_string_to_date(ocr_dict['dated']), int(ocr_dict['document_id'])) \
            .execute()
        session.close()
        print("Successful insert into Judgment_Liens table\n")
    except Exception as error:
        print("Failed to insert into Judgment_Liens table\n")
        print(error)


# TODO PASS IN THE AMOUNT & FILE NUMBER
def update_state_lien(ocr_str):
    query = "UPDATE state_liens SET amount=amount-%s WHERE file_number = %s"
    try:
        conn = mysql.connector.connect(host=host_url,
                                       database=database_name,
                                       user=username,
                                       password=password)
        cursor = conn.cursor()
        cursor.execute(query, ocr_str)
        conn.commit()
        conn.close()
        print("Successful database update\n")
    except errorcode:
        print("Failed to update database\n")
        print(errorcode)


# TODO PASS IN THE AMOUNT & FILE NUMBER
def update_judgment_lien(ocr_str):
    query = "UPDATE judgment_liens SET amount=amount-%s WHERE file_number = %s"
    try:
        conn = mysql.connector.connect(host=host_url,
                                       database=database_name,
                                       user=username,
                                       password=password)
        cursor = conn.cursor()
        cursor.execute(query, ocr_str)
        conn.commit()
        conn.close()
        print("Successful insert into database\n")
    except errorcode:
        print("Failed to insert into database\n")
        print(errorcode)
