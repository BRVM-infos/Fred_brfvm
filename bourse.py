import pandas as pd
import os
os.system("") 
import streamlit as st

import streamlit_shadcn_ui as ui
#import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

    
################################
# Page configuration
st.set_page_config(
    page_icon= "🌍",
    layout="wide", 
    page_title= "BRVM",  
    initial_sidebar_state="expanded")

#####################################   
from streamlit_option_menu import option_menu
# horizontal Menu
app = option_menu(None, ["Acceuil", "Tendances", "Dividende", 'Etats Financier', 'Contact'], 
icons=['house', 'fire', "calculator-fill", 'graph-up-arrow', 'person-vcard-fill'], 
menu_icon="cast", default_index=0, orientation="horizontal")
#app

####################################
#st.header("BRVM") TO HIDDE FOOTER RUNNINF    #MainMenu {visibility: hidden;}
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 
 
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


# Read csv file
df_main = pd.read_csv('brvm_data.csv')

# Extract unique countries and companies
country_uemoa = df_main['Pays'].unique()
company = df_main['Company_Name'].unique()

# Create a dictionary to map each country in UEMOA to its list of unique companies
pays_company_dict = {}
for _, row in df_main.iterrows():
    pays = row['Pays']
    company_name = row['Company_Name']
    if pays not in pays_company_dict:
        pays_company_dict[pays] = set()  # Use set to automatically handle duplicates
    pays_company_dict[pays].add(company_name)

# Convert sets to lists in the dictionary
country = {key: list(value) for key, value in pays_company_dict.items()}

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
        marker=dict(color='orange', size=20),  # Adjust marker size here
        line=dict(color='grey'),  # Adjust line color if needed
        name='Dividende'
    ))
    fig.update_layout(
        #title=f'Dividende en FCFA ',
        title = {'text': "Dividende net", 
                            'font': {'color': 'lightgrey', 'size': 18} },
        xaxis_title='Date',
        yaxis_title='Prix FCFA',
        template='plotly_white',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Plot area background color
        paper_bgcolor='rgba(0, 0, 0, 0.1)' # Overall background color
    )
    return fig

def plot_benefice(stock_data, company):
    colors = ['red' if val < 0 else 'green' for val in stock_data['Resultat_net']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stock_data['Date'],
        y=stock_data['Resultat_net'],
        marker_color=colors
    ))
    fig.update_layout(
      #  title=f'Bénéfice net',
       title = {'text': "Bénéfice net", 
                            'font': {'color': 'lightgrey', 'size': 18} },
        xaxis_title='Date',
        yaxis_title='Million Fcfa',
        template='plotly_white',
         plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Plot area background color
        paper_bgcolor='rgba(0, 0, 0, 0.1)' # Overall background color
    )
    return fig

#************Side bar, main task of Appp*******

# Sidebar - Country and Company Selection
countries = country_uemoa

selected_country = st.sidebar.selectbox('Pays', countries)

if selected_country:
    companies = df_main[df_main['Pays'] == selected_country]['Company_Name'].unique()
    selected_company = st.sidebar.selectbox('Entreprises' , companies)

    st.markdown(f"""
                 <div class="pays">  {selected_company}  </div> """,
                   unsafe_allow_html=True)

    if selected_company:
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
                          #    metric card
                cart_pays=  df_main[df_main['Company_Name'] == selected_company]['Pays'].unique()[0]
                st.markdown(f"""
                        <div class="pays">{cart_pays} </div> """,
                          unsafe_allow_html=True)
                with st.expander('A Propos', expanded=True):
                
                     # Display description content
                     resume =  df_main[df_main['Company_Name'] == selected_company]['Description'].unique()[0]
                     st.markdown(f"""
                        <div class="resume">{resume} </div> """,
                          unsafe_allow_html=True)
           

st.set_option('deprecation.showPyplotGlobalUse', False)




