import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="iZEV Dashboard", layout="wide")
st.header("📊 Data Visualization: Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-23")

# Dataframe
df = pd.read_csv("izev.csv", skipinitialspace=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.columns = df.columns.str.strip()
df['Month and Year'] = pd.to_datetime(df['Month and Year'], format="%B %Y")
df = df.sort_values('Incentive Request Date')

# 1. Car count per province % Month and year
col11, col12, col13 = st.columns([1.5, 6, 1])
with col12: 
    print(df.columns)
    car_count_per_month = df['Month and Year'].value_counts().reset_index()
    car_count_per_month.columns = ['Month and Year', 'Number of Inventive Requests']
    df_aggregated = df.groupby(['Month and Year', 'Recipient Province / Territory']).size().reset_index(name='Number of Incentive Requests')
    print(df_aggregated.columns)
    fig = px.line(
        df_aggregated,
        title="Number of Incentive Requests per Province",
        x="Month and Year", 
        y="Number of Incentive Requests", 
        color="Recipient Province / Territory", 
        line_group="Recipient Province / Territory", 
        line_shape="spline", 
        render_mode="svg"
    )
    fig.update_layout(
    width=1000,  # Width in pixels
    height=600,  # Height in pixels
    )
    st.plotly_chart(fig)


# 2. Vehicle brands & model count (month and year)
st.divider()
col21, col22, col23 = st.columns([1, 4, 4])
with col22:
    fig = px.sunburst(
        df, 
        title="Vehicle Make and Models for each",
        path=['Vehicle Make', 'Vehicle Model']
    )
    st.plotly_chart(fig)
    
with col23: 
    fig = px.sunburst(
        df,
        title="Types of Electric Vehicle: BEV, PHEV, FCEV",
        path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 'Vehicle Make']
    )
    st.plotly_chart(fig)
    
# 3. Incentive amount count (focus on 2500 and 5000)
st.divider()
col31, col32, col33 = st.columns([1.5, 6, 1])
with col32: 
    df['Eligible Incentive Amount'] = df['Eligible Incentive Amount'].str.replace(',', '')
    df['Eligible Incentive Amount'] = pd.to_numeric(df['Eligible Incentive Amount'])
    # Binning
    bins = [0, 2500, 5000]
    labels = ['low to medium', 'medium to high']

    # Create a new column 'Incentive Amount' based on binning
    df['Eligible Incentive Amounts'] = pd.cut(df['Eligible Incentive Amount'], bins=bins, labels=labels, include_lowest=True)

    fig = px.treemap(df, title="Eligible Incentive Amounts",
                    path=[px.Constant('All Vehicles'), 
                          'Eligible Incentive Amounts',
                          'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)',
                          'Vehicle Make', 
                          ], 
                    values='Eligible Incentive Amount',
                    color_continuous_scale='RdBu',
                    )
    
    fig.update_layout(
    width=1000,
    height=600,
    )
    st.plotly_chart(fig)