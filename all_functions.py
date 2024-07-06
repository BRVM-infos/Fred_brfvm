import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
import logging
import re


#******************* Définir les fonction graphiques*************

def filter_data(df, country, company):
    filtered_df = df[(df['Secteur'] == country) & (df['Company_Name'] == company)]
    return filtered_df
    
def filter_ratio(df, sector, company):
    filtered_df = df[(df['Secteur'] == sector) & (df['Company_Name'] == company)]
    return filtered_df

def plot_dividende(stock_data, company):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=stock_data['Date'], 
        y=stock_data['Dividende'], 
        mode='lines+markers',
        marker=dict(color='#0addf0', size=20),  # Adjust marker size here
        line=dict(color='grey'),  # Adjust line color if needed
        name='Dividende',
        
    ))
    fig.update_layout(
        #title=f'Dividende en FCFA ',
        title = {'text': "Dividende net (Fcfa)", 
                            'font': {'color': 'black','size': 18}},
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True ), # Disable zoom on x-axis
        template='plotly_white',
        #plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Plot area background color
        #paper_bgcolor='rgba(0, 0, 0, 0.1)',# Overall background color
        #width=400,  # Set the width here
        height=350,  # Set the height here
        margin=dict(l=10, r=20, t=50, b=20),  # Adjust the margins around the plot
    )
    return fig

def plot_benefice(stock_data, company):
    colors = ['#FF5D91' if val < 0 else '#6BFF07' for val in stock_data['Resultat_net']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stock_data['Date'],
        y=stock_data['Resultat_net'],
        marker_color=colors,
        width=0.5
    ))
    # Customize the x-axis to show all categories
    fig.update_xaxes(
        tick0=0,
        dtick=1 ) #
    fig.update_layout(
      #  title=f'Bénéfice net',
       title = {'text': "Bénéfice net (Million Fcfa)", 
                            'font': {'color': 'black', 'size': 18} },
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True ), # Disable zoom on x-axis
        bargap=0.0,  # Adjust the gap as needed 
        template='plotly_white',
         #plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Plot area background color
        #paper_bgcolor='rgba(0, 0, 0, 0.1)', # Overall background color
        #width=400,  # Set the width here
        height=350,  # Set the height here
        margin=dict(l=10, r=20, t=50, b=20),  # Adjust the margins around the plot
    )
    return fig

def price(url):
           
        
    # Fetch HTML content
           #response = requests.get(url)
          # Parse HTML content
           #soup = BeautifulSoup(response.text, 'html.parser')
           class_name = 'cot1u'  
           try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
             # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
        # Extract data from the specified HTML class
            elements = soup.find_all(class_=class_name)
            return   [element.text.strip() for element in elements][0].split(" ")[0].replace('XOF', '')

           except requests.exceptions.RequestException as e:
              logging.error(f"Error fetching data from {url}: {e}")
              return "Désolé de l'erreur"
         # Extract data from the specified HTML class
           #lements = soup.find_all(class_=class_name)
           
            
def plot_PER(stock_data, company):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=['2019','2020', '2021', '2022', '2023'], 
        y=stock_data['PER'], 
        mode='lines+markers', 
        marker=dict(color='orange', size=20),  # Adjust marker size here
        line=dict(color='grey'),  # Adjust line color if needed
        name='Dividende'
    ))
    fig.update_layout(
        #title=f'Dividende en FCFA ',
        title = {'text': "P.E.R", 
                            'font': {'color': 'lightgrey', 'size': 18} },
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True ), # Disable zoom on x-axis
        template='plotly_white',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Plot area background color
        paper_bgcolor='rgba(0, 0, 0, 0.1)',# Overall background color
        #width=400,  # Set the width here
        height=350,  # Set the height here
        margin=dict(l=10, r=20, t=50, b=20),  # Adjust the margins around the plot
    )
    return fig

def history_variation(ticket):  
    # Specify the URL of the webpage to scrape and the class name
    url = 'https://www.sikafinance.com/marches/cotation_' + ticket
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        class_name = 'tableVar'  # Replace with the actual class name

        # Find the specified class element
        table = soup.find('table', class_=class_name)
        if not table:
            print(f"No table found with class name: {class_name}")
            return None

        # Extract column names from <th> tags
        headers = table.find_all('th')
        columns = [header.get_text().strip() for header in headers]

        # Extract raw data from <tr> tags
        rows = table.find_all('tr')[1:]  # Skip the header row
        data = []
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text().strip() for cell in cells]
            data.append(row_data)

        # Create a DataFrame
        df = pd.DataFrame(data, columns=columns)
        # prompt: Avec le DataFrame df_annon: i like to use first column as index
        df.set_index(df.columns[0], inplace=True)
        # Apply the function to the DataFrame
        #styled_df = df.style.apply(style_dataframe, axis=1)
        # Display the styled DataFrame
        #st.write('Performance')
        #st.markdown(styled_df._repr_html_(), unsafe_allow_html=True)
        return st.dataframe(df)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def ratio_chart(value, title:str, l:int, m:int):
