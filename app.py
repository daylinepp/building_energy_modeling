import streamlit as st
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import os
from datetime import datetime
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly

import pickle


st.set_page_config(layout="wide") # or "centered"

st.title("Building Energy Modeling")
st.header("Consumption Forecasting & System Analysis")
st.markdown("Web App by [Daylin Epp](https://www.linkedin.com/in/daylin-epp-62989760/)")
st.write("---")
st.markdown("")
st.markdown("Please visit the project repository for more information ")

# Prophet Forecasting
##################################################################################
# load preprocessed dataframes for forecasting scenarios
df_uni = pd.read_csv('raw_data/univariate_forecast.csv')
df_multi = pd.read_csv('raw_data/multivariate_forecast.csv')
# make sure dates are correct dtype
df_uni['ds'] = pd.to_datetime(df_uni['ds'])
df_multi['ds'] = pd.to_datetime(df_multi['ds'])

# train/test split
# done in univariate case for consistency
test_uni = df_uni[(df_uni['ds'] >= '2021-05-25 00:00:00')]     # last week of data (168 hours)
train_uni = df_uni[(df_uni['ds'] < '2021-05-25 00:00:00')]
# must be done in multivariate case so that added regressor date is available for forecast
test_multi = df_multi[(df_multi['ds'] >= '2021-05-25 00:00:00')]     # last week of data (168 hours)
train_multi = df_multi[(df_multi['ds'] < '2021-05-25 00:00:00')]

CONS_UNI = 'Univariate Forecast'
CONS_MULTI = ' Multivariate Forecast'

# Prophet Forecasting Model

# will need to add a cache to improve load times once each option has been run
#@st.cache(allow_output_mutation=True)
def make_forecast(selection):

    if selection == CONS_UNI:
        title = "Univariate Consumption Forecast"
        axis_label = "Energy Use (kWh)"
        df_prophet = train_uni
        extra_regressor = False
        
    if selection == CONS_MULTI:
        title = "Multivariate Consumption Forecast including Outside Air Temperature & Demand"
        axis_label = "Energy Use (kWh)"
        df_prophet = train_multi
        extra_regressor = True

    m = Prophet(interval_width=0.9)
    if extra_regressor:
        m.add_regressor('demand')
        m.add_regressor('temp thresh')

    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=len(test_uni), freq='H')
    if extra_regressor:
        future['demand'] = df_multi['demand']
        future['temp thresh'] = df_multi['temp thresh']

    forecast = m.predict(future)

    fig_forecast = plot_plotly(m, forecast)
    fig_forecast.update_layout(title=title, yaxis_title=axis_label, xaxis_title="Date")
    fig_components = plot_components_plotly(m, forecast)

    return fig_forecast, fig_components

st.header("Energy Consumption Forecast")
st.markdown("This tool is capable of forecasting hourly building energy consumption. It has been trained on data from June 1, 2020 to May 25, 2021."
            " The forecasting window provides data for the final week of May.")
st.markdown("""
Interpretting the graphs below:
* Use the time period selection boxes at the top left of the graph to change the field of view
* Hover your cursor over the graph to read specific observation values
    * Black points are actual values
    * Dark blue line is forecast predictions
    * Light blue area is 90% confidence interval
""")
st.markdown("Notice there is *significant improvement* in how the forecast fits the actual data in the multivariate case.")
st.markdown("")

selected_case = st.selectbox("Select Forecast Type:", (CONS_UNI, CONS_MULTI))
plotly_fig, plotly_components = make_forecast(selected_case)
st.plotly_chart(plotly_fig)
st.markdown("The graphs below break down the components of the forecasting curve."
            " They highlight the overall trend, weekly seasonality, and daily seasonality of energy consumption.")
st.plotly_chart(plotly_components)

# Predictive Modeling
##################################################################################
model = pickle.load(open("lgb_model_v2.sav", "rb"))

def prediction(Point_34, Point_17, Point_37, Point_21, 
               Point_194, Point_26, Point_22, Point_9, 
               Point_13, Point_23, Point_90, Point_198, Point_10):

    df = pd.DataFrame([{'Point_34': Point_34, 
                        'Point_17': Point_17, 
                        'Point_37': Point_37, 
                        'Point_21': Point_21, 
                        'Point_194': Point_194, 
                        'Point_26': Point_26, 
                        'Point_22': Point_22, 
                        'Point_9': Point_9, 
                        'Point_13': Point_13, 
                        'Point_23': Point_23, 
                        'Point_90': Point_90, 
                        'Point_198': Point_198, 
                        'Point_10': Point_10}])
    
    pred = model.predict(df)
    return pred

st.header("Energy Consumption Prediction")
st.markdown("Now you can try out the model by setting values for each feature."
            "")

Point_90 = st.slider('Average Outside Air Temp', -2.0, 33.0, 10.0, 0.5)
Point_21 = st.slider('Mixed Air Temp', 10.0, 40.0, 20.0, 0.5)
Point_22 = st.slider('Min Room Error', -10.0, 10.0, 0.0, 0.5)
Point_37 = st.slider('Supply Air Temp', 9.0, 33.0, 18.0, 0.5)
Point_26 = st.slider('Max Room Temp', 19.0, 35.0, 25.0, 0.5)
Point_17 = st.slider('Total Flow', 0.0, 7475.0, 3000.0, 25.0)
Point_194 = st.slider('Make Up Air Unit 1 Supply Temp', 12.0, 34.0, 22.0, 0.5)
Point_198 = st.slider('Make Up Air Unit 2 Supply Temp', 12.0, 34.0, 22.0, 0.5)
Point_13 = st.slider('Duct Pressure Point', 0.0, 480.0, 200.0, 10.0)
Point_23 = st.slider('Min Room Temp', 14.0, 27.0, 21.0, 0.5)
Point_34 = st.slider('Set Point', 10.0, 33.0, 20.0, 0.5)
Point_9 = st.slider('Return Carbon Dioxide', 390.0, 730.0, 450.0, 10.0)
Point_10  = st.selectbox('Air Handling Unit Supply Fan',("ON","OFF"))

if st.button('Make Hourly Energy Consumption Prediction'):
    result = prediction(Point_34, Point_17, Point_37, Point_21, 
                        Point_194, Point_26, Point_22, Point_9, 
                        Point_13, Point_23, Point_90, Point_198, Point_10)
    consumption = round(result[0], 1)
    try:
        st.write(consumption, 'kWh')
    except:
        pass