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
import pickle
import matplotlib.collections as mcoll
import networkx as nx

# Create structure and headers
st.header('Optimization of road inspector locations', divider='red')
st.subheader('A data story by RWS group 3')

st.write('This dashboard shows the results of this data science project. Enjoy!')
st.write('This map shows all the results')


# st.sidebar.write('Made by: RWS group 3')
# st.sidebar.write('[insert names]')

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
tab_a, tab_b, tab_c = st.tabs(['Overview results', 'Boxplots', 'Inspector areas'])

# Show result summary
results_path = image_path = Path(__file__).parents[0] / "Dashboard_data/Results_df"
df_results = pd.read_csv(results_path, index_col=0)
tab_a.dataframe(df_results)

# Show boxplots to compare results
image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/Opt_boxplot.png"
image_result = Image.open(image_path)
tab_b.image(image_result)

# Show some shortest path examples
tab_c.write('The map here shows the areas that each road inspector covers for method 1, minimum travel times.')

# tab_c.write('NEED TO BE UPDATED WITH REAL POINTS INSTEAD OF RANDOM')
image_path = Path(__file__).parents[0] / "Dashboard_data/Inspectorareas.png"
image_path = Image.open(image_path)
tab_c.image(image_path)

path = Path(__file__).parents[0] / "NetworkX_graph_new.pickle"
G = pickle.load(open(path, 'rb'))

def WGS84toDutchRD(wgs84East, wgs84North):
    # translated from Peter Knoppers's code

    # wgs84East: longtitude
    # wgs84North: latitude

    # Western boundary of the Dutch RD system. */
    WGS84_WEST_LIMIT = 3.2

    # Eastern boundary of the Dutch RD system. */
    WGS84_EAST_LIMIT = 7.3

    # Northern boundary of the Dutch RD system. */
    WGS84_SOUTH_LIMIT = 50.6

    # Southern boundary of the Dutch RD system. */
    WGS84_NORTH_LIMIT = 53.7

    if (wgs84North > WGS84_NORTH_LIMIT) or \
        (wgs84North < WGS84_SOUTH_LIMIT) or \
        (wgs84East < WGS84_WEST_LIMIT) or \
        (wgs84East > WGS84_EAST_LIMIT):
        resultX = -1
        resultY = -1
    else:
        r = [[155000.00, 190094.945,   -0.008, -32.391, 0.0],
            [-0.705, -11832.228,    0.0  ,   0.608, 0.0],
            [0.0  ,   -114.221,    0.0  ,   0.148, 0.0],
            [0.0  ,     -2.340,    0.0  ,   0.0  , 0.0],
            [0.0  ,      0.0  ,    0.0  ,   0.0  , 0.0]]
        s = [[463000.00 ,      0.433, 3638.893,   0.0  ,  0.092],
            [309056.544,     -0.032, -157.984,   0.0  , -0.054],
            [73.077,      0.0  ,   -6.439,   0.0  ,  0.0],
            [59.788,      0.0  ,    0.0  ,   0.0  ,  0.0],
            [0.0  ,      0.0  ,    0.0  ,   0.0  ,  0.0]]
        resultX = 0
        resultY = 0
        powNorth = 1
        dNorth = 0.36 * (wgs84North - 52.15517440)
        dEast = 0.36 * (wgs84East - 5.38720621)

        for p in range(5):
            powEast = 1
            for q in range(5):
                resultX = resultX + r[p][q] * powEast * powNorth
                resultY = resultY + s[p][q] * powEast * powNorth
                powEast = powEast * dEast
            powNorth = powNorth * dNorth
    return resultX, resultY

def plot_network(G):
    """Returns fig, ax of a subplot containing the road network of NL
    This can be used to plot other things like shortest path or clusters of an inspector"""
    
    # Make array containing all edges from network G
    edges_arr = np.array(list(G.edges()))

    # Make a figure
    fig, ax = plt.subplots()
    fig.set_figheight(5)

    # Add edges from network to LineCollection object
    line_segments = mcoll.LineCollection(edges_arr, colors='cornflowerblue')
    ax.add_collection(line_segments)

    # Set limits and scale of figure
    ax.set(xlim=(np.min(edges_arr[:, :, 0]),np.max(edges_arr[:, :, 0])), 
        ylim=(np.min(edges_arr[:, :, 1]),np.max(edges_arr[:, :, 1])))

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    return fig, ax

