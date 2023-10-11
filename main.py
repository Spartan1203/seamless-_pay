import pandas as pd
import streamlit as st
import plotly_express as px
import matplotlib.pyplot as plt
import folium
import io
#from st_files_connection import FilesConnection
#conn=st.expreimental_connection('gcs', type=FilesConnection)
st.set_page_config(page_title="Visa Visualizations",
                   page_icon=":bar_chart:",
                   layout="wide")
st.title(":blue[Exploratory Data Analysis of Visa Applications from Africa]")
f1_approved=pd.read_excel(
    io="dataset.xlsx",
    engine="openpyxl",
    sheet_name="f1_data",
    header=0,
    usecols="A:L")
b1b2=pd.read_excel(
    io="https://github.com/Spartan1203/seamless-_pay/blob/main/FYs97-22_NIVDetailTable%20(1).xlsx",
    engine="openpyxl",
    sheet_name="b1b2_data",
    header=0,
    usecols="A:K")
#st.dataframe(f1_approved)
#st.dataframe(b1b2)
st.sidebar.header("Filter countries:")
country= st.sidebar.multiselect(
    'select the country:',
    default=f1_approved['Countries'].unique(),
    options=f1_approved['Countries'].unique())
b1b2_approved=b1b2.loc[0:12,:]
b1b2_approved.set_index("Countries",inplace=True)
b1b2_approved=b1b2_approved.query("Countries == @country")
top_5_b1b2_applicants=b1b2.loc[15:19,:]
top_5_b1b2_applicants.set_index("Countries",inplace=True)
top_5_b1b2_applicants=top_5_b1b2_applicants.query("Countries == @country")
top_5_b1b2_acceptance_rates=b1b2.loc[22:26,:]
top_5_b1b2_acceptance_rates.set_index("Countries",inplace=True)
top_5_b1b2_acceptance_rates=top_5_b1b2_acceptance_rates.query("Countries == @country")
top_5_b1b2_refusal_rates=b1b2.loc[29:33,:]
top_5_b1b2_refusal_rates.set_index("Countries",inplace=True)
top_5_b1b2_refusal_rates=top_5_b1b2_refusal_rates.query("Countries == @country")
st.subheader("B1B2 Visa Approval Data for Africa: 2013-2022")
st.dataframe(b1b2_approved)
st.subheader("Top 5 B1B2 Applicants from Africa: 2013-2022")
st.dataframe(top_5_b1b2_applicants)
st.subheader("Top 5 B1B2 Visa Refusal Rates Data for Africa: 2013-2022")
st.dataframe(top_5_b1b2_refusal_rates)
st.subheader("Top 5 B1B2 Visa Acceptance Rates Data for Africa: 2013-2022")
st.dataframe(top_5_b1b2_acceptance_rates)
df_selection= f1_approved.query(
    "Countries == @country")
df_selection.set_index("Countries", inplace=True)
st.subheader("F1 Visa Refusal Rates Data for Africa: 2013-2022")
st.dataframe(df_selection)


st.title(":bar_chart: Visa Visuals")
st.markdown("##")
total_applications=df_selection['Total'].sum()
df_selection["Average_applications"]=df_selection.iloc[:,0:9].mean(axis=1)
average_applications=df_selection['Average_applications'].mean().astype('int')
right_column, left_column =st.columns(2)
with left_column:
    st.subheader('total applications:')
    st.subheader(f"{total_applications}")
with right_column:
    st.subheader('Average applications:')
    st.subheader(f"{average_applications}")
    st.markdown("---")


df_new_1=df_selection.drop(['Total','Average_applications'],axis=1)
df_new_1=df_new_1.query("Countries==@country")
#st.dataframe(df_new_1.T)
line_fig=px.line(df_new_1.T,
               title="<b>Visa Approvals: 2013-2022 for </b>" f'{country}',
               template="plotly_white")
line_fig.update_xaxes(title_text="year")
line_fig.update_yaxes(title_text="number of applicants")
line_fig.add_annotation(x='2020',ax=0,ay=-200,text="Pandemic")
st.subheader("Trend visualization of applications: 2013-2022")
st.plotly_chart(line_fig)
df_selection['Percentage']=(df_selection['Total']/total_applications)*100
df_new_2=df_selection[['Percentage']].query("Countries==@country")
st.dataframe(df_new_2)
pie_fig=px.pie(df_new_2,
               names=df_new_2.index,
               values='Percentage',
               labels=df_new_2.index,
               hole=.1
               )
pie_fig.update_traces(textposition='inside',textinfo='label+percent')
st.subheader("Pie Visualization of percentage number of applications per country")
st.plotly_chart(pie_fig)
bar_h=px.bar(df_new_2,x='Percentage',y=df_new_2.index)
st.subheader("Bar Visualization of percentage number of applications per country")
st.plotly_chart(bar_h)
