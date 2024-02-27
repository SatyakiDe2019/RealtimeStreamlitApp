#############################################################
#### Written By: SATYAKI DE                              ####
#### Written On: 17-Dec-2023                             ####
#### Modified On 26-Feb-2024                             ####
####                                                     ####
#### Objective: This is the main calling                 ####
#### python script that will invoke the                  ####
#### main class, which will contextualize the source     ####
#### files & then read the data into pandas dataframe,   ####
#### and then dynamically create the Streamlit-app       ####
#### based Dashboard, which will show all the KPIs.      ####
####                                                     ####
#############################################################

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

import streamlit as st
import streamlit_echarts as ste
import random
import time
import pandas as pd
import numpy as np
import asyncio
import plotly.graph_objs as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
# Main Class to consume streaming
import clsStreamConsume as ca

# Create the instance of the Covid API Class
x1 = ca.clsStreamConsume()

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

fileDBPath = cf.conf['DB_PATH']
DBFileName = cf.conf['DB_FILE_NM']
debugInd = cf.conf['DEBUG_IND']

var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print('*' *60)
DInd = 'Y'

# Initialize a dataframe to store historical data
dataHistory = pd.DataFrame(columns=["Temperature", "Humidity", "Pressure"])
df_conv = pd.DataFrame()
########################################################
################  End Of Global Area   #################
########################################################

def toPositive(row, flag):
    try:
        x_val = ''

        if flag == 'ServoMeter':
            x_val = abs(float(row['ServoMotor'])) * 5 * np.random.uniform(20, 40.5)
        elif flag == 'DCMotor':
            x_val = abs(float(row['DCMotor'])) * 0.001 * np.random.uniform(40, 60)

        return x_val

    except Exception as e:
        x = str(e)
        print(x)

        val = 0

        return val

def toPositiveInflated(row, flag):
    try:
        x_val = ''

        if flag == 'ServoMeter':
            x_val = abs(float(row['ServoMeter'])) * 10 * np.random.uniform(20, 30)
        elif flag == 'DCMeter':
            x_val = abs(float(row['DCMeter'])) * 10 * np.random.uniform(20, 30.5)

        return x_val

    except Exception as e:
        x = str(e)
        print(x)

        val = 0

        return val

def getStream():
    try:
        cnt = 0

        while True:
            asyncio.sleep(1)
            df = x1.conStream(var1, DInd)

            if cnt == 0:
                df_conv = df
            else:
                d_frames = [df_conv, df]
                df_conv = pd.concat(d_frames)

            cnt += 1

            print('Iteration : ', str(cnt))
            print('*' *200)

            df = pd.DataFrame()

            return df_conv
    except:
        df = pd.DataFrame()

        return df

def getData(var, Ind):
    try:
        # Let's pass this to our map section
        df = getStream()

        nRange = df.shape[0]

        df['ServoMeterNew'] = df.apply(lambda row: toPositiveInflated(row, 'ServoMeter'), axis=1)
        df['ServoMotorNew'] = df.apply(lambda row: toPositive(row, 'ServoMeter'), axis=1)
        df['DCMotor'] = df.apply(lambda row: toPositiveInflated(row, 'DCMeter'), axis=1)
        df['DCMeterNew'] = df.apply(lambda row: toPositive(row, 'DCMeter'), axis=1)
        df['Timestamp'] = pd.date_range(start="2024-01-01", periods=nRange, freq='h')

        #Rename New Columns to Old Columns
        df.rename(columns={'ServoMeterNew':'Temperature'}, inplace=True)
        df.rename(columns={'ServoMotorNew':'Humidity'}, inplace=True)
        df.rename(columns={'DCMotor':'Pressure'}, inplace=True)

        df2 = df[['Temperature', 'Humidity', 'Pressure', 'Timestamp']]

        return df2
    except Exception as e:
        x = str(e)
        print(x)

        df2 = pd.DataFrame()

        return df2

def createHumidityGauge(humidity_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = humidity_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Humidity", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'cyan'},
                {'range': [50, 100], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': humidity_value}
        }
    ))

    fig.update_layout(height=220, paper_bgcolor = "white", font = {'color': "darkblue", 'family': "Arial"}, margin=dict(t=0, l=5, r=5, b=0))

    return fig

