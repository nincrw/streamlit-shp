import streamlit as st
import pandas as pd
import numpy as np 

st.title('Interactive Dashboard')
st.sidebar.title('Traffic')

st.markdown('Interactive Dashboard 🔥')
st.sidebar.markdown('Traffic 🔥')

file_name = 'Tweets.csv'

# Read CSV
@st.cache(persist=True)
def read_data():
# 	data = pd.read_csv('https://github.com/nincrw/streamlit-shp/blob/main/' + file_name)
	data = pd.read_csv('https://raw.githubusercontent.com/nincrw/streamlit-shp/main/' + file_name)
	data['tweet_created'] = pd.to_datetime(data['tweet_created'])
	return data

data = read_data()

# Random tweet
st.sidebar.subheader('Show random tweet')
random_tweet = st.sidebar.radio('Sentiment', ('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

# st.write(data)
