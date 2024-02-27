import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", layout="wide")
st.header("📊 Data Visualization: Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-20")

df = pd.read_csv("izev.csv", skipinitialspace=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

col1, col2 = st.columns(2)

# 2. Vehicle brands & model count (month and year)
with col1:
    st.write("Vehicle Make & Model Count")
    fig = px.sunburst(df, path=['Vehicle Make', 'Vehicle Model'])
    st.plotly_chart(fig)
    
with col2: 
    st.write("Type of Electric Vehicle: BEV, PHEV, FCEV")