def plot_area_inspector(cluster, inspector_loc, time_to_incident, time_str='minimum', G=G):
    """Color roads that certain inspector is responsible for
    cluster is a integer. Make sure it is not larger than the no. of inspectors in dataset
    The coordinates in time_to_incident have to be in WGS84 coordinates"""

    # Create figure with NL road network
    fig, ax = plot_network(G)

    # Get right coordinates for inspectors
    loc_inspector = WGS84toDutchRD(inspector_loc.loc[cluster - 1]['1'], inspector_loc.loc[cluster - 1]['0'])
    
    # Get coordinates for all incidents in the cluster
    coor = np.array(time_to_incident[time_to_incident['2'] == cluster])

    # Plot the cluster
    ax.scatter(coor[:, 0], coor[:, 1], s=2, zorder=2, color='salmon')
    ax.scatter(0, 0, s=2, color='salmon', label='Incidents within reach')

    # Plot inspector point
    ax.scatter(loc_inspector[0], loc_inspector[1], color='red', zorder=2)
    
    ax.set_title(f'Area of inspector {cluster} for method 1 with minimum travel times')

    ax.scatter(0, 0, color='red', label='Location of inspector')

    ax.legend()
    return fig

path = Path(__file__).parents[0] / "Dashboard_data/Optimization_results/cluster_min_inspector_locations.csv"
cluster_min_inspector_loc = pd.read_csv(path, sep=';')

path = Path(__file__).parents[0] / "Dashboard_data/cluster_min_traveltime_WGS84"
min_traveltime_WGS84 = pd.read_csv(path, index_col=0)


message = f'Please enter an integer between 1 and {len(cluster_min_inspector_loc)}.'
cluster = tab_c.number_input(message, min_value=1, value=18, max_value=len(cluster_min_inspector_loc))
if cluster != int(cluster):
    tab_c.write('Please enter an integer')
else:
    fig = plot_area_inspector(cluster, cluster_min_inspector_loc, min_traveltime_WGS84, time_str='minimum', G=G)
    tab_c.pyplot(fig)





st.divider()
st.write('These tabs delve a bit deeper into the methods used to come to the results and the different steps taken')
# Tabs for statistics
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Incidents", 
                                            "Network",
                                            "Clustering 1 & 2",
                                            "Machine Learning",
                                            "Frequency-based"])


# Tab 1, incidents
tab1.write("Statistics of incidents")
tab1.write('This figures shows how the incidents were spread over the day')

image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/incident_day.png"
image_incident = Image.open(image_path)
tab1.image(image_incident)

# Tab 2 speed data
tab2.write('To use the algorithms, a networkX graph was made to easily find the shortest path.')
tab2.write('However, the graph was unconnected when extracting the data from the shapefile')
tab2.write('Using two different methods, the missing edges were estimated. Those can be seen in the following graph:')

image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/connecting_network.png"
image_network = Image.open(image_path)
tab2.image(image_network)

tab2.write("Besides that, the speed on each road section had to be calculated")
tab2.write("Here is some info about how speed is calculated ...")
tab2.write("And here a nice small boxplot comparing maximum speed on roads and estimated peak hour speed")

image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/Speed_boxplot.png"
image_speed = Image.open(image_path)
tab2.image(image_speed)

# Tab 3
tab3.write('This figure shows how the clustering optimization methods work')

image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/clustering_explanation.PNG"
image_cluster = Image.open(image_path)
tab3.image(image_cluster)

# Tab 4
tab4.write('TODO')

# Tab 5
tab5.write('This figure shows how the frequency-based optimization works')

image_path = Path(__file__).parents[0] / "Dashboard_data/Figures/frequencybased_explanation.PNG"
image_freq = Image.open(image_path)
tab5.image(image_freq)
