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

def get_fruityvice_data(this_fruit_choice):
   #Call Fuityvice service, get fruit
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)

   #Take the JSON response and normalise it
   fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())
   
   return fruityvice_normalised
   

#New Section to display fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      #streamlit.write('The user entered, ', fruit_choice)
      
      #Call function
      back_from_function = get_fruityvice_data(fruit_choice)
      
      #Display normalised data
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()



streamlit.header("The fruit load list contains:")

#Connection to Snowflake and required statements to return data from a database
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_sql_select = "SELECT * FROM FRUIT_LOAD_LIST"
      my_cur.execute(my_sql_select)
      return my_cur.fetchall()
   
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


#Don't run this section of the code while troubleshooting
#streamlit.stop()

def insert_row_snowflake(new_fruit):
     my_sql_insert = "INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')"
     my_cur.execute(my_sql_insert)
     return "Thanks for adding " + new_fruit
   

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)














