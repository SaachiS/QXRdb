import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Tab Configuration
st.set_page_config(page_title="QXR", page_icon="Images/QXR_logo-removebg.png")

# Hides link Button 
st.markdown("""
    <style>
    /* Hide the link button */
    .stApp a:first-child {
        display: none;
    }
    
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)

# Hides Fullscreen Button 
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

# Sidebar color 
sidebar_style = """
<style>
[data-testid="stSidebar"] {
    background-color: #01051E;
}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# Sets background color
page_bg_img = """
<style>
[data-testid="stApp"] {
background-color: #343434;
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------
# MAIN
st.title("General Member Dashboard")

# Sidebar content
st.sidebar.header('Configurations')
amount_data_shown = st.sidebar.empty()  # Placeholder for later
st.sidebar.subheader('Table')
show_data = st.sidebar.checkbox('Show csv Data')  # Checkbox for showing our dataset
st.sidebar.markdown('---')  # Adds a horizontal line to create a separation
st.sidebar.markdown('<br>' * 1, unsafe_allow_html=True)
st.sidebar.image('Images/QXR_logo-removebg.png', use_column_width=True)

# Function to load data from Google Sheets
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1oXECl5MWUnHDzSbot-8zZGLNNpdB3pmEWAUjS6CVDLA/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=list(range(2))).reset_index(drop=True)
    return data

# Load data and cache the result to avoid reloading it on each interaction

def get_data_for_pie(df):
    year_count = df['Year'].value_counts().rename_axis('Year').reset_index(name='Count')
    program_count = df['Program'].value_counts().rename_axis('Program').reset_index(name='Count')
    return year_count, program_count

# Pie Charts
def generate_shades(hex_color, n):
    base_color = px.colors.hex_to_rgb(hex_color)
    scale = [(
        hex_color,
        f"rgb({base_color[0] * (1 - (i / n))}, "
        f"{base_color[1] * (1 - (i / n))}, "
        f"{base_color[2] * (1 - (i / n))})"
    ) for i in range(n)]
    return [color[1] for color in scale]

# Pie Charts with fancy styling
if not show_data:
    st.subheader("Visualization")
    df = load_data()
    year_count, program_count = get_data_for_pie(df)
    
    shades = generate_shades('#00e5fd', len(year_count))

    # Distribution by Year Pie Chart with fancy styling
    year_pie = px.pie(year_count, values='Count', names='Year', title="Distribution by Year",
                      color_discrete_sequence=shades, hole=0.3)
    year_pie.update_traces(textinfo='percent+label', 
                           pull=[0.1 if i == year_count['Count'].idxmax() else 0 for i in range(len(year_count))])
    year_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=True)

    shades = generate_shades('#00e5fd', len(program_count))

    # Distribution by Program Pie Chart with fancy styling
    prog_pie = px.pie(program_count, values='Count', names='Program', title="Distribution by Program",
                      color_discrete_sequence=shades, hole=0.3)

    prog_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=True)

    # Display the fancy pie charts
    st.plotly_chart(year_pie, use_container_width=True)
    st.plotly_chart(prog_pie, use_container_width=True)

else:  # If our checkbox is selected, display our dataset
    st.subheader("Raw Data")
    df = load_data()
    st.dataframe(df, width=600)
                
