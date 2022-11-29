import streamlit as st
import pandas as pd 
import numpy as np
import streamlit as st
import plotly.express as px
import datetime
from datetime import date, time, datetime, timedelta
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
from PIL import Image
a1,a2 = st.columns(2)
with a1:
    st.title ("Police Department Incident Reports")
    st.markdown('2018 to Present')
with a2:
    image = Image.open('San_Francisco_Police_logo.png')
    st.image(image)
    
df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')

df1=df.drop(['SF Find Neighborhoods','Current Police Districts','Current Supervisor Districts','Analysis Neighborhoods','HSOC Zones as of 2018-06-05','OWED Public Spaces','Central Market/Tenderloin Boundary Polygon - Updated','Parks Alliance CPSI (27+TL sites)','ESNCAG - Boundary File','Areas of Vulnerability, 2016'], axis=1)

df1.dropna(axis=1,thresh=0, inplace= True)
df1.dropna(axis=0,thresh=0, inplace= True)

Year = df['Incident Year'].unique().tolist()
Dia=df['Incident Day of Week'].unique().tolist()

Years = st.multiselect('Year: ',Year,default = Year)
dias = st.multiselect('Day of the week: ',Dia,default = Dia)

mask = (df['Incident Year'].isin(Years))&(df['Incident Day of Week'].isin(dias))


df = df[mask]

mapa=pd.DataFrame()
mapa['lat']=df['Latitude']
mapa['lon']=df['Longitude']
mapa=mapa.dropna()
st.map(mapa)

b1,b2 = st.columns(2)
with b1:
    fig=plt.figure(figsize=(30,20))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Incident Time'].sort_values().unique(), y=df.groupby(['Incident Time']).count()['Row ID'], name='Cases per hour', line=dict(color='#003785', width=4)))
    fig.update_layout(xaxis_title='Hour', yaxis_title='Cases')
    fig.update_layout(title = 'Hourly Crimes')
    st.plotly_chart(fig, use_container_width=True)
    
with b2:
    fig2=px.pie(df, values=df.groupby(['Resolution']).count()['Row ID'], names=df['Resolution'].unique(),color_discrete_sequence =['#003785','#1465bb','#2196f3','#81c9fa'], hole=.3)
    fig2.update_layout(title = 'Resolution of the case')
    st.plotly_chart(fig2, use_container_width=True)

c1,c2 = st.columns(2)
with c1:
    fig3=px.bar(df, x=df.groupby(['Incident Day of Week']).count()['Row ID'], y=df['Incident Day of Week'].unique(),color = df['Incident Day of Week'].unique(), color_discrete_sequence =['#003785','#1465bb','#2196f3','#81c9fa','#6aa9e9','#98c3ed','#afcdea'], height=500)
    fig3.update_layout(xaxis_title='Cases', yaxis_title='Day')
    fig3.update_layout(title = 'Crimes by Day of the Week')
    st.plotly_chart(fig3, use_container_width=True)
    

with c2:
    fig4=px.bar(df, y=df.groupby(['Incident Year']).count()['Row ID'], x=df['Incident Year'].sort_values().unique(),color=df.groupby(['Incident Year']).count()['Row ID'],color_discrete_sequence =['#003785','#1465bb','#2196f3'], height=500)
    fig4.update_layout(xaxis_title='Year', yaxis_title='Cases')
    fig4.update_layout(title = 'Total Crimes by Year')
    st.plotly_chart(fig4, use_container_width=True)


st.markdown('In this board we can see graphs of the chrism behavior in the different districts, in what we could divide it into year, day and if these cases in which resolution ended, as well as what are the most dangerous hours. This information helps people who are from San Francisco or who plan to move to the city to take these parameters into account and understand the behavior of criminals.')

st.markdown('We can see in the time graph how the cases dropped in 2022, they are unfounded cases, it could be due to police suspicions about some criminal act that had to be reported to be on the record.We can also see that the peak time for cases is at 12 in the morning, since it is an hour less supervised and there may be more opportunities for robbery or assault')
