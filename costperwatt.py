from operator import mod
import streamlit as st
import pandas as pd
import base64
from millify import millify

st.set_page_config(layout="wide")

with st.container():
    st.header('Enter Project Info')

with st.container():
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col3:
        system_size = st.number_input(label="System Size", step=0.1)
    with col4:
        totalprojectcost = st.number_input(label="Total Project Cost", step=0.1)
    with col5:
        dealer_fee = st.number_input(label="Dealer Fee Percent", step=0.1)
    with col6:
        tax_percent = st.number_input(label="Project Tax Percent", step=0.1)
    with col1:
        next_step = False
        if ((system_size !=0) and (totalprojectcost !=0) and (dealer_fee !=0 and (tax_percent !=0))):
            next_step = True
            #next_step = st.checkbox('Continue to Next Section')
            total_watt = (totalprojectcost/system_size/1000)
            dealerfee_watt = (dealer_fee/100)*total_watt
            tax_watt = ((totalprojectcost*tax_percent)/100)/10000
            costforproject_watt = total_watt + dealerfee_watt + tax_watt
        else:
            st.error('Please Input a Value in Each of the Boxes to Continue')
        
with st.container():
    if next_step:
        st.header('Enter Project Costs')

with st.container():
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    if next_step:
        with col1:
            module = st.number_input(label="Module", step=0.1)
            module_metric = (module/costforproject_watt)*100
            st.metric(label='Module', value = millify(module_metric, precision=2))

            travel = st.number_input(label="Travel", step=0.1)
            travel_metric = (travel/costforproject_watt)*100
            st.metric(label="Travel", value=millify(travel_metric, precision=2))

        with col2:
            shipping = st.number_input(label="Shipping", step=0.1)
            ship_metric = (shipping/costforproject_watt)*100
            st.metric(label='Shipping', value=millify(ship_metric, precision=2))
            
            battery = st.number_input(label="Battery", step=0.1)
            battery_metric = (battery/costforproject_watt)*100
            st.metric(label='Battery', value=millify(battery_metric, precision=2))
        
        with col3:
            inverter = st.number_input(label="Inverter", step=0.1)
            inverter_metric = (inverter/costforproject_watt)*100
            st.metric(label='Inverter', value=millify(inverter_metric, precision=2))

            electrical_eng = st.number_input(label="Elecrtrical Engineering", step=0.1)
            electrical_eng_metric = (electrical_eng/costforproject_watt)*100
            st.metric(label='Electrical Eng', value=millify(electrical_eng_metric, precision=2))
        
        with col4:  
            monitoring = st.number_input(label="Monitoring", step=0.1)
            monitoring_metric = (monitoring/costforproject_watt)*100
            st.metric(label='Monitoring', value=millify(monitoring_metric, precision=2))
        
            mechanical_eng = st.number_input(label="Mechanical Engineering", step=0.1)
            mechanical_eng_metric = (mechanical_eng/costforproject_watt)*100
            st.metric(label='Mechanical Eng', value=millify(mechanical_eng_metric, precision=2))
        
        with col5:   
            ac_wiring = st.number_input(label="AC Wiring", step=0.1)
            ac_wiring_metric = (ac_wiring/costforproject_watt)*100
            st.metric(label='AC Wiring', value=millify(ac_wiring_metric, precision=2))

            sales_comission = st.number_input(label="Sales-Commissions", step=0.1)
            sales_comission_metric = (sales_comission/costforproject_watt)*100
            st.metric(label='Sales Commission', value=millify(sales_comission_metric, precision=2))

        with col6: 
            racking = st.number_input(label="Racking", step=0.1)
            racking_metric = (racking/costforproject_watt)*100
            st.metric(label='Racking', value=millify(racking_metric, precision=2))
        
            misc = st.number_input(label="Misc", step=0.1)
            misc_metric = (misc/costforproject_watt)*100
            st.metric(label='Misc', value=millify(misc_metric, precision=2))

        with col7:  
            concrete_roofing = st.number_input(label="Concrete and Roofing", step=0.1)
            concreate_roofing_mertric = (concrete_roofing/costforproject_watt)*100
            st.metric(label='Concrete Roofing', value=millify(concreate_roofing_mertric, precision=2))
            
            spare1 = st.number_input(label="Spare 1", step=0.1)
            spare_metric1 = (spare1/costforproject_watt)*100
            st.metric(label='Spare 1', value=millify(spare_metric1, precision=2))
       
