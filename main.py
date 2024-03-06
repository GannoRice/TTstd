import pandas as pd
import streamlit as st
import plotly_express as px
import numpy as np

#importing the cleaned version of the document
df = pd.read_csv('vehicles_clean.csv')

#Title
st.header('Vehicle data analysis project:')
st.header('Data viewer:')
st.dataframe(df)


# histogram with check boxes displaying the relative prices of vehicle types

st.header('Compare price distribution the types of vehicles and their price')
# get a list of car types and order them
types_listed = sorted(df['type'].unique())
# select drop down 1
type_1 = st.selectbox(
                              label='Select Vehicle Type',
                              options=types_listed,
                              index=types_listed.index('SUV')
                              )
# Drop down 2
type_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=types_listed,
                              index=types_listed.index('sedan')
                              )
# filter mask
mask_filter = (df['type'] == type_1) | (df['type'] == type_2)
df_filtered = df[mask_filter]

# normalise checkbox
normalize = st.checkbox('Normalize graph', value=True)
if normalize:
    hist_norm = 'percent'
else:
    hist_norm = None

# create a plotly histogram figure
type_hist = px.histogram(
                      df_filtered,
                      x='price',
                      nbins=30,
                      color= 'type',
                      histnorm=hist_norm,
                      barmode='overlay'
                      )
# display the figure with streamlit
st.write(type_hist)


#Bar graph showing the average prices for each vehicle type

st.header('Average prices of different vehicle types')

#get average prices 
def average_price(col,row):

    data = {'type': row, 'average_price': col}
    df_av = pd.DataFrame(data= data)
    df_av = df_av.groupby('type').mean()

    return df_av

df_av = average_price(df['price'], df['type'])

df_av = df_av.reset_index().sort_values(by= 'average_price').reset_index().drop(columns={'index'})

#create bar graph
type_bar = px.bar(
                 df_av,
                 color= 'type'
                 )

type_bar.update_traces(
                             marker_line_width = 0,
                             selector=dict(type="bar")
                  )
type_bar.update_layout(
                             bargap=0,
                             bargroupgap = 0,
                             title = "Average price for different vehicle types",
                             yaxis_title = "Average price",
                             xaxis_title = "Type of vehicle"       
                 )    

st.write(type_bar)



#Scatter graph
st.header('Scatter graph comparing the relationship between price and how many miles each type has done')

# remove high mileage vehicles that skew the graph
def remove_outliers(col):
    sorted(col)
    q1,q3 = col.quantile([0.25,0.75])
    IQR = q3-q1
    lbound = q1 - (1.5*IQR)
    ubound = q3 + (1.5*IQR)
    return lbound, ubound

# compare the values between the price, odometer
df_scat = df
low,high = remove_outliers(df_scat['price'])

df_scat['price'] = np.where(df_scat['price']> high,high,df_scat['price'])
df_scat['price'] = np.where(df_scat['price']< low,low,df_scat['price'])


df_scat = df_scat.query('0 < odometer < 600000')

#create scatter plot
pco_scat = px.scatter(
                df_scat,
                x= "odometer", 
                y= "price", 
                color= "type",                
    )
    
st.write(pco_scat)