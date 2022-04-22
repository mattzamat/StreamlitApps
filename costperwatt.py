from operator import mod
import streamlit as st
import pandas as pd
import base64

st.set_page_config(layout="wide")

def app():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Project Info')
        system_size = st.number_input(label="System Size", step=0.1)
        totalprojectcost = st.number_input(label="Total Project Cost", step=0.1)
        dealer_fee = st.number_input(label="Dealer Fee Percent", step=0.1)
        tax_percent = st.number_input(label="Project Tax Percent", step=0.1)
        next_step = False
        if ((system_size !=0) and (totalprojectcost !=0) and (dealer_fee !=0 and (tax_percent !=0))):
            next_step = True
            next_step = st.checkbox('Continue to Next Section')
        else:
            st.error('Please Input a Value in Each of the Boxes to Continue')
        
        
        if next_step:
            with col2:
                st.header('Variables')
                with st.form(key='calculate'):
                    module = st.number_input(label="Module", step=0.1)
                    shipping = st.number_input(label="Shipping", step=1)
                    inverter = st.number_input(label="Inverter", step=1)
                    monitoring = st.number_input(label="Monitoring", step=1)
                    ac_wiring = st.number_input(label="AC Wiring", step=1)
                    racking = st.number_input(label="Racking", step=1)
                    concrete_roofing = st.number_input(label="Concrete and Roofing", step=1)
                    mainpanel = st.number_input(label="Main Panel Upgrade", step=1)
                    travel = st.number_input(label="Travel", step=1)
                    battery = st.number_input(label="Battery", step=1)
                    electrical_eng = st.number_input(label="Elecrtrical Engineering", step=1)
                    mechanical_eng = st.number_input(label="Mechanical Engineering", step=1)
                    sales_comission = st.number_input(label="Sales-Commissions", step=1)
                    misc = st.number_input(label="Misc", step=1)
                    spare = st.number_input(label="Spare", step=1)
                    
                    calculate = st.form_submit_button(label='Calculate!')

                    if calculate:
                        with col3:
                            st.header('Returned Percentages')
                            total_watt = (totalprojectcost/system_size/1000)
                            dealerfee_watt = (dealer_fee/100)*total_watt
                            tax_watt = ((totalprojectcost*tax_percent)/100)/10000
                            costforproject_watt = total_watt + dealerfee_watt + tax_watt

                            module_metric = (module/costforproject_watt)*100
                            ship_metric = (shipping/costforproject_watt)*100
                            inverter_metric = (inverter/costforproject_watt)*100
                            monitoring_metric = (monitoring/costforproject_watt)*100
                            ac_wiring_metric = (ac_wiring/costforproject_watt)*100
                            racking_metric = (racking/costforproject_watt)*100
                            concreate_roofing_mertric = (concrete_roofing/costforproject_watt)*100
                            mainpanel_metric = (mainpanel/costforproject_watt)*100
                            travel_metric = (travel/costforproject_watt)*100
                            battery_metric = (battery/costforproject_watt)*100
                            electrical_eng_metric = (electrical_eng/costforproject_watt)*100
                            mechanical_eng_metric = (mechanical_eng/costforproject_watt)*100
                            sales_comission_metric = (sales_comission/costforproject_watt)*100
                            misc_metric = (misc/costforproject_watt)*100
                            spare_metric = (spare/costforproject_watt)*100
                            
                            st.metric(label='Module', value=module_metric)
                            st.metric(label='Shipping', value=ship_metric)
                            st.metric(label='Inverter', value=inverter_metric)
                            st.metric(label='Monitoring', value=monitoring_metric)
                            st.metric(label='AC Wiring', value=ac_wiring_metric)
                            st.metric(label='Racking', value=racking_metric)
                            st.metric(label='Concrete Roofing', value=concreate_roofing_mertric)
                            st.metric(label='Main Panel', value=mainpanel_metric)
                            st.metric(label="Travel", value=travel_metric)
                            st.metric(label='Battery', value=battery_metric)
                            st.metric(label='Electrical Eng', value=electrical_eng_metric)
                            st.metric(label='Mechanical Eng', value=mechanical_eng_metric)
                            st.metric(label='Sales Commission', value=sales_comission_metric)
                            st.metric(label='Misc', value=misc_metric)
                            st.metric(label='Spare', value=spare_metric)

                            opt = {
                                "Module Cost": module,
                                "Shipping Cost": shipping,
                                "Inverter Cost": inverter,
                                "Monitoring Cost": monitoring,
                                "AC Wiring Cost": ac_wiring,
                                "Racking Cost": racking,
                                "Concrete Cost": concrete_roofing,
                                "Main Panel Cost": mainpanel,
                                "Travel Cost": travel,
                                "Battery Cost": battery,
                                "Electrical Eng Cost": electrical_eng,
                                "Mechanical Eng Cost": mechanical_eng,
                                "Sales Comission Price": sales_comission,
                                "Misc Cost": misc,
                                "Spare Cost": spare,
                                "Module Metric": module_metric,
                                "Shipping Metric": ship_metric,
                                "Inverter Metric": inverter_metric,
                                "Monitoring Metric": monitoring_metric,
                                "AC Wiring Metric": ac_wiring_metric,
                                "Racking Metric": racking_metric,
                                "Concrete Metric": concreate_roofing_mertric,
                                "Main Panel Metric": mainpanel_metric,
                                "Travel Metric": travel_metric,
                                "Battery Metric": battery_metric,
                                "Electrical Eng Metric": electrical_eng_metric,
                                "Mechanical Eng Metric": mechanical_eng_metric,
                                "Sales Comission Metric": sales_comission_metric,
                                "Misc Metric": misc_metric,
                                "Spare Metric": spare_metric, 
                            }

                            opt_df = pd.DataFrame([opt])
                            csv = opt_df.to_csv(index=False)
                            b64 = base64.b64encode(csv.encode()).decode()
                            st.download_button(label='Download Results to CSV', data=b64)

app()