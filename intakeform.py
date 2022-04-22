from calendar import month
from decimal import ROUND_UP
from re import sub
import streamlit as st
from deta import Deta
from gsheetsdb import connect
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
from gsheetsdb import connect
from pandas import DataFrame
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")

import gspread

credentials = {
  "type": "service_account",
  "project_id": "themarginator",
  "private_key_id": "7954daaac827ed086e026dbeef2145e47c7234e2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvC/cgqekuksyK\nzOOS8cJoQ2TkyawkramcDZuAoeqE6fwJnvWbyzdCsImOgxrc2MmZ2njzQtsR2Spe\nU8s2iqxdKk48EOrS15JKvYS/zm/P8JxfPMFjm9ymsiCN5R8jp/r/Ym7iq4nUnfxX\nxES65BX702/ORdmULO0vUHV0cILbqtGbmhOSSq9SR7Am+taznFGN/KDGUsSdIH25\nZ6eOZPct+9PFaXzOum08BwDFWr/YMFcFMYZq0djXuCpooOF7Vnu97SBkuq7A/AMi\n1LEjrLADAaopBmtoIjx5uTbryhuxOriUBO/p6Jsy1++QgYKaYDZckNd6wBGPBYtb\nuxhDFCibAgMBAAECggEAMaaGMTigkHpJFDGrdzmlt+ctzgs6DalIi5/8dI74szyf\nJad16PvKL9tdGRQs4WmIPWCPoAhdlQFxGBJSeKT64O4oBLeTs7w7nYGGDtWiN2v7\nHrRf8j36ZzntK/JKU9XIxvmHlDmtvaYWNlrQV+ZsKeK+OtbrMTFREXOT7TQgmeew\nI/tXuZXf0hKxhcU0mqNrAvTzqTwAGRZXkUTkaWSejy6EaAjLF+hwdEObq5ODtcMB\n5/wMx1I53OnNQIBmvxFaxPL8YFUSV3bCT2bmpSDK+hCf/QaVaEABTClHdyYy0JF4\nfgOj6gP8lrL+VLrZruGZkGHfiAerFjZvTghzqkd1mQKBgQDpfm71P9b03yJDXZlz\nbXR9X3eSDy8P+Xi4sm3SJb9LoNI/bopDCJiPYXE4ydK4AOWB68iGVkjIxbZc7Dnn\njrYguO5b1yNTmvLFvRtF+NcRXyguLkkz9X0fr8iiNmgA5xVaMIjXR0kBiW9bhWep\n5jzNeWIEV/xNMFyUMwI+XfleHwKBgQC/61KJaTHIzO4KjCtiXgV8wSj8ZYiiC+Ls\nYMYqwtnBQherFRicMJfUO0nN41UHz0RybQusbS7bOhK9TNcIQQt5Ij/ZCnO4PLPm\ngp06QBBvyoMKENIkuIQtU4KNErtNv2n6WFsBDJxlnAc9hTKE/Wm8LaBGuNg+akoy\nMQCM2LxuBQKBgDv6uYAQhSRkCUYqzhdjn4/xLSL8+Ybt+7/ePe3Euo4v4rJer++m\nTqJOUqpW1eVkfZBRRDKWCZ5hg4X9PKap90kSmFBJRI7ed8yp1k60LHMO8aBjTXSm\ndBzmp/Bbb34D3m1LmGtMqYlWh5+H9mgjd60EqFQbUfl2GeIL9GCW/U7bAoGAfy/M\nuxPj0lc9SfAqsD3vFQZNyzbencWS1WQs8BnBhbnvRYntjVUGybeg6blGmK5bhhmO\nKu8QpmiOErXhq66vk8+G0KeEmQxhjNnyqK/cNLnYrcsH+R3vOrqlQiivyI6aBTaY\n2NEqtIv6oGKtYEUw1WzHUxcc+AAou6qN2smn1qECgYBP9v9ZfFnmb57wnkZN0Vkt\nhB2HVDVg208rNeCnPcUbysPnunVVE5Pc/s1YW/sud+UI6oCqKonxRsCy2bnjttgD\n6rmEH1Muy9xSzwyEh4Ldig7gbIx2VGaADIWTOVO1OaRLSsIWOcCnvoFresMGgKfS\nWF4LxHeffdM3Tj7ktcMqfA==\n-----END PRIVATE KEY-----\n",
  "client_email": "matthsq@themarginator.iam.gserviceaccount.com",
  "client_id": "106943139207166064486",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/matthsq%40themarginator.iam.gserviceaccount.com"
}


gc = gspread.service_account_from_dict(credentials)

sh = gc.open("TheMarginator Streamlit")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "TheMarginator Streamlit"
spread = Spread(spreadsheetname,client = client)



@st.cache()

def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

