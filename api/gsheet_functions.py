from dotenv import load_dotenv
import pandas as pd
import gspread
import json 
import os
load_dotenv()



class GeezSheets:


    def query_google_sheet_worksheet(self):
        
        creds_json_str = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
        if creds_json_str is None:
            raise ValueError("GOOGLE_SHEETS_CREDS_JSON environment variable not set.")

        creds_dict = json.loads(creds_json_str)
        gc = gspread.service_account_from_dict(creds_dict)

        sh = gc.open("metro_united_way_data")
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df 


    def update_gsheet_data (self, dataframe):    
        creds_json_str = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
        if creds_json_str is None:
            raise ValueError("GOOGLE_SHEETS_CREDS_JSON environment variable not set.")

        creds_dict = json.loads(creds_json_str)
        gc = gspread.service_account_from_dict(creds_dict)

        sh = gc.open("metro_united_way_data")
        worksheet = sh.get_worksheet(0)
        altered_data = [dataframe.columns.tolist()] + dataframe.values.tolist()
        
        return worksheet.update('A1', altered_data)

