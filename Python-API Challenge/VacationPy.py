#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import gmaps
import json
from api_keys import g_key
gmaps.configure(api_key=g_key)


# In[ ]:


cities = pd.read_csv("output_data/cities.csv", encoding="utf-8")
cities.head()


# In[ ]:


# Humidity Heat Map

humidity = cities["Humidity"].astype(float)
maxhumidity = humidity.max()
locations = cities[["Lat", "Lng"]]


# In[ ]:


fig = gmaps.figure()
heat_layer = gmaps.heatmap_layer(locations, weights=humidity,dissipating=False, max_intensity=maxhumidity,point_radius=3)
fig.add_layer(heat_layer)
fig


# In[ ]:


# Create new DataFrame fitting weather criteria

narrowed_city_df = cities.loc[(cities["Max Temp"] > 70) & (cities["Max Temp"] < 80) & (cities["Cloudiness"] == 0), :]
narrowed_city_df = narrowed_city_df.dropna(how='any')
narrowed_city_df.reset_index(inplace=True)
del narrowed_city_df['index']
narrowed_city_df.head()


# In[ ]:


# Hotel Map

hotellist = []

for i in range(len(narrowed_city_df)):
    lat = narrowed_city_df.loc[i]['Lat']
    lng = narrowed_city_df.loc[i]['Lng']

    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,
        "types" : "hotel",
        "key": g_key
    }
    
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    requested = requests.get(base_url, params=params)
    jsn = requested.json()
    try:
        hotellist.append(jsn['results'][0]['name'])
    except:
        hotellist.append("")
narrowed_city_df["Hotel Name"] = hotellist
narrowed_city_df = narrowed_city_df.dropna(how='any')
narrowed_city_df.head()


# In[ ]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in narrowed_city_df.iterrows()]
locations = narrowed_city_df[["Lat", "Lng"]]


# In[ ]:



markers = gmaps.marker_layer(locations)
fig.add_layer(markers)
fig