def createTempGauge(temparature_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = temparature_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temperature", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'cyan'},
                {'range': [50, 100], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': temparature_value}
        }
    ))

    fig.update_layout(height=220, paper_bgcolor = "white", font = {'color': "darkblue", 'family': "Arial"}, margin=dict(t=0, l=5, r=5, b=0))

    return fig

def createPressureGauge(pressure_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pressure_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Pressure", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'cyan'},
                {'range': [50, 100], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': pressure_value}
        }
    ))

    fig.update_layout(height=220, paper_bgcolor = "white", font = {'color': "darkblue", 'family': "Arial"}, margin=dict(t=0, l=5, r=5, b=0))

    return fig

def createTemperatureLineChart(data):
    # Assuming 'data' is a DataFrame with a 'Timestamp' index and a 'Temperature' column
    fig = px.line(data, x=data.index, y='Temperature', title='Temperature Vs Time')
    fig.update_layout(height=270)  # Specify the desired height here
    return fig

def createHumidityLineChart(data):
    # Assuming 'data' is a DataFrame with a 'Timestamp' index and a 'Temperature' column
    fig = px.line(data, x=data.index, y='Humidity', title='Humidity Vs Time')
    fig.update_layout(height=270)  # Specify the desired height here
    return fig

def createPressureLineChart(data):
    # Assuming 'data' is a DataFrame with a 'Timestamp' index and a 'Temperature' column
    fig = px.line(data, x=data.index, y='Pressure', title='Pressure Vs Time')
    fig.update_layout(height=270)  # Specify the desired height here
    return fig

def main():
    # Custom CSS to make the sidebar narrower
    st.markdown(
        """
        <style>
            .css-1d391kg {
                width: 30px;  /* Adjust the width as needed */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("KPIs")
    selected_kpis = st.sidebar.multiselect(
        "Select KPIs", options=["Temperature", "Humidity", "Pressure"], default=["Temperature"]
    )

    # Split the layout into columns for KPIs and graphs
    gauge_col, kpi_col, graph_col = st.columns(3)

    # Auto-refresh setup
    st_autorefresh(interval=7000, key='data_refresh')

    # Fetching real-time data
    data = getData(var1, DInd)

    st.markdown(
        """
        <style>
        .stEcharts { margin-bottom: -50px; }  /* Class might differ, inspect the HTML to find the correct class name */
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display gauges at the top of the page
    gauges = st.container()

    with gauges:
        col1, col2, col3 = st.columns(3)
        with col1:
            humidity_value = round(data['Humidity'].iloc[-1], 2)
            humidity_gauge_fig = createHumidityGauge(humidity_value)
            st.plotly_chart(humidity_gauge_fig, use_container_width=True)

        with col2:
            temp_value = round(data['Temperature'].iloc[-1], 2)
            temp_gauge_fig = createTempGauge(temp_value)
            st.plotly_chart(temp_gauge_fig, use_container_width=True)

        with col3:
            pressure_value = round(data['Pressure'].iloc[-1], 2)
            pressure_gauge_fig = createPressureGauge(pressure_value)
            st.plotly_chart(pressure_gauge_fig, use_container_width=True)


    # Next row for actual readings and charts side-by-side
    readings_charts = st.container()


    # Display KPIs and their trends
    with readings_charts:
        readings_col, graph_col = st.columns([1, 2])

        with readings_col:
            st.subheader("Latest Readings")
            if "Temperature" in selected_kpis:
                st.metric("Temperature", f"{temp_value:.2f}%")

            if "Humidity" in selected_kpis:
                st.metric("Humidity", f"{humidity_value:.2f}%")

            if "Pressure" in selected_kpis:
                st.metric("Pressure", f"{pressure_value:.2f}%")


        # Graph placeholders for each KPI
        with graph_col:
            if "Temperature" in selected_kpis:
                temperature_fig = createTemperatureLineChart(data.set_index("Timestamp"))

                # Display the Plotly chart in Streamlit with specified dimensions
                st.plotly_chart(temperature_fig, use_container_width=True)

            if "Humidity" in selected_kpis:
                humidity_fig = createHumidityLineChart(data.set_index("Timestamp"))

                # Display the Plotly chart in Streamlit with specified dimensions
                st.plotly_chart(humidity_fig, use_container_width=True)

            if "Pressure" in selected_kpis:
                pressure_fig = createPressureLineChart(data.set_index("Timestamp"))

                # Display the Plotly chart in Streamlit with specified dimensions
                st.plotly_chart(pressure_fig, use_container_width=True)


if __name__ == "__main__":
    main()
