import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#read in the file
movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")

movies_data.info()

movies_data.duplicated()

movies_data.count()

movies_data.dropna()

st.write("""
Average Movie Budget, Grouped by Genre
""")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize = (19, 10))

plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average \
Budget of Movies in Each Genre')

st.pyplot(fig)

col1, col2 = st.columns(2)
col1.write('# This is Column 1')
col2.write('# This is Column 2')

st.write('### Columns of different sizes')
col1, col2, col3, col4 = st.columns([1,3,1,2])

col1.write('# This is Column 1')
col2.write('# This is Column 2')
col3.write('# This is Column 3')
col4.write('# This is Column 4')

# Creating sidebar widget unique values from our movies dataset
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = movies_data['year'].unique().tolist()

with st.sidebar:
    st.write("Select a range on the slider (it represents movie score) \
       to view the total number of movies in a genre that falls \
       within that range ")
    #create a slider to hold user scores
    new_score_rating = st.slider(label = "Choose a value:",
                                  min_value = 1.0,
                                  max_value = 10.0,
                                 value = (3.0,4.0))

#create a multiselect widget to display genre
new_genre_list = st.multiselect('Choose Genre:',
                                        genre_list, default = ['Animation',\
                                         'Horror',  'Fantasy', 'Romance'])
#create a selectbox option that holds all unique years
year = st.selectbox('Choose a Year',
    year_list, 0)

#Configure and filter the slider widget for interactivity
score_info = (movies_data['score'].between(*new_score_rating))

#Filter the selectbox and multiselect widget for interactivity
new_genre_year = (movies_data['genre'].isin(new_genre_list)) \
& (movies_data['year'] == year)

# visualization section
#group the columns needed for visualizations
col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    dataframe_genre_year = movies_data[new_genre_year]\
    .groupby(['name',  'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write("""#### User score of movies and their genre """)
    rating_count_year = movies_data[score_info]\
    .groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)