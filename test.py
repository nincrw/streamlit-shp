import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# import os
import base64
# from io import BytesIO

st.title('Sentiment of US Airlines Tweets')
st.sidebar.title('Sentiment of US Airlines Tweets')

st.markdown('Interactive db to analyze the sentiment of Tweets 🐦')
st.sidebar.markdown('Interactive db to analyze the sentiment of Tweets 🐦')

# data_path = r'C:\Users\ni.wathanyusakul\Downloads\PC\Dashboard'
file_name = 'Tweets.csv'

# Read CSV
@st.cache(persist=True)
def read_data():
# 	data = pd.read_csv(data_path + '\\' + file_name)
	data = pd.read_csv('\\' + file_name)
	data['tweet_created'] = pd.to_datetime(data['tweet_created'])
	return data

data = read_data()

# Random tweet
st.sidebar.subheader('Show random tweet')
random_tweet = st.sidebar.radio('Sentiment', ('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Visualization Type',['Histogram', 'Pie Chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

# Bar & Pie chart
if not st.sidebar.checkbox('Hide', True):
	st.markdown('### Number of tweets by sentiment')
	if select == 'Histogram':
		fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=300)
		st.plotly_chart(fig)
	else:
		fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
		st.plotly_chart(fig)

# Slider
st.sidebar.subheader('When and where are users tweeting from?')
# hour = st.sidebar.number_input('Hour of day', min_value=0, max_value=23)
hour = st.sidebar.slider('Hour of day', 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

# def to_excel(df):
# 	output = BytesIO()
# 	writer = pd.ExcelWriter(output, engine='xlsxwriter')
# 	df.to_excel(writer, index = False, sheet_name='Sheet1')
# 	workbook  = writer.book
# 	worksheet = writer.sheets['Sheet1']
# 	format1 = workbook.add_format({'num_format': '0.00'}) # Tried with '0%' and '#,##0.00' also.
# 	worksheet.set_column('A:A', None, format1) # Say Data are in column A
# 	writer.save()
# 	processed_data = output.getvalue()
# 	return processed_data

# def get_table_download_link(df):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     # val = df.to_csv()
#     val = to_excel(df)
#     b64 = base64.b64encode(val)  # val looks like b'...'
#     return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Your_File.xlsx">Download Excel file</a>' # decode b'abc' => abc

def get_table_download_link_csv(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
    return href

# location / map
if not st.sidebar.checkbox('Close', True, key='1'):
# if not st.sidebar.checkbox('Close', True):
	st.markdown('### Tweet locations based on time of day')
	# st.markdown('%i tweets between %i.00 and %i.00' % (len(modified_data), hour, hour+1))
	st.markdown('%i tweets between %i.00 and %i.00' % (len(modified_data), hour, (hour+1)%24))
	st.map(modified_data)

	# show raw data
	if st.sidebar.checkbox('Show data', False):
		st.write(modified_data)
		# download xlsx
		# st.markdown(get_table_download_link(modified_data[['tweet_id','airline','text']]), unsafe_allow_html=True)
		# download csv
		st.markdown(get_table_download_link_csv(modified_data), unsafe_allow_html=True)

# Multi filter option
st.sidebar.subheader('Breakdown airline tweets by sentiment')
airline_list = data['airline'].unique()
choice = st.sidebar.multiselect('Pick Airlines', airline_list, key='0')

if len(choice) > 0:
	choice_data = data[data.airline.isin(choice)]
	fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment'
		, histfunc='count', color='airline_sentiment', facet_col='airline_sentiment'
		, labels={'airline_sentiment':'tweets'}, height=500, width=700)
	st.plotly_chart(fig_choice)

# Word cloud
st.sidebar.header('Word Cloud')
word_sentiment = st.sidebar.radio('Sentiment word cloud', ('positive','neutral','negative'))

if not st.sidebar.checkbox('Hide', True, key='3'):
	st.header('Word cloud for %s sentiment' % (word_sentiment))
	df = data[data['airline_sentiment'] == word_sentiment]
	words = ' '.join(df['text'])
	processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
	word_cloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
	plt.imshow(word_cloud)
	plt.xticks([])
	plt.yticks([])
	# st.set_option('deprecation.showPyplotGlobalUse', False)
	st.pyplot()
