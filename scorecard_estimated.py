import gspread
import pandas as pd
import gspread_dataframe as gd
import streamlit as st
import itertools
from google.oauth2.service_account import Credentials

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

ws1 = gc.open("TheMarginator Streamlit").worksheet("Intake Sheet")
ws2 = gc.open("TheMarginator Streamlit").worksheet("Actuals")

def app():
    st.markdown('Enter Actual Values Below')
   
    with st.form(key='data1'):
        jobnumber = st.number_input(label="Job Number", step=1)
        totalmanhours_actual = st.number_input(label="Total Man Hours Actual", step=1)
        totalcost_actual = st.number_input(label="Total Cost Actual", step=1)
        totalcosttoclient_actual = st.number_input(label="Total Cost to Client Actual", step=1)

        submitted = st.form_submit_button(label = 'Append Estimated Results')
    
        if submitted:
        
            opt = {
                "Job Number": jobnumber,
                "Total Man Hours Actual": totalmanhours_actual,
                "Total Cost Actual": totalcost_actual,
                "Total Cost to Client Actual": totalcosttoclient_actual,
            }
            
            opt_df = pd.DataFrame([opt])
            opt_df['Gross Profit Actual'] = opt_df['Total Cost to Client Actual'] - opt_df['Total Cost Actual']            
            opt_df_data = opt_df.values.tolist()

            old_df = gd.get_as_dataframe(ws1)
            old_df = old_df.fillna(0)
            old_df = old_df[old_df['Job Number']==(jobnumber)]
            old_df_data = old_df.values.tolist()

            combined_data = opt_df_data + old_df_data
            results = list(itertools.chain.from_iterable(combined_data))
            updated_row = pd.DataFrame([results])
            updated_row_data = updated_row.values.tolist()
            ws2.append_rows(updated_row_data)

            
            estimatedmanhours = int(old_df['Total Man Hours'])
            estimatedcost = int(old_df['Total Cost'])
            estimatedcosttoclient = int(old_df['Total Cost To Client'])

            actualmanhours = int(opt_df['Total Man Hours Actual'])
            actualcost = int(opt_df['Total Cost Actual'])
            actualcosttoclient = int(opt_df['Total Cost to Client Actual'])

            totalmanhours_difference = actualmanhours - estimatedmanhours
            actualcost_difference = actualcost - estimatedcost
            costtoclient_difference = actualcosttoclient - estimatedcost
            
            st.metric(label="Total Man Hours Actual", value=actualmanhours, delta=totalmanhours_difference, delta_color="inverse")
            st.metric(label="Total Cost Actual", value=actualcost, delta=actualcost_difference, delta_color="inverse")
            st.metric(label="Total Cost to Client Actual", value=estimatedcosttoclient, delta=costtoclient_difference, delta_color="inverse")
