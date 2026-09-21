import streamlit as st
import os

from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie!")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Crear conexión con Snowflake
conn = st.connection("snowflake")
session = conn.session()

# Obtener frutas desde la tabla
my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(col("FRUIT_NAME"))

# Convertir FRUIT_NAME a lista
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

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)

    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS)
        VALUES ('""" + ingredients_string + """','"""+name_on_order+"""')
    """

    st.write(my_insert_stmt)
    st.stop()

time_to_insert = st.button("Submit Order")



if time_to_insert:
    if ingredients_list:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
    else:
        st.warning("Please choose at least one ingredient.")
