import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui

from bourse import df_main # import main dataframe
from all_functions import plot_PER, filter_ratio


df_main = df_main
#df_main = pd.read_csv('output_6.csv')
sector = df_main['Secteur'].unique()
def app():


    col = st.columns([0.2, 0.8], gap='medium')  

    with col[0]:
      selected_sector = st.selectbox('Secteur', sector)
    #plot_PER()
   
      if selected_sector:
        companies = df_main[df_main['Secteur'] == selected_sector]['Company_Name'].unique()
        selected_company = st.selectbox('Entreprises' , companies)
    
    
       
    with col[1]:
        
        st.caption(f"""
                        <div class="resume_ratio">Les ratios financiers,
                    tels que les ratios de liquidité (capacité à couvrir les dettes à court terme), 
                   de rentabilité (marge bénéficiaire nette, ROE), 
                   d\'endettement (niveau de dette par rapport aux capitaux propres) 
                   et d'efficacité (rotation des actifs), sont cruciaux pour les investisseurs. 
                   Ils fournissent une vue d'ensemble sur la santé financière et la performance opérationnelle
                    d'une entreprise, aidant ainsi à prendre des décisions d'investissement éclairées.</div> """,
                          unsafe_allow_html=True)   
        bol = st.columns([0.1, 0.3, 0.1, 0.3], gap='medium')

        with bol[1] :
            val1 = df_main[df_main['Company_Name'] == selected_company]['debt_to_equity'].unique()[0].round(2)
            val1 = int(val1)
            if val1 == 0 :
              st.write("Disponile Bientôt")
            else:
              ui.metric_card(
            title="Debt to Equity ( D/E )",
            content=f"{val1} %",
            description="environ",
            key=f"card1",
           )
        
        with bol[3] :
            val3 = df_main[df_main['Company_Name'] == selected_company]['return_on_equity'].unique()[0].round(2)
            val3 = int(val3)
            if val3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ui.metric_card(
            title="Return on Equity ( ROE )",
            content=f"{val3} %",
            description="environ",
            key=f"card",
           )
            
        bal = st.columns([0.1, 0.3, 0.1, 0.3], gap='medium')


        with bal[1] :
          
            vol1 = df_main[df_main['Company_Name'] == selected_company]['current_ratio'].unique()[0].round(2)
            vol1 = int(vol1)
            if vol1 == 0 :
              st.write("Disponile Bientôt")
            else:
              ui.metric_card(
            title="Current Ratio ( CR )",
            content=f"{vol1} %",
            description="environ",
            key=f"card3",
           )
            
        with bal[3] :
            vol3 = df_main[df_main['Company_Name'] == selected_company]['return_on_asset'].unique()[0].round(2)
            vol3 = int(vol3)
            if vol3 == 0 :
              st.write("Disponile Bientôt")
            else:
              ui.metric_card(
            
              content=f"{vol3} %",
              title="Return on Asset ( ROA ) ",
              description="environ",
             key="fuck",
    
           )

    ### Plot P.E.R Ratios  

    go = st.columns([0.1, 0.4, 0.3], gap='medium')    
    with go[1]:
      filtered_data = filter_ratio(df_main, selected_sector, selected_company)
      fig1 = plot_PER(filtered_data, selected_company) 
      #st.plotly_chart(fig1)
        
