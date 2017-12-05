#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:02:06 2017

@author: k1461506
"""
"""
Metadata:
trip_id: ID attached to each trip taken
start_time: day and time trip started, in CST
stop_time: day and time trip ended, in CST
bikeid: ID attached to each bike
tripduration: time of trip in seconds 
from_station_name: name of station where trip originated
to_station_name: name of station where trip terminated 
from_station_id: ID of station where trip originated
to_station_id: ID of station where trip terminated
usertype: "Customer" is a rider who purchased a 24-Hour Pass; "Subscriber" is a rider who purchased an Annual Membership
gender: gender of rider 
birthyear: birth year of rider
"""

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


os.chdir("D:\Documents\Project\BikeTrips") 

if os.path.isdir('outputs') is not True:
    os.mkdir('outputs')


Q1_trips = pd.read_csv(os.path.join("data", "Divvy_Trips_2017_Q1.csv"), error_bad_lines=False, header=0, engine="python")
stations = pd.read_csv(os.path.join("data", "Divvy_Stations_2017_Q1Q2.csv"), header=0, engine="python")


#Size of Q1 trips dataframe 
print "Q1_trips has %d rows of data and %d columns" %(Q1_trips.shape[0], Q1_trips.shape[1])

# find range of trip durations
# After converting them to minutes
Q1_trips["tripduration"] = Q1_trips["tripduration"]/60

print "Max duration: " 
print max(Q1_trips["tripduration"]) #There seems to be a ridiculous number of outliers 
print "Min duration: " 
print min(Q1_trips["tripduration"])

#Find IQR 
q75, q25 = np.percentile(Q1_trips["tripduration"], [75, 25])
iqr = q75-q25

# Trips above 75th percentile
Q1_trips = Q1_trips[Q1_trips["tripduration"] < (q75 * 1.5)]  
# And remove trips below the 25th percentile
Q1_trips = Q1_trips[Q1_trips["tripduration"] > q25]

# Check head of trips 
Q1_trips.head()

# We can create nodes of to and from station_ids to check the flows of commuters
tripGraph = nx.from_pandas_dataframe(Q1_trips, 'from_station_id', 'to_station_id', create_using=nx.Graph()) 
pos = nx.spring_layout(tripGraph)
plt.figure(3, figsize=(20, 20))
nx.draw(tripGraph, with_labels=True, node_color = "lightgrey")

# This does not look very nice, so let's see
# If we can draw connections between nodes on a map

#First, let's clean up a dataframe of unnecessary data - in this case, demographic data is not so important
nodes = Q1_trips.copy()
to_drop = ['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration', 'usertype', 'gender', 'birthyear']
nodes.drop(to_drop, axis=1, inplace=True) 

#clean up station files as well 
coords = stations.copy()
coords.drop(["name", "city", "dpcapacity", "online_date"], axis=1, inplace=True)

# Merge them
nodes = pd.merge(nodes, coords, left_on='from_station_id', right_on='id')

# Clean merged tables and repeat for stations from
nodes.rename(columns={'latitude':'lat_from', 'longitude':'long_from'}, inplace=True)
nodes.drop(['id'], axis=1, inplace=True)


nodes = pd.merge(nodes, coords, left_on='to_station_id', right_on='id')
nodes.rename(columns={'latitude':'lat_to', 'longitude':'long_to'}, inplace=True)
nodes.drop(['id'], axis=1, inplace=True)

# Now that we have a dataframe that is full of the latitude and logitude data we need,
# We can begin to attempt plotting it
# But first, save it to a csv so that we can pull it later 
nodes.to_csv(os.path.join('outputs', 'nodes.csv'))

from mpl_toolkits.basemap import Basemap as Basemap

# Get a basemap or chicago 
m = Basemap(
        projection='merc',
        llcrnrlon = -87.940102,
        llcrnrlat = 41.643921,
        urcrnrlon = -87.523987,
        urcrnrlat = 42.023022,
        lat_ts = 0,
        resolution='i',
        suppress_ticks = True)

# get dictionary of node positions 
# convert it to the right map projection
pos = {}
for i in range(stations.shape[0]):
    pos[stations['id'][i]] = m(stations['longitude'][i], stations['latitude'][i])

# This gives quite a bad graph at the moment (due to hyperconcentration of edges in the middle)
G = nx.Graph() 
for i in range(nodes.shape[0]):
    G.add_edge(nodes['from_station_id'][i], nodes['to_station_id'][i])
plt.figure(3, figsize=(20,20))
nx.draw_networkx(G, pos, with_labels=False, node_size = 50, node_color='blue', alpha=0.5, edge_color="#9595b7")
plt.savefig(os.path.join('outputs', 'network_graph.pdf'))

# TODO: Fix edges not showing up with base map 
# TODO: Add weights to edges
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='white', lake_color='white')
plt.show()

"""
# Use this code later 
#Plot bike station points on chicago census tracts map
f, ax = plt.subplots(figsize=(10, 10))
chicago.plot(color="white", ax = ax, edgecolor="#cccccc", alpha=0.5)
ax.scatter(stations["longitude"], stations["latitude"], alpha=0.5, marker="x")
ax.set_axis_off()

plt.show()
"""