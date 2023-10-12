import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
import pandas as pd
import branca.colormap as cm
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from pathlib import Path

# Import visualize function to make things more organized
# from Map_function_dashboard import visualize_map
# from Map_function_dashboard import DutchRDtoWGS84

# Create structure and headers
st.header('Optimization of road inspector locations', divider='red')
st.subheader('A data story by RWS group 3')

st.write('This dashboard shows the results of this data science project. Enjoy!')

st.sidebar.write('Made by: ...')

# # Import data
# speed_path = Path(__file__).parents[0] / 'speed_data.shp'
# incidents_path = Path(__file__).parents[0] / 'incidents_data'

# speed = gpd.read_file(speed_path)
# incidents = pd.read_csv(incidents_path, sep=';')


map_path = Path(__file__).parents[0] / "Dashboard_data\Dashboard_map.html"

HtmlFile = open(map_path, 'r', encoding='utf-8')
source_code = HtmlFile.read() 
# print(source_code)

# @st.cache_resource ## cache something??
components.html(source_code, height = 600)