import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie!")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Conexión con Snowflake
conn = st.connection("snowflake")
session = conn.session()

# Obtener frutas desde Snowflake
my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(col("FRUIT_NAME"))

fruit_rows = my_dataframe.collect()

fruit_list = [
    row["FRUIT_NAME"]
    for row in fruit_rows
]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# API SmoothieFroot
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.text(smoothiefroot_response.json())
