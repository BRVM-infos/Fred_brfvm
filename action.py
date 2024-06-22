import os
import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

# Set up css file via fucntion
# Function to load CSS from a file and inject it into the app
def load_css(file_name):
     if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style >{f.read()}</style>', unsafe_allow_html=True)
     else:
        st.error(f"CSS file '{file_name}' not found. Please check the file path.")

# Set the working directory to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
        

# Load the CSS file
load_css('style.css')

# Function extrac action price
def extract_data_from_class(url: str):
    
    
        # Fetch HTML content
        response = requests.get(url)

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        class_name = 'cot1u'  
        
        elements = soup.find_all(class_=class_name)

        return [element.text.strip() for element in elements]

