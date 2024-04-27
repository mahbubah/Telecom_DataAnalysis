import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Tellco Data", layout="wide")

# cache the result so that it doesn't load everytime
#@st.cache()
def loadData():
    df = pd.read_csv('data/clean_data.csv')
    df['Total Avg RTT (ms)'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
    df['Total Avg Bearer TP (kbps)'] = df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)']
    df['Total TCP Retrans. Vol (Bytes)'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']
    df['Total Data Volume (Bytes)'] = df['Total UL (Bytes)'] + df['Total DL (Bytes)']
    df['Social Media Data Volume (Bytes)'] = df['Social Media UL (Bytes)'] + df['Social Media DL (Bytes)']
    df['Google Data Volume (Bytes)'] = df['Google UL (Bytes)'] + df['Google DL (Bytes)']
    df['Email Data Volume (Bytes)'] = df['Email UL (Bytes)'] + df['Email DL (Bytes)']
    df['Youtube Data Volume (Bytes)'] = df['Youtube UL (Bytes)'] + df['Youtube DL (Bytes)']
    df['Netflix Data Volume (Bytes)'] = df['Netflix UL (Bytes)'] + df['Netflix DL (Bytes)']
    df['Gaming Data Volume (Bytes)'] = df['Gaming UL (Bytes)'] + df['Gaming DL (Bytes)']
    df['Other Data Volume (Bytes)'] = df['Other UL (Bytes)'] + df['Other DL (Bytes)']

    df = df[[
        'Bearer Id',
        'Dur. (ms)',
        'IMSI',
        'MSISDN/Number',
        'IMEI',
        'Total Avg RTT (ms)',
        'Total Avg Bearer TP (kbps)',
        'Total TCP Retrans. Vol (Bytes)',
        'Handset Manufacturer',
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)',
        'Total Data Volume (Bytes)']]

    return df

def displayHandsetsInfo(df):
    st.title("Handsets of Users")
    st.write("")
    plotly_plot_treemap(df)
    st.write("")
    st.markdown("***Handset manufacturers with more than 200 devices.***")
    plotly_plot_pie(df, 'Handset Manufacturer', 200)
    st.write("")
    st.markdown("**Handset types with more than 1000 devices.**")
    plotly_plot_pie(df, 'Handset Type', 1000)


def displayApplicationsInfo(df):
    st.title("Usage of applications")
    st.write("")
    st.markdown("**Total data used per application**")
    apps = df[['Social Media Data Volume (Bytes)',
    'Google Data Volume (Bytes)',
    'Email Data Volume (Bytes)',
    'Youtube Data Volume (Bytes)',
    'Netflix Data Volume (Bytes)',
    'Gaming Data Volume (Bytes)',
    'Other Data Volume (Bytes)']].copy(deep=True)
    apps.rename(columns={
        'Social Media Data Volume (Bytes)': 'Social Media',
        'Google Data Volume (Bytes)': 'Google',
        'Email Data Volume (Bytes)': 'Email',
        'Youtube Data Volume (Bytes)': 'Youtube',
        'Netflix Data Volume (Bytes)': 'Netflix',
        'Gaming Data Volume (Bytes)': 'Gaming',
        'Other Data Volume (Bytes)': 'Other'},
        inplace=True)
    total = apps.sum()
    total = total.to_frame('Data volume')
    total.reset_index(inplace=True)
    total.rename(columns={'index': 'Applications'}, inplace=True)
    fig = px.pie(total, names='Applications', values='Data volume')
    st.plotly_chart(fig)
    app_handsets_df = df[[
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)']]
    app_handsets_df = app_handsets_df.groupby('Handset Type').sum()
    sort_df = app_handsets_df.sort_values('Gaming Data Volume (Bytes)').head()

def plotly_plot_pie(df, column, limit=None):
    a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
    a = a.sort_values("count", ascending=False)
    if limit:
        a.loc[a['count'] < limit, column] = f'Other {column}s'
    fig = px.pie(a, values='count', names=column, width=800, height=500)
    st.plotly_chart(fig)

def plotly_plot_treemap(df):
    fig = px.treemap(df, path=[px.Constant("Handset Manufacturers"), 'Handset Manufacturer', 'Handset Type'])
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig)


# because the data in the database doesn't change, we need to call loadData() only once
df= loadData()
st.sidebar.title("Pages")
choices = ["Handsets", "Applications"]
page = st.sidebar.selectbox("Choose Page",choices)

if page == "Handsets":
    displayHandsetsInfo(df)
    pass
elif page == "Applications":
    displayApplicationsInfo(df)

