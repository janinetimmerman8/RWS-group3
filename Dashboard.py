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

# Create structure and headers
st.header('Optimization of road inspector locations', divider='red')
st.subheader('A data story by RWS group 3')

st.write('This dashboard shows the results of this data science project. Enjoy!')
st.write('At the bottom of the page, you can see some statistics')


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

# Tabs for statistics
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Incidents", "Speed",
                                            "Optimization method 1",
                                            "Optimziation method 2",
                                            "Optimization method 3"])


# Tab 1, incidents
tab1.write("Statistics of incidents")
tab1.write('Add more nice statistics and information')


# Make date time type of start time column
incidents_df['start_time'] = pd.to_datetime(incidents_df['start_time'])

incidents_df['hour_of_day'] = incidents_df['start_time'].apply(lambda x: x.hour)
hourly_counts = incidents_df.groupby('hour_of_day').size().reset_index(name='accident_count')

fig_1 = plt.figure(figsize=(12, 6))
plt.bar(hourly_counts['hour_of_day'], hourly_counts['accident_count'])
plt.xlabel('Hour of a day')
plt.ylabel('Accidents count')
plt.title('Accident count by hour of day')
plt.xticks(hourly_counts['hour_of_day'])

plt.axvspan(0, 5, alpha=0.2, color='red', label='0-5h')
plt.axvspan(6, 9, alpha=0.2, color='black', label='6-9h')
plt.axvspan(10, 14, alpha=0.2, color='green', label='10-14h')
plt.axvspan(15, 18, alpha=0.2, color='yellow', label='15-18h')
plt.axvspan(19, 23, alpha=0.2, color='orange', label='19-23h')
plt.legend()


tab1.pyplot(fig_1)

# Tab 2 speed data
tab2.write("Here is some info about how speed is calculated ...")
tab2.write("And here a nice small boxplot")

fig_2 = plt.figure(figsize=(8, 6))

category = ['Max_speed', 'Peak_speed']

for i in range(2):
    bp = plt.boxplot(speed_df[category[i]], patch_artist=True, 
                showmeans=False, positions=[i])

    for item in ['boxes', 'whiskers', 'medians', 'caps']:
            plt.setp(bp[item], color='darkred')

    plt.setp(bp['boxes'], facecolor='lightsalmon', alpha=0.6)
    plt.setp(bp['fliers'], markeredgecolor='darkred')

plt.ylabel('Speed on the higways [km/h]')
plt.xticks([0, 1], labels=['Maximum speed', 'Peak hour speed'])
plt.title('Boxplot of speed distribution')

tab2.pyplot(fig_2)

# Tab 3
tab3.write('Here some info how the frequency based optimization works')

# Tab 4
tab4.write('Here some info about how the machine learning optimization works')

# Tab 5
tab5.write('Here some info about how the clustering optimization works')
