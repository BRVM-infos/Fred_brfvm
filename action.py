import os
import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

# Function extrac action price from url and specific class "cotlu"
#This function can be extend with two variable (url, class)
def extract_data_from_class(url: str):  
        # Fetch HTML content
        response = requests.get(url)
       # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        class_name = 'cot1u'  # Replace with the actual class name
        # Extract data from the specified HTML class
        elements = soup.find_all(class_=class_name)
        return [element.text.strip() for element in elements][0].split(" ")[0].replace('XOF', '')

