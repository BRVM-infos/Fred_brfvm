import streamlit as st
import pandas as pd



from all_functions import plot_PER, filter_ratio

df_main = pd.read_csv('output_4.csv')
sector = df_main['Secteur'].unique()
def app():


    col = st.columns([0.2, 0.8], gap='medium')  

    with col[0]:
      selected_sector = st.selectbox('Secteur', sector)
    #plot_PER()
   
      if selected_sector:
        companies = df_main[df_main['Secteur'] == selected_sector]['Company_Name'].unique()
        selected_company = st.selectbox('Entreprises' , companies)
        
        

   
        