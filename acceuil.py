import streamlit as st
import pandas as pd
from math import ceil
import streamlit_shadcn_ui as ui
from all_functions import price, plot_benefice, plot_dividende, filter_data,ratio_chart, current_ratio, debt_ratio





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
          
        op = st.columns([0.37, 0.3])
        with op[0]:
        # Define the tab options
          options = ['Price Ratios','Liquidity Ratios', 'Leverage Ratios', 'Profitability Ratios']
          # Create the tabs
          selected_tab = ui.tabs(options=options, default_value='Price Ratios', key="kanaries")
         
        if selected_tab == 'Profitability Ratios':
         with st.container(height=300, border=False):
         
          bol = st.columns([0.3, 0.1,0.05, 0.3, 0.1], gap='small')
          
          with bol[2]:
             st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 3px solid rgba(49, 51, 63, 0.2);
                        height: 100px;
                        margin: auto;
                        
                    }
                </style>
            '''
                )
          with bol[3] :
          
            vo = df_main[df_main['Company_Name'] == selected_company]['profit_margin_ratio'].unique()[0]
          
            if vo == 0 :
              st.write("Disponile Bientôt")
            else:
              ratio_chart(vo, 'Profit Margin Ratio', 5, 15)
              
          with bol[0] :
            val3 = df_main[df_main['Company_Name'] == selected_company]['return_on_equity'].unique()[0].round(2)
            val3 = int(val3)
            if val3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ratio_chart(val3, 'Return on Equity (ROE)', 10, 20)
          # Chart Legend
          with bol[1]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
          with bol[4]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
        elif selected_tab == 'Liquidity Ratios':         
         with st.container(height=300, border=False):
          bal = st.columns([0.3, 0.1,0.05, 0.3, 0.1], gap='small')
          with bal[0] :
          
            vol1 = df_main[df_main['Company_Name'] == selected_company]['current_ratio'].unique()[0].round(2)
            vol1 = int(vol1)
            if vol1 == 0 :
              st.write("Disponile Bientôt")
            else:
              current_ratio(vol1, 'Current Ratio')
          with bal[2]:
             st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 3px solid rgba(49, 51, 63, 0.2);
                        height: 100px;
                        margin: auto;
                        
                    }
                </style>
            '''
                )
          with bal[3] :
            vol3 = df_main[df_main['Company_Name'] == selected_company]['return_on_asset'].unique()[0].round(2)
            vol3 = int(vol3)
            if vol3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ratio_chart(vol3, 'Return on Asset (ROA)', 5, 10)
          with bal[1]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
          with bal[4]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
        elif selected_tab == 'Price Ratios':         
         with st.container(height=300, border=False):
          bala = st.columns([0.3, 0.1,0.05, 0.3, 0.1], gap='small')
              
          with bala[3] :
            vo1 = df_main[df_main['Company_Name'] == selected_company]['price_earning_ratio'].unique()[0]  
            ratio_chart(vo1, 'Price Earning Ratio (PER)',15, 25)

          with bala[0] :
            div = list(df_main[df_main['Company_Name'] == selected_company]['Dividende'])[4]
            vo2 = ceil((div/float(action.replace('\xa0', '').replace(',', '.')))*100)
            ratio_chart(vo2, 'Dividende Yield',3, 5)
          with bala[2]:
             st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 3px solid rgba(49, 51, 63, 0.2);
                        height: 100px;
                        margin: auto;
                        
                    }
                </style>
            '''
                )
          with bala[1]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
          with bala[4]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
        elif selected_tab == 'Leverage Ratios':
         with st.container(height=300, border=False):
          balas = st.columns([0.3, 0.1,0.05, 0.3, 0.1], gap='small')
      
          with balas[0] :
            val1 = df_main[df_main['Company_Name'] == selected_company]['debt_to_equity'].unique()[0].round(2)
            val1 = int(val1)
            if val1 == 0 :
              st.write("Disponile Bientôt")
            elif select_sector == 'Secteur' :
              debt_ratio_bank(val1, 'Debt to Equity (D/E)')
            else:
               debt_ratio(val1, 'Debt to Equity (D/E)')
          with balas[1]:
           st.markdown('<span style="color:#6BFF07">■</span>  Low', unsafe_allow_html=True)          
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#FF5D91  ">■</span>  High', unsafe_allow_html=True)
          with balas[4]:
           st.markdown('<span style="color:#FF5D91  ">■</span>  Low', unsafe_allow_html=True)
           st.markdown('<span style="color:#a4f26f">■</span>  Moderate', unsafe_allow_html=True)
           st.markdown('<span style="color:#6BFF07">■</span>  High', unsafe_allow_html=True)
        

st.set_option('deprecation.showPyplotGlobalUse', False)

 
    
        
