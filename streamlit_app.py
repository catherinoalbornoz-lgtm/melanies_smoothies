import streamlit as st
import requests
import pandas as pd
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
).select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)


#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert to snowpark dataframe to a pandas Dataframe so wecan use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

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
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )
