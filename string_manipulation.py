import re


# process ocr string from notice of state tax lien document
def process_notice_of_state_lien(extracted_str, doc_id):
    print('---- Started to process_state_lien_string ----\n')
    try:
        data = {} # dictionary to organize the important data
        keys = ["file_number", "date_filed", "taxpayer_name", "address", "certificate_number", "letter_id", "total",
                "dated", "ftb_account", "corporation_number", "FEIN", "sos_number", "taxable_years", "lien_id", "document_id"]
        data = data.fromkeys(keys, None)
        data["document_id"] = doc_id
        for x in range(len(extracted_str)):
            # File #
            if extracted_str[x].find("File #:") > 0:
                loc1 = extracted_str[x].find("File #:")
                data["file_number"] = extracted_str[x][loc1+8:loc1+21]
            # Date filed
            if extracted_str[x].find("Date Filed: ") > 0:
                loc2 = extracted_str[x].find("Date Filed: ")
                data["date_filed"] = extracted_str[x][loc2+12:]

            # Taxpayer Name
            if extracted_str[x].find("hereby certifies that the following named taxpayer") > 0:
                data["taxpayer_name"] = extracted_str[x+1]

            # Address
            if extracted_str[x].find("hose last known address was") > 0:
                loc8 = extracted_str[x].find("was")
                data["address"] = extracted_str[x][loc8+3:]

            # Certificate No / Certificate Number
            if extracted_str[x] == "Certificate No.":
                data["certificate_number"] = extracted_str[x+1]
            elif extracted_str[x].find("ertificate No.") > 0:
                loc6 = extracted_str[x].find("ertificate No.")
                if len(extracted_str[x]) > 25:
                    data["certificate_number"] = extracted_str[x][loc6+15:loc6+25]
                else:
                    data["certificate_number"] = extracted_str[x][loc6+15:]

            # Letter ID
            if extracted_str[x].find("etter ID.") > 0:
                loc7 = extracted_str[x].find("etter ID.")
                data["letter_id"] = extracted_str[x][loc7+10:]

            # Amount Due / Total / Total Lien Amount
            if extracted_str[x].find("TOTAL $") > 0:
                loc3 = extracted_str[x].find("TOTAL $")
                data["total"] = extracted_str[x][loc3+6:]
            # TODO make this is accurate
            elif extracted_str[x].find("otal Lien Amount") > 0:
                data["total"] = extracted_str[x+1][2:]
            elif extracted_str[x].find("AX PERIOD PENALTY INTEREST TOTAL") > 0:
                total_amount = re.search(r'(?:[^$]*($)){4}', extracted_str[x]).group()
                loc9 = total_amount.find(" to")
                data["total"] = total_amount[:loc9]

            # Dated
            dated = re.search(r'^([1-9]|1[0-2])(\/)([1-9]|1[0-9]|2[0-9]|3[0-1])(\/)20[0-9][0-9]$', extracted_str[x])
            if dated:
                dated.group()
                data["dated"] = extracted_str[x]
            elif extracted_str[x].find("ated: ") > 0:
                loc4 = extracted_str[x].find("ated: ")
                data["dated"] = extracted_str[x][loc4+5:]
            elif extracted_str[x].find("ATED:") > 0:
                loc5 = extracted_str[x].find("ATED:")
                data["dated"] = extracted_str[x][loc5+5:]

            # FTB Account Number
                # data["ftb_account"]
            # Corporation Number
                # data["corporation_number"]
            # FEIN
                # data["FEIN"]
            # SOS Number
                # data["sos_number"]
            # Taxable Years
                # data["taxable_years"]
            # Lien ID
            if extracted_str[x].find("ien ID: :") > 0:
                loc10 = extracted_str[x].find("ien ID: :")
                data["lien_id"] = extracted_str[x][loc10+8:loc10+14]
        taxpayer = []
        address = []
        for i in range(20):
             taxpayer.append(extracted_str[i])
             address.append(extracted_str[i])
        data["taxpayer_name"] = taxpayer
        data["address"] = address
        return data

    except Exception as e:
        print("**** Processing state lien failed moving on ****\n")
        print(e)
        return False


