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

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "TheMarginator Streamlit"
spread = Spread(spreadsheetname,client = client)
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

@st.cache()
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

def update_the_spreadsheet(spreadsheetname,dataframe):
    worksheet = sh.worksheet("Intake Sheet")
    col_list = worksheet.row_values(1)
    spread.df_to_sheet(dataframe[col_list],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

#df = load_the_spreadsheet('Intake Sheet')

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
