import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from all_functions import price, plot_benefice, plot_dividende, filter_data,ratio_chart, current_ratio, debt_ratio
from etat_financier import app




#************Side bar, main task of Appp*******

def app(df_main, selected_company, select_sector):
 
  ################# TITLE & INTRODUCTION App ############
  # Set the title of the Streamlit app
    st.markdown('<div class="title">Outil Pratique, Analyse des Entreprises Cotées dans BRVM</div>',
             unsafe_allow_html=True)
    
    ddd = st.columns([0.9,0.1])
    with ddd[1]:
         st.markdown(".......")
    dddd = st.columns([0.9,0.1])
    with dddd[0]:
         st.markdown(".......")
       
 
    if selected_company:
        #Price Action calculate of the select company
        web = "https://www.sikafinance.com/marches/cotation_"
        car = df_main[df_main['Company_Name'] == selected_company]['Ticket'].unique()[0]
        url = web + car
        action = price(url)
        rapport = df_main[df_main['Company_Name'] == selected_company]['Trismestre'].unique()[0]
        # Display Action price of select company
        # Column Division
        ol1, ol2, ol3 = st.columns(3)

        with ol1:
            selected_country = df_main[df_main['Company_Name'] == selected_company]['Pays'].unique()[0]
            st.markdown(f"""
                <div class="action"> {selected_company} </br> ({selected_country}) </div>
              """,
             unsafe_allow_html=True)
        with ol2:
           st.markdown(f"""
                <div class="action"> Action  <br/> {action} Fcfa </div>
              """,
             unsafe_allow_html=True)
        with ol3:
           st.markdown(f"""
                <div class="action"> Profit net T1 2024 </br> {rapport} </div>
              """,
             unsafe_allow_html=True)
        
        filtered_data = filter_data(df_main, select_sector, selected_company)
        fig1 = plot_benefice(filtered_data, selected_company)
        fig2 = plot_dividende(filtered_data, selected_company)
            
             # Create columns for side-by-side charts
        col1, col2 = st.columns(2)

            # Plot line chart in the first column
        with col1:
              
              st.plotly_chart(fig1)

             
        with col2:

            st.plotly_chart(fig2)
        dd = st.columns([0.5,0.5])
        with dd[0]:
           st.markdown("...")
        ##### RATIOS #############
        head = st.columns([0.3, 0.5,0.2], gap='medium')
       
        with head[1]:
          st.markdown('<div class="subheader">Les Ratios Financier (Indicateurs) </div>',
             unsafe_allow_html=True)
        bol = st.columns([0.1, 0.3, 0.1, 0.3], gap='medium')

        with bol[3] :
            val1 = df_main[df_main['Company_Name'] == selected_company]['debt_to_equity'].unique()[0].round(2)
            val1 = int(val1)
            if val1 == 0 :
              st.write("Disponile Bientôt")
            elif select_sector == 'Secteur' :
               debt_ratio(val1, 'Debt to Equity (D/E)')
            else:
               debt_ratio(val1, 'Debt to Equity (D/E)')

        
        with bol[1] :
            val3 = df_main[df_main['Company_Name'] == selected_company]['return_on_equity'].unique()[0].round(2)
            val3 = int(val3)
            if val3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ratio_chart(val3, 'Return on Equity (ROE)')
       
     
        bal = st.columns([0.1, 0.3, 0.1, 0.3], gap='medium')
      
        with bal[1] :
          
            vol1 = df_main[df_main['Company_Name'] == selected_company]['current_ratio'].unique()[0].round(2)
            vol1 = int(vol1)
            if vol1 == 0 :
              st.write("Disponile Bientôt")
            else:
              current_ratio(vol1, 'Current Ratio')
            
        with bal[3] :
            vol3 = df_main[df_main['Company_Name'] == selected_company]['return_on_asset'].unique()[0].round(2)
            vol3 = int(vol3)
            if vol3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ratio_chart(vol3, 'Return on Asset (ROA)')
    
           

      
                                 
        
  ##### Column Division : Chart of price action and table of history variation
 
      
      
      
        

st.set_option('deprecation.showPyplotGlobalUse', False)

 
    
        
