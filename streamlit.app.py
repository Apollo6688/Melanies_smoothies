# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

import requests    
moothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response) 

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


title = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be:",title)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose up to five ingredients:"
    , my_dataframe
    ,max_selections = 5
)

if ingredients_list:
    
    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + title+ """')"""
    

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button ('Submit_order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

   
