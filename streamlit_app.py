# Import python packages
from snowflake.snowpark.functions import col
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
#Title

st.markdown(
    "<h1 style='white-space: nowrap;'>🥤 Customize Your Smoothie! 🥤</h1>",
    unsafe_allow_html=True
)

#sub-title

st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

#add Streamlit Input Widget SELECTBOX

# option = st.selectbox('What is your favorite fruit?', ('Banana', 'Strawberries', 'Peaches'))

# st.write('You selected:', option)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:' ,my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders
                    (ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
