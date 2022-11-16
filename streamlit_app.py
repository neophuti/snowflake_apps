import streamlit
import pandas
import requests

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favourites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')

streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')

streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Load fruits file into dataframe
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Set index to the name of the fruit
my_fruit_list = my_fruit_list.set_index("Fruit")

#Pick list for choosing which fruits the customer wnats to include in their smoothie and prepopulate
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

#Load selected fruits into dataframe
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display fruits table
streamlit.dataframe(fruits_to_show)

#Call Fuityvice service, get fruit
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#Display fruit
streamlit.text(fruityvice_response)




