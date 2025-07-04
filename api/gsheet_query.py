from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import pandas as pd
import gspread
import json 
import os
load_dotenv()


#############################
#        Gsheet Auth        #
#############################
creds_json_str = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
scope = "https://www.googleapis.com/auth/spreadsheets"

if creds_json_str is None:
    raise ValueError("GOOGLE_SHEETS_CREDS_JSON environment variable not set.")

creds_dict = json.loads(creds_json_str)
gc = gspread.service_account_from_dict(creds_dict)


def query_google_sheet_worksheet ():

    sh = gc.open("metro_united_way_data")
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()
    
    df = pd.DataFrame(data)
    return print(df.head())


query_google_sheet_worksheet()










