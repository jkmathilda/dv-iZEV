import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="iZEV Dashboard", layout="wide")
st.header("📊 Data Visualization: Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-20")

df = pd.read_csv("izev.csv", skipinitialspace=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

col1, col2 = st.columns(2)

# 2. Vehicle brands & model count (month and year)
with col1:
    fig = px.sunburst(df, 
                      title="Vehicle Make & Model Count",
                      path=['Vehicle Make', 'Vehicle Model'])
    st.plotly_chart(fig)
    
with col2: 
    st.write("Types of Electric Vehicle: BEV, PHEV, FCEV")
    fig = px.sunburst(df,
                      path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 'Vehicle Make'])
    st.plotly_chart(fig)