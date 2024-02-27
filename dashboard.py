import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="iZEV Dashboard", layout="wide")
st.header("📊 Data Visualization: Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-23")

df = pd.read_csv("izev.csv", skipinitialspace=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.columns = df.columns.str.strip()
# df = df.sort_values('Incentive Request Date')

# 1. Car count per province % Month and year
col11, col12, col13 = st.columns([2, 6, 1])
with col12: 
    print(df.columns)
    car_count_per_month = df['Month and Year'].value_counts().reset_index()
    car_count_per_month.columns = ['Month and Year', 'Number of Vehicles']
    df_aggregated = df.groupby(['Month and Year', 'Recipient Province / Territory']).size().reset_index(name='Number of Vehicles')
    print(df_aggregated.columns)
    fig = px.line(
        df_aggregated,
        title="Number of Vehicles per Province",
        x="Month and Year", 
        y="Number of Vehicles", 
        color="Recipient Province / Territory", 
        line_group="Recipient Province / Territory", 
        line_shape="spline", 
        render_mode="svg"
    )
    # fig = px.line(
    #     df,
    #     car_count_per_month,
    #     x="Incentive Request Date", 
    #     y="Number of Vehicles", 
    #     color="Recipient Province / Territory", 
    #     line_group="Recipient Province / Territory", 
    #     line_shape="spline", 
    #     render_mode="svg"
    # )
    st.plotly_chart(fig)


# 2. Vehicle brands & model count (month and year)
col21, col22 = st.columns(2)
with col21:
    fig = px.sunburst(
        df, 
        title="Vehicle Make & Model Count",
        path=['Vehicle Make', 'Vehicle Model']
    )
    st.plotly_chart(fig)
    
with col22: 
    fig = px.sunburst(
        df,
        title="Types of Electric Vehicle: BEV, PHEV, FCEV",
        path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 'Vehicle Make']
    )
    st.plotly_chart(fig)