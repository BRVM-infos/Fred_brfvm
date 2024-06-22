import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import streamlit as st


def extract_data_from_class():
       # Fetch HTML content
       url = "https://www.sikafinance.com/marches/cotation_BOAC.ci"
        response = requests.get(url)
          # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        class_name = 'cot1u'  
        
        elements = soup.find_all(class_=class_name)

        return [element.text.strip() for element in elements]

