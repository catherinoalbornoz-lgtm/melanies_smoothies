import streamlit as st
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie!")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Conexión con Snowflake
conn = st.connection("snowflake")
session = conn.session()

# Obtener frutas desde Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

# Convertir los resultados a una lista
fruit_rows = my_dataframe.collect()

fruit_list = [
    row["FRUIT_NAME"]
    for row in fruit_rows
]

# Elegir ingredientes
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Nombre de la persona
name_on_order = st.text_input(
    "Name on order:"
)

# Construir lista de ingredientes
if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)

    # SQL para insertar pedido
    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (INGREDIENTS, NAME_ON_ORDER)
        VALUES
            ('""" + ingredients_string + """','""" + name_on_order + """')
    """

# Botón
time_to_insert = st.button("Submit Order")

if time_to_insert:

    if ingredients_list and name_on_order:

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )

    elif not name_on_order:

        st.warning(
            "Please enter your name."
        )

    else:

        st.warning(
            "Please choose at least one ingredient."
        )
