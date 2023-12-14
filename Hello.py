# streamlit_app.py

import streamlit as st
from st_aggrid import AgGrid

select_all = '''
  SELECT 
    kinopoisk_id,
    -- imdb_id,
    name_ru,
    name_orig,
    film_type,
    film_year, 
    ARRAY(select jsonb_array_elements(countries::jsonb) ->> 'country') as country,
    ARRAY(select jsonb_array_elements(genres::jsonb) ->> 'genre') as genre,
    rating_kinopoisk,
    rating_imdb,
    poster_url
  FROM movies
  LIMIT 100;
'''

counter = '''
SELECT 
   COUNT(DISTINCT kinopoisk_id) as counter 
FROM movies;
'''

countries = '''
SELECT DISTINCT 
   ARRAY(select jsonb_array_elements(countries::jsonb) ->> 'country') as country
FROM movies;
'''

genres = '''
SELECT DISTINCT 
   ARRAY(select jsonb_array_elements(genres::jsonb) ->> 'genre') as genre
FROM movies;
'''

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query(select_all, ttl="1m").reset_index(drop=True)
counter = conn.query(counter, ttl="1m").reset_index(drop=True)
countries = conn.query(countries, ttl="1m").reset_index(drop=True)
genres = conn.query(genres, ttl="1m").reset_index(drop=True)

uniq_countries = list(countries['country'].unique())
uniq_genres = list(genres['genre'].unique())
option_c = st.selectbox(
   "Movies of what country to show?",
   (uniq_countries),
   index=None,
   placeholder="Select country...",
)

option_g = st.selectbox(
   "Movies of what genre to show?",
   (uniq_genres),
   index=None,
   placeholder="Select genre...",
)

st.metric(label="Total movies", value=f"{counter.loc[0, 'counter']}")

st.write("#### Currenty available movies")
data = df
if option_c:
   data = data.loc[data['country'].apply(lambda x: True if option_c in str(x) else False)]

if option_g:
   data = data.loc[data['genre'].apply(lambda x: True if option_g in str(x) else False)]

if data.shape[0] > 0:
   AgGrid(data)
else:
   option_c = option_c or ''
   option_g = option_g or ''
   st.write("#### No movies for {option_c} and {option_g}")
