import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(page_title="iZEV Dashboard", layout="wide")
st.header("📊 Data Visualization: Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-23")

# Dataframe
df = pd.read_csv("izev.csv", skipinitialspace=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.columns = df.columns.str.strip()
df['Month and Year'] = pd.to_datetime(df['Month and Year'], format="%B %Y")
df = df.sort_values('Incentive Request Date')

# 1. Car count per province % Month and year
st.subheader("Number of Incentive Requests per Province")
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
st.subheader("Incentive Requests Ratio by Vehicle Make and Type of Electric Cars")
col21, col22 = st.columns(2)

with col21:
    year = st.selectbox(
        options=['Total', '2019', '2020', '2021', '2022', '2023'],
        label='Select Year:',
        key='year1'
    )
    df['Calendar Year'] = df['Calendar Year'].astype(str)
    if year == 'Total':
        fig = px.sunburst(
            df, 
            title="Vehicle Make and Models for each",
            path=['Vehicle Make', 'Vehicle Model']
        )
        st.plotly_chart(fig)
    else:
        yearly_df = df[df['Calendar Year'] == year]
        fig = px.sunburst(
            yearly_df, 
            title="Vehicle Make and Models for each in " + year,
            path=['Vehicle Make', 'Vehicle Model']
        )
        st.plotly_chart(fig)
    
with col22: 
    year = st.selectbox(
        options=['Total', '2019', '2020', '2021', '2022', '2023'],
        label='Select Year:',
        key='year2'
    )
    df['Calendar Year'] = df['Calendar Year'].astype(str)
    if year == 'Total':
        fig = px.sunburst(
            df,
            title="Types of Electric Vehicle: BEV, PHEV, FCEV",
            path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 'Vehicle Make']
        )
        st.plotly_chart(fig)
    else:
        yearly_df = df[df['Calendar Year'] == year]
        fig = px.sunburst(
            yearly_df,
            title="Types of Electric Vehicle in " + year + ": BEV, PHEV, FCEV",
            path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 'Vehicle Make']
        )
        st.plotly_chart(fig)
    
# 3. Incentive amount count (focus on 2500 and 5000)
st.divider()
st.subheader("Eligible Incentive Amounts")

col31, col32, col33 = st.columns([1.5, 6, 1])
with col32: 
    df['Eligible Incentive Amount'] = df['Eligible Incentive Amount'].str.replace(',', '')
    df['Eligible Incentive Amount'] = pd.to_numeric(df['Eligible Incentive Amount'])
    # # Binning
    # bins = [0, 2500, 5000]
    # labels = ['low to medium', 'medium to high']
    
    df['Eligible Incentive Amount'] = pd.to_numeric(df['Eligible Incentive Amount'], errors='coerce')
    df['Eligible Incentive Amounts'] = np.where(df['Eligible Incentive Amount'] <= 2500, 'low to medium', 'medium to high')

    df_count = df.groupby(['Eligible Incentive Amounts', 
                        'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 
                        'Vehicle Make']).size().reset_index(name='Count')

    df_avg_incentive = df.groupby(['Eligible Incentive Amounts', 
                                'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 
                                'Vehicle Make'])['Eligible Incentive Amount'].mean().reset_index(name='Average Incentive Amount')

    df_merged = pd.merge(df_count, df_avg_incentive, on=['Eligible Incentive Amounts', 
                                                        'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 
                                                        'Vehicle Make'])

    fig = px.treemap(df_merged, 
                    path=['Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 
                        'Vehicle Make'], 
                    values='Count',
                    color='Average Incentive Amount',
                    color_continuous_scale='RdBu',  
                    title='Treemap of Vehicles by Incentive Amount and Type')


    # Merge counts with averages
    # grouped_df = df.groupby(
    #     ['Eligible Incentive Amounts', 
    #      'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)', 
    #      'Vehicle Make']
    # )['Eligible Incentive Amount'].mean().reset_index()
        
    # fig = px.treemap(grouped_df, title="Eligible Incentive Amounts",
    #                 path=[px.Constant('All Vehicles'), 
    #                       'Eligible Incentive Amounts',
    #                       'Battery-Electric Vehicle (BEV), Plug-in Hybrid Electric Vehicle (PHEV) or Fuel Cell Electric Vehicle (FCEV)',
    #                       'Vehicle Make', 
    #                       ], 
    #                 values='Eligible Incentive Amount',
    #                 # color='Counts',
    #                 color_continuous_scale='Blues',
    #                 )
    
    fig.update_layout(
    width=1000,
    height=600,
    )
    st.plotly_chart(fig)