# Value for the gauge
 

# Define the gauge chart
 fig = go.Figure(go.Indicator(
    #title= "debt ratio",
    mode="gauge+number",
    value=value,
    number={'font': {'size': 30, 'color': '#0addf0','weight': 'bold'}, 'suffix': " %"},
    gauge={
        'axis': {'range': [0, 100], 'visible': True},  # Hide axis values
        'bar': {'color': "#0addf0"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, l], 'color': "#FF5D91"},#RED
            {'range': [l, m], 'color': "#a4f26f"},#lightgreen
            {'range': [m, 100], 'color': "#6BFF07"},# GREEN
             ],
     }
    ))
 fig.update_layout(
      
        title = {'text': f" \t\t \t\t \t\t \t\t \t\t {title}",
                            'font': {'color': 'grey', 'size': 18}},
    
        plot_bgcolor='#e8ebf1',  # Plot area background color
        paper_bgcolor='#e8ebf1', # Overall background color
        #width=290,  # Set the width here
        height=220,  # Set the height here
        margin=dict(l=10, r=20, t=50, b=20), # Adjust the margins around the plot
    )


 st.plotly_chart(fig)

def current_ratio(value, title:str):
# Value for the gauge
 

# Define the gauge chart
 fig = go.Figure(go.Indicator(
    #title= "debt ratio",
    mode="gauge+number",
    value=round(value/100, 1),
    number={'font': {'size': 30, 'color': '#0addf0','weight': 'bold'}},
    gauge={
        'axis': {'range': [0, 4], 'visible': True},  # Hide axis values
        'bar': {'color': "#0addf0"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 1], 'color': "#FF5D91"},
            {'range': [1, 4], 'color': "#6BFF07"},
             ],
     }
    ))
 fig.update_layout(
      
        title = {'text': f" \t\t \t\t \t\t \t\t \t\t {title}",
                            'font': {'color': 'grey', 'size': 18}},
    
        plot_bgcolor='#e8ebf1',  # Plot area background color
        paper_bgcolor='#e8ebf1', # Overall background color
        #width=290,  # Set the width here
        height=220,  # Set the height here
        margin=dict(l=10, r=10, t=50, b=30), # Adjust the margins around the plot
    )
 
 


 st.plotly_chart(fig)

def debt_ratio(value, title:str):
# Value for the gauge
 

# Define the gauge chart
 fig = go.Figure(go.Indicator(
    #title= "debt ratio",
    mode="gauge+number",
    value=round(value/100, 1),
    number={'font': {'size': 30, 'color': '#0addf0','weight': 'bold'}},
    gauge={
        'axis': {'range': [0, 12], 'visible': True},  # Hide axis values
        'bar': {'color': "#0addf0"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [2, 10], 'color': "#FF5D91"}, # Red
            {'range': [1, 2], 'color': "#a4f26f"},#LighGreen
            {'range': [0, 1], 'color': "#6BFF07"}, #Green
             ],
     }
    ))
 fig.update_layout(
      
        title = {'text': f" \t\t \t\t \t\t \t\t \t\t {title}",
                            'font': {'color': 'grey', 'size': 18}},
    
        plot_bgcolor='#e8ebf1',  # Plot area background color
        paper_bgcolor='#e8ebf1', # Overall background color
        #width=290,  # Set the width here
        height=220,  # Set the height here
        margin=dict(l=10, r=10, t=50, b=30), # Adjust the margins around the plot
    )
 
 


 st.plotly_chart(fig)

 def debt_ratio_bank(value, title):
  # Define the gauge chart
  fig = go.Figure(go.Indicator(
    #title= "debt ratio",
    mode="gauge+number",
    value=int(value/100),
    number={'font': {'size': 30, 'color': '#0addf0','weight': 'bold'}},
    gauge={
        'axis': {'range': [0, 25], 'visible': True},  # Hide axis values
        'bar': {'color': "#0addf0"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [15, 25], 'color': "#FF5D91"}, # Red
            {'range': [10, 15], 'color': "#a4f26f"},#LighGreen
            {'range': [0, 10], 'color': "#6BFF07"}, #Green
             ],
     }
    ))
  fig.update_layout(
      
        title = {'text': f" \t\t \t\t \t\t \t\t \t\t {title}",
                            'font': {'color': 'grey', 'size': 18}},
    
        plot_bgcolor='#e8ebf1',  # Plot area background color
        paper_bgcolor='#e8ebf1', # Overall background color
        #width=290,  # Set the width here
        height=220,  # Set the height here
        margin=dict(l=10, r=10, t=50, b=30), # Adjust the margins around the plot
    )
 
  st.plotly_chart(fig)

