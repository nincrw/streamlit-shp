import streamlit as st

st.title('Interactive Dashboard')
st.sidebar.title('Traffic')

st.markdown('Interactive Dashboard 🔥')
st.sidebar.markdown('Traffic 🔥')

file_name = 'Tweets.csv'

# Read CSV
@st.cache(persist=True)
def read_data():
	data = pd.read_csv(data_path + '\\' + file_name)
	data['tweet_created'] = pd.to_datetime(data['tweet_created'])
	return data

data = read_data()

st.write(data)