# process ocr string from notice of judgment lien document
def process_notice_of_judgment_lien(extracted_str, doc_id):
    print('---- Started to process_judgment_string ----\n')
    try:
        Dict = {}
        keys = ["file_number", "date_filed", "debtor_org_name", "debtor_address", "creditor_org_name", "creditor_address",
                "court_name", "action_title", "action_number", "date_entered", "date_of_renewals", "amount", "date_of_notice",
                "dated", "document_id"]
        # Initialize all key values to Null
        Dict = Dict.fromkeys(keys, None)
        Dict["document_id"] = doc_id
        for x in range(len(extracted_str)):
            # File #
            if extracted_str[x].find("File #:") > 0:
                loc1 = extracted_str[x].find("File #:")
                Dict["file_number"] = extracted_str[x][loc1+8:loc1+21]
            # Date filed
            if extracted_str[x].find("Date Filed: ") > 0:
                loc2 = extracted_str[x].find("Date Filed: ")
                Dict["date_filed"] = extracted_str[x][loc2+12:]
            # Debtor's / Organization Name
                # Dict["debtor_org_name"]
            # Debtor's Address
                # Dict["debtor_address"]
            # Creditor's / Organization Name
                # Dict["creditor_org_name"]
            # Creditor's Address
                # Dict["creditor_address"]
            # Name of Court Where Judgment was Entered
                # Dict["court_name"]
            # Title of the Action
                # Dict["action_title"]
            # Number of this Action / Case Number
                # Dict["action_number"]
            # Date Judgment was Entered
                # Dict["date_entered"]
            # Date of renewals
                # Dict["date_of_renewals"]
            # Amount Required to Satisfy Judgment at This Date of Notice
                # Dict["amount"]
            # Date of this Notice
                # Dict["date_of_notice"]
            # Dated
                # Dict["dated"]

        print("String man:", Dict)
        return Dict

    except Exception as e:
        print("**** Processing judgement lien failed moving on ****\n")
        print(e)
        return False


# process ocr string from release of lien document
def process_release_of_state_lien(extracted_str, doc_id):
    print('---- Started to process_release_state_lien_string ----')
    try:
        Dict = {}
        keys = ["file_number", "date_filed", "taxpayer_name", "address", "certificate_number", "letter_id", "total",
                "dated", "ftb_account", "corporation_number", "FEIN", "sos_number", "taxable_years", "lien_id"
                "release_lien", "recorded_on"]
        Dict = Dict.fromkeys(keys, None)
        Dict["document_id"] = doc_id
        for x in range(len(extracted_str)):
            # Certificate No
            if extracted_str[x] == "CERTIFICATE NO.":
                Dict["certificate_number"] = extracted_str[x+1]
            # Letter ID
            elif extracted_str[x] == "LETTER ID.":
                Dict["letter_id"] = extracted_str[x+1]
            # In the amount of
            elif extracted_str[x] == "In the amount of":
                Dict["total"] = extracted_str[x-1]
            # which was recorded on
            elif extracted_str[x] == "which was recorded on":
                Dict["recorded_on"] = extracted_str[x-1]
            # in volume/page
            elif extracted_str[x] == "in volume/page":
                Dict["release_lien"] = extracted_str[x-1]

            # File #
            if extracted_str[x].find("File #:") > 0:
                loc1 = extracted_str[x].find("File #:")
                Dict["file_number"] = extracted_str[x][loc1+8:loc1+21]
            # Date filed
            if extracted_str[x].find("Date Filed: ") > 0:
                loc2 = extracted_str[x].find("Date Filed: ")
                Dict["date_filed"] = extracted_str[x][loc2+12:]
            # Name of Taxpayer
            if extracted_str[x].find("hereby releases and certifies that there has been released all property from any lien imposed") > 0:
                Dict["taxpayer_name"] = extracted_str[x+1]

            # TODO fix this; .find() function not working
            # Dated
            if extracted_str[x].find("Date: ") > 0:
                loc3 = extracted_str[x].find("Date: ")
                Dict["dated"] = extracted_str[x][loc3+6:]

        return Dict

    except Exception as e:
        print("**** Processing release of state lien failed moving on ****")
        print(e)
        return False


# Organizes the 'total' & 'document_id' to be inserted into postgres
def process_federal_lien(extracted_str, doc_id):
    print('---- Started to process__release_federal_string ----')
    try:
        data = {} # dictionary to organize the important data
        keys = ["total", "document_id"]
        data = data.fromkeys(keys, None)

        data["total"] = extracted_str[0]
        data["document_id"] = doc_id
        print(data["total"])
        print(data["document_id"])

        return data

    except Exception as e:
        print("**** Processing federal lien file failed moving on ****")
        print(e)
        return False


# TODO figure out what data we need from this document, the doc format is rough
def process_satisfaction_of_judgment():
    print('---- Started to process_satisfaction_of_judgment_string ----')
    try:
        db_input = []
        # File #
        # Date filed

        return db_input

    except Exception as e:
        print("**** Processing file failed moving on ****")
        print(e)
        return False


# main function that cleanses the data pulled from mongodb
# and prepares it to be inserted into the appropriate MySQL table
def do_string_manipulation(extracted_str, doc_type, action_type, doc_id):
    if doc_type == "Notice of State Tax Lien" and action_type == "Termination":
        final_str = process_release_of_state_lien(extracted_str, doc_id)
        return final_str
    elif doc_type == "Notice of State Tax Lien":
        final_str = process_notice_of_state_lien(extracted_str, doc_id)
        return final_str
    elif doc_type == "Judgment Lien" and action_type == "Termination":
        final_str = process_satisfaction_of_judgment()
        return final_str
    elif doc_type == "Judgment Lien":
        final_str = process_notice_of_judgment_lien(extracted_str, doc_id)
        return final_str
    elif doc_type == "Notice of Federal Tax Lien" and action_type == "Termination":
        final_str = process_federal_lien()
        return final_str
    else:
        print("No Matches")
        return

