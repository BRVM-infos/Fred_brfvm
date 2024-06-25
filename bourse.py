import pandas as pd
import os
os.system("") 
import requests
import re
import streamlit as st
from bs4 import BeautifulSoup

import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go

    
################################
# Page configuration
st.set_page_config(
    page_icon= "🌍",
    layout="wide", 
    page_title= "BRVM",  
    initial_sidebar_state="expanded")
###################################
# fixe theme
dark = '''
<style>
    .stApp {
   background: radial-gradient(#263882 16%, #29063c 40%, #09152f 55%, #0b0344 70%, #120a57 85%);
    }
</style>
'''
st.markdown(dark, unsafe_allow_html=True)

# Use a global variable to store the current theme
st.session_state.theme = "dark"
#####################################   
from streamlit_option_menu import option_menu
# horizontal Menu
app = option_menu(None, ["Acceuil", "Tendances", 'Etats Financier'], 
        icons=['house', 'fire', 'graph-up-arrow'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"color":"white","font-size": "16px", "text-align": "center", 
        "margin":"0px", "--hover-color": "#605f77"},
        "nav-link-selected": {"background-color": "#9f047e"}
        }
        )

####################################
#TO HIDDE FOOTER RUNNINF   
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 
 
#####################################

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
#######################################################################
# Read csv file and preapare the data
#df_main = pd.read_csv('output.csv')
df_main = pd.read_csv('output_1.csv')

# Extract unique countries and companies
country_uemoa = df_main['Pays'].unique()
company = df_main['Company_Name'].unique()

# Create a dictionary to map each country in UEMOA to its list of unique companies
pays_company_dict = {}
for _, row in df_main.iterrows():
    pays = row['Pays']
    company_name = row['Company_Name']
    if pays not in pays_company_dict:
        pays_company_dict[pays] = set()  
    pays_company_dict[pays].add(company_name)

# Convert sets to lists in the dictionary
country = {key: list(value) for key, value in pays_company_dict.items()}
####################################################################################
#******************* Définir les fonction graphiques*************

def filter_data(df, country, company):
    filtered_df = df[(df['Pays'] == country) & (df['Company_Name'] == company)]
    return filtered_df
    
def plot_dividende(stock_data, company):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=stock_data['Date'], 
        y=stock_data['Dividende'], 
        mode='lines+markers', 
        marker=dict(color='orange', size=20),  
        line=dict(color='grey'),  
        name='Dividende'
    ))
    fig.update_layout(
        title = {'text': "Dividende net (Fcfa)", 
                            'font': {'color': 'lightgrey', 'size': 18} },
        xaxis=dict(fixedrange=True),  
        yaxis=dict(fixedrange=True ), 
        template='plotly_white',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',  
        paper_bgcolor='rgba(0, 0, 0, 0.1)',
        height=350,  
        margin=dict(l=10, r=20, t=50, b=20), 
    )
    return fig

def plot_benefice(stock_data, company):
    colors = ['red' if val < 0 else 'green' for val in stock_data['Resultat_net']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=(2019, 2020, 2021, 2022, 2023),
        y=stock_data['Resultat_net'],
        marker_color=colors
    ))
    # Customize the x-axis to show all categories
    fig.update_xaxes(
        tick0=0,
        dtick=1 ) #
    fig.update_layout(
       title = {'text': "Bénéfice net (Million Fcfa)", 
                            'font': {'color': 'lightgrey', 'size': 18} },
        xaxis=dict(fixedrange=True),  
        yaxis=dict(fixedrange=True ),
        template='plotly_white',
         plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0.1)',
        height=350,  
        margin=dict(l=10, r=20, t=50, b=20),  
    )
    return fig
# Function help, to get real time action price of company !!!
def price(url):
        
    # Fetch HTML content
           response = requests.get(url)
          # Parse HTML content
           soup = BeautifulSoup(response.text, 'html.parser')
           class_name = 'cot1u'  
         # Extract data from the specified HTML class
           elements = soup.find_all(class_=class_name)

           return  [element.text.strip() for element in elements][0].split(" ")[0].replace('XOF', '')
############################################################################
#************Side bar, main task of Appp*******

# Sidebar - Country and Company Selection
countries = country_uemoa

selected_country = st.sidebar.selectbox('Pays', countries)

if selected_country:

    companies = df_main[df_main['Pays'] == selected_country]['Company_Name'].unique()
    selected_company = st.sidebar.selectbox('Entreprises' , companies)
    with st.sidebar :
        
        st.caption("""La BRVM (Bourse Régionale des Valeurs Mobilières) est une plateforme dynamique
                    où les investisseurs découvrent des opportunités uniques pour capitaliser sur 
                   la croissance économique et l innovation en Afrique de l Ouest""")
        st.divider()
        st.sidebar.markdown('''<a href="https://www.linkedin.com/in/alfred-diokou/" target="_blank"
                             class="sidebar-caption"><i class="fab fa-linkedin linkedin-icon">
                            </i> Alfred Diokou</a>''', unsafe_allow_html=True)


    if selected_company:
        
        web = "https://www.sikafinance.com/marches/cotation_"
        car = df_main[df_main['Company_Name'] == selected_company]['Ticket'].unique()[0]
        url = web + car
        action = price(url)
        rapport = df_main[df_main['Company_Name'] == selected_company]['Trismestre'].unique()[0]
        # Display company name  with this price action
        st.markdown(f"""
          <div class="inline-div-container">
            <div class="inline-div"> {selected_company} </br> ({selected_country}) </div>
            <div class="action">Action  <br/> {action} Fcfa </div>
            <div class="action_1">Profit net T1 2024 </br> {rapport} </div>
          </div>""",
             unsafe_allow_html=True)
        
        # Column Division
        cols = st.columns([0.8, 0.2], gap='medium') 
        filtered_data = filter_data(df_main, selected_country, selected_company)
        
        with cols[0] :
            
             # Create columns for side-by-side charts
            col1, col2 = st.columns(2)

            # Plot line chart in the first column
            with col1:
              fig1 = plot_dividende(filtered_data, selected_company)
              st.plotly_chart(fig1)

            # Plot bar chart in the second column
            with col2:
              fig2 = plot_benefice(filtered_data, selected_company)
              st.plotly_chart(fig2)
        
        with cols[1] :
                  
                
                with st.expander('A Propos', expanded=True):
                
                     # Display description content
                     resume =  df_main[df_main['Company_Name'] == selected_company]['Description'].unique()[0]
                     st.caption(f"""
                        <div class="resume">{resume} </div> """,
                          unsafe_allow_html=True)
           

st.set_option('deprecation.showPyplotGlobalUse', False)




