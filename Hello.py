# streamlit_app.py

import streamlit as st
from st_aggrid import AgGrid

from scripts import select_all

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query(select_all, ttl="1m").reset_index(drop=True)

option = st.selectbox(
   "Movies of what country to show?",
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

AgGrid(df)
