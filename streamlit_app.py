# Import python packages
from snowflake.snowpark.functions import col
import streamlit as st
import requests
import pandas as pd

# Write directly to the app
# Title

st.markdown(
    "<h1 style='white-space: nowrap;'>🥤 Customize Your Smoothie! 🥤</h1>",
    unsafe_allow_html=True
)

# Sub-title

st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Snowflake connection

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Create pandas dataframe
pd_df = my_dataframe.to_pandas()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe.select("FRUIT_NAME").to_pandas()["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        # Get SEARCH_ON value
        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.subheader(
            fruit_chosen + ' Nutrition Information'
        )

        # Call SmoothieFroot API using SEARCH_ON
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        st_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    # Insert order into Snowflake

    my_insert_stmt = """INSERT INTO smoothies.public.orders
                    (ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