def update_the_spreadsheet(spreadsheetname,dataframe):
    worksheet = sh.worksheet("Intake Sheet")
    col_list = worksheet.row_values(1)
    spread.df_to_sheet(dataframe[col_list],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')


def app():
    col1, col2, col3 = st.columns(3)
    with st.form(key='clientdata'):
        
        with col1:
            st.header('Client Information')
            name = st.text_input("Your name")
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            zipcode = st.text_input("Zip Code")
            jobnumber = st.number_input(label="Job Number", step=1)
            jobtype = st.selectbox(
                'Pick a Job Type',
                ('Residential', 'Commercial'))
            date = st.date_input(label="Date")
        
        with col2:
            st.header('Labor')
            journeyman_normal = st.number_input(label="Journeyman - Normal", step=1)
            apprentice_normal = st.number_input(label="Apprentice - Normal", step=1)
            journeyman_overtime = st.number_input(label="Journeyman - Overtime", step=1)
            apprentice_overtime = st.number_input(label="Apprentice - Overtime", step=1)
            journeyman_rate = st.number_input(label="Journeyman - Rate", step=1)
            apprentice_rate = st.number_input(label="Apprentice - Rate", step=1)
            burden = st.number_input(label="Burden", step=1)
            chargerate = st.number_input(label="Charge Rate", step=1)
        
        with col3:
            st.header('Cost for Project')
            modulewatts = st.number_input(label="Module Watts", step=1)
            numberofmodules = st.number_input(label="Number of Modules", step=1)
            materialscost = st.number_input(label="Materials Cost", step=1)
            materialstax = st.number_input(label="Material Tax", step=1)
            subcontractorcost = st.number_input(label="Subcontractor Cost", step=1)
            subcontractortax = st.number_input(label="Subcontractor Tax", step=1)
            equipmentrentalcost = st.number_input(label="Equipment Cost", step=1)
            equipmentrentaltax = st.number_input(label="Equipment Tax", step=1)
            permitcost = st.number_input(label="Permit Cost", step=1)
            permittax = st.number_input(label="Permit Tax", step=1)
            projecttax = st.number_input(label="Project Tax", step=1)

        submitted = st.form_submit_button(label = 'Store in database')

        if submitted:
            opt = {
                "Name": name,
                "Address": address,
                "City": city,
                "State": state,
                "Zip Code": zipcode,
                "Job Number": jobnumber,
                "Job Type": jobtype,
                "Date": date,
                "Journeyman Normal": journeyman_normal,
                "Apprentice Normal": apprentice_normal,
                "Journeyman Overtime": journeyman_overtime,
                "Apprentice Overtime": apprentice_overtime,
                "Apprentice Rate": apprentice_rate,
                "Journeyman Rate": journeyman_rate,
                "Burden": burden,
                "Charge Rate": chargerate,
                "Module Watts": modulewatts,
                "# of Modules": numberofmodules,
                "Materials Cost": materialscost,
                "Material Tax": materialstax,
                "Subcontractor Cost": subcontractorcost,
                "Subcontractor Tax": subcontractortax,
                "Equipment Rental Cost": equipmentrentalcost,
                "Equipment Rental Tax": equipmentrentaltax,
                "Equipment Rental Cost": equipmentrentalcost,
                "Equipment Rental Tax": equipmentrentaltax,
                "Permit Cost": permitcost,
                "Permit Tax": permittax,
                "Project Tax": projecttax
                }
            
            df = load_the_spreadsheet('Intake Sheet')
            
            opt_df = DataFrame([opt])
            opt_df['Quarter'] = pd.to_datetime(opt_df['Date'])
            opt_df['Quarter'] = opt_df['Quarter'].dt.quarter
            opt_df['Total Man Hours'] = opt_df['Journeyman Normal'] + opt_df['Apprentice Normal'] + opt_df['Journeyman Overtime'] + opt_df['Apprentice Overtime']
            opt_df['Labor Without Burden'] =((opt_df['Journeyman Normal'] * opt_df['Journeyman Rate']) + 
                        (opt_df['Apprentice Normal'] * opt_df['Apprentice Rate']))
            opt_df['Labor With Burden'] = opt_df['Labor Without Burden'] + (opt_df['Labor Without Burden']*opt_df['Burden'])
            opt_df['Total Cost'] = opt_df['Labor With Burden'] + opt_df['Materials Cost'] + opt_df['Subcontractor Cost'] + opt_df['Equipment Rental Cost'] + opt_df['Permit Cost']  
            opt_df['Total Cost To Client'] = ((opt_df['Labor With Burden']+(opt_df['Labor With Burden']*opt_df['Burden']))
            + (opt_df['Materials Cost'] + (opt_df['Materials Cost'] * opt_df['Material Tax']))
            + (opt_df['Subcontractor Cost'] + (opt_df['Subcontractor Cost'] * opt_df['Subcontractor Tax'])) 
            + (opt_df['Equipment Rental Cost'] + (opt_df['Equipment Rental Cost'] * opt_df['Equipment Rental Tax']))
            + (opt_df['Permit Cost'] + (opt_df['Permit Cost'] * opt_df['Permit Tax'])))
            opt_df['Gross Profit'] = opt_df['Total Cost To Client'] - opt_df['Total Cost']
            opt_df['Sales Per Man Hour'] = opt_df['Total Cost To Client'] / opt_df['Total Man Hours']
            opt_df['GP %'] = (opt_df['Gross Profit'] / opt_df['Total Cost To Client'])*100
            opt_df['GP/MHR'] = opt_df['Gross Profit'] / opt_df['Total Man Hours']          
            opt_df['The Score'] = opt_df['GP/MHR'] + (opt_df['GP %']*100)
    
            new_df = df.append(opt_df, ignore_index=True)
            update_the_spreadsheet('Intake Sheet', new_df)
app()
