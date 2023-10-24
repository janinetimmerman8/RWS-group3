# Import modules
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
from PIL import Image

# Create structure and headers
st.header('Optimization of road inspector locations', divider='red')
st.subheader('A data story by RWS group 3')

st.write('This dashboard shows the results of this data science project. Enjoy!')
st.write('This map shows all the results')


st.sidebar.write('Made by: RWS group 3')
st.sidebar.write('[insert names]')

# Load data
incidents_df_path = map_path = Path(__file__).parents[0] / "Dashboard_data/incidents_data"
incidents_df = pd.read_csv(incidents_df_path, sep=';')

speed_df_path = map_path = Path(__file__).parents[0] / "Dashboard_data/speed_data.shp"
speed_df = gpd.read_file(speed_df_path)

# Open folium map
map_path = Path(__file__).parents[0] / "Dashboard_data/Dashboard_map.html"

HtmlFile = open(map_path, 'r', encoding='utf-8')
source_code = HtmlFile.read() 

components.html(source_code, height = 600, width=850)

st.divider()
st.write('The following tabs show some more information about the final results')
# Make tabs for results
tab_a, tab_b, tab_c = st.tabs(['Overview results', 'Boxplots', 'Shortest path'])

# Show result summary
results_path = image_path = Path(__file__).parents[0] / "Dashboard_data/Results_df"
df_results = pd.read_csv(results_path, index_col=0)
tab_a.dataframe(df_results)

# Show boxplots to compare results
image_path = Path(__file__).parents[0] / "Dashboard_data/Opt_boxplot.png"
image_result = Image.open(image_path)
tab_b.image(image_result)

# Show some shortest path examples
tab_c.write('Here you can see an example of the route an inspector takes to an accident')

tab_c.write('NEED TO BE UPDATED WITH REAL POINTS INSTEAD OF RANDOM')
image_path = Path(__file__).parents[0] / "Dashboard_data/pathfinding.png"
image_path = Image.open(image_path)
tab_c.image(image_path)

st.divider()
st.write('These tabs delve a bit deeper into the methods used to come to the results and the different steps taken')
# Tabs for statistics
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Incidents", 
                                            "Network",
                                            "Clustering",
                                            "Method 2",
                                            "Method 3",
                                            "Method 4"])


# Tab 1, incidents
tab1.write("Statistics of incidents")
tab1.write('Add more nice statistics and information')

image_path = Path(__file__).parents[0] / "Dashboard_data/incident_day.png"
image_incident = Image.open(image_path)
tab1.image(image_incident)

# Tab 2 speed data
tab2.write('To use the algorithms, a networkX graph was made to easily find the shortest path.')
tab2.write('However, the graph was unconnected when extracting the data from the shapefile')
tab2.write('Using two different methods, the missing edges were estimated. Those can be seen in the following graph:')

image_path = Path(__file__).parents[0] / "Dashboard_data/connecting_network.png"
image_network = Image.open(image_path)
tab2.image(image_network)

tab2.write("Besides that, the speed on each road section had to be calculated")
tab2.write("Here is some info about how speed is calculated ...")
tab2.write("And here a nice small boxplot comparing maximum speed on roads and estimated peak hour speed")

image_path = Path(__file__).parents[0] / "Dashboard_data/Speed_boxplot.png"
image_speed = Image.open(image_path)
tab2.image(image_speed)

# Tab 3
tab3.write('Here some info how the clustering based optimization works')

# Tab 4
tab4.write('Here some info about ')

# Tab 5
tab5.write('Here some info about ')

# Tab 6
tab6.write('Here some info about ')
