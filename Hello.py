# streamlit_app.py

import streamlit as st
from st_aggrid import AgGrid

select_all = '''
  SELECT 
    kinopoisk_id,
    imdb_id,
    name_ru,
    name_en,
    name_orig,
    film_type,
    film_year, 
    ARRAY(select jsonb_array_elements(countries::jsonb) ->> 'country') as country,
    ARRAY(select jsonb_array_elements(genres::jsonb) ->> 'genre') as genre,
    rating_kinopoisk,
    rating_imdb,
    poster_url,
    poster_url_preview
  FROM films
  LIMIT 500;
'''

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query(select_all, ttl="1m").reset_index(drop=True)

option = st.selectbox(
   "Movies of what country to show? (not active)",
   ("Email", "Home phone", "Mobile phone"),
   index=None,
   placeholder="Select country...",
)

# uniq_countries = [i for sublst in df['country'].unique() for i in sublst] 

# country = st.select("Choose country", list(df.index), uniq_countries)
# if not country:
#     st.error("Please select at least one country.")
# else:
#     data = df.loc[df['country'].str.contains(country)]
#     st.write("### Currenty available movies", data.sort_index())
st.write("### Currenty available movies")
AgGrid(df)
