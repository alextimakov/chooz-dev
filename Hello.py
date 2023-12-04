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

counter = '''
SELECT COUNT(DISTINCT kinopoisk_id) as counter FROM films;
'''

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query(select_all, ttl="1m").reset_index(drop=True)
counter = conn.query(counter, ttl="1m").reset_index(drop=True)

uniq_countries = set([i for sublst in df['country'].values for i in sublst])
option = st.selectbox(
   "Movies of what country to show? (not active)",
   (uniq_countries),
   index=None,
   placeholder="Select country...",
)


# if not country:
#     st.error("Please select at least one country.")
# else:
#     data = df.loc[df['country'].str.contains(country)]
#     st.write("### Currenty available movies", data.sort_index())
st.metric(label="Total movies", value=f"{counter.loc[0, 'counter']}")

st.write("### Currenty available movies")
if option:
   data = df.loc[df['country'].apply(lambda x: True if option in str(x) else False)]
   if data.shape[0] > 0:
      AgGrid(data)
   else:
      st.write("#### No movies for {option}") 
else:
   AgGrid(df)
