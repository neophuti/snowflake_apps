import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#New Section to display fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
    else:
    #streamlit.write('The user entered, ', fruit_choice)

    #Call Fuityvice service, get fruit
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

    #Take the JSON response and normalise it
    fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())

    #Display normalised data
    streamlit.dataframe(fruityvice_normalised)
except URLError as e:
  streamlit.error()

#Don't run this section of the code while troubleshooting
streamlit.stop()


#Connection to Snowflake and required statements to return data from a database
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

my_cur = my_cnx.cursor()

my_sql_select = "SELECT * FROM FRUIT_LOAD_LIST"

my_cur.execute(my_sql_select)

my_data_rows = my_cur.fetchall()

streamlit.header("The fruit load list contains:")

streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')

streamlit.write('Thanks for adding ', add_my_fruit)

my_sql_insert = "INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')"

my_cur.execute(my_sql_insert)












