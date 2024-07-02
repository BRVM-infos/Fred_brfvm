import pandas as pd
import os
os.system("") 
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
import re

import etat_financier, acceuil


   
################################
# Page configuration
st.set_page_config(
    page_icon= "🌍",
    layout="wide", 
    page_title= "BRVM",  
    initial_sidebar_state="expanded")
#radial-gradient(#263882 16%, #29063c 40%, #09152f 55%, #0b0344 70%, #120a57 85%)
###################################
# fixe theme
dark = '''
<style>
    .stApp {
 
   background: #e5dcdc;
    }
</style>
'''
st.markdown(dark, unsafe_allow_html=True)
##  background-color: #0c0a1a;
# Use a global variable to store the current theme
#st.session_state.theme = "dark"

####################################
#st.header("BRVM") TO HIDDE FOOTER RUNNINF    #MainMenu {visibility: hidden;}
#TO HIDDE FOOTER RUNNINF   
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 



############## Data Preparation ###################
# Read csv file
#df_main = pd.read_csv('output.csv')
df_main = pd.read_csv('output_4.csv')


# Extract unique countries and Sector
ticket = df_main['Ticket']
country_uemoa = df_main['Secteur'].unique()
company = df_main['Company_Name'].unique()

# Create a dictionary to map each country in UEMOA to its list of unique companie
pays_company_dict = {}
for _, row in df_main.iterrows():
    pays = row['Secteur']
    company_name = row['Company_Name']
    if pays not in pays_company_dict:
        pays_company_dict[pays] = set()  # Use set to automatically handle duplicates
    pays_company_dict[pays].add(company_name)

# Convert sets to lists in the dictionary
country = {key: list(value) for key, value in pays_company_dict.items()}


# Sidebar - Country and Company Selection
countries = country_uemoa




#####################################   
###Create class for multipl Page
class MultiApp:
    def __init_(self):
       self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
     })
    
    def run():

    # horizontal Menu
        app = option_menu(None, ["Acceuil",'Ratios Financier', 'Trends'], 
        icons=['house-fill', 'heart-pulse-fill', 'fire'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "5!important" },
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"color":"black","font-size": "16px","font-family": "Helvetica", "font-weight": "bold", "text-align": "center", 
        "margin":"0px", "--hover-color": "#605f77"},
        "nav-link-selected": {"background-color": "#f3e696"}
        }
        )
    # navigat page to choosse
        if app == 'Acceuil':
            acceuil.app(df_main, countries)
        if app == 'Ratios Financier':
            etat_financier.app()
        
    run()



 
#####################################
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


