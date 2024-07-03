import streamlit as st
import pandas as pd
from all_functions import price, plot_benefice, plot_dividende, filter_data, history_variation





#************Side bar, main task of Appp*******

def app(df_main, sector):
 
  ################# TITLE & INTRODUCTION App ############
  # Set the title of the Streamlit app
  
  
  cols = st.columns([0.2,0.8], gap='large')
  with cols[0]:
    select_sector = st.selectbox('Secteur', sector)

    if select_sector:
      companies = df_main[df_main['Secteur'] == select_sector]['Company_Name'].unique()
      selected_company = st.selectbox('Entreprises' , companies)
      
       
  with cols[1]:  
    if selected_company:
        #Price Action calculate of the select company
        web = "https://www.sikafinance.com/marches/cotation_"
        car = df_main[df_main['Company_Name'] == selected_company]['Ticket'].unique()[0]
        url = web + car
        action = price(url)
        rapport = df_main[df_main['Company_Name'] == selected_company]['Trismestre'].unique()[0]
        # Display Action price of select company
        # Column Division
      

        
        filtered_data = filter_data(df_main, select_sector, selected_company)
        fig1 = plot_benefice(filtered_data, selected_company)
        fig2 = plot_dividende(filtered_data, selected_company)
            
             # Create columns for side-by-side charts
        col1, col2 = st.columns(2)

            # Plot line chart in the first column
    with col1:
              selected_country = df_main[df_main['Company_Name'] == selected_company]['Pays'].unique()[0]
              st.markdown(f"""
                <div class="action"> {selected_company} </br> ({selected_country}) </div>
              """,
             unsafe_allow_html=True)
              st.plotly_chart(fig1)

             
    with col2:
            
            st.markdown(f"""
           <div class="inline-div-container">
             <div class="action">Action  <br/> {action} Fcfa </div>
             <div class="action_1">Profit net T1 2024 </br> {rapport} </div>
           </div>""",
             unsafe_allow_html=True)

            st.plotly_chart(fig2)
                                 
  with cols[0] :
    with st.expander('A Propos', expanded=True):
                
                     # Display description content
                     resume =  df_main[df_main['Company_Name'] == selected_company]['Description'].unique()[0]
                     st.caption(f"""
                        <div class="resume">{resume} </div> """,
                          unsafe_allow_html=True)
  
  ##### Column Division : Chart of price action and table of history variation
 
      
      
      
        

st.set_option('deprecation.showPyplotGlobalUse', False)

 
    
        
