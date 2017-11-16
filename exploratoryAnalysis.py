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
import pysal as ps
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns




os.chdir("/home/k1461506/BikeTrips")
if os.path.isdir('outputs') is not True:
    os.mkdir('outputs')
    
shplink = os.path.join("data", "census_tracts_2010.shp")    

Q1_trips = pd.read_csv(os.path.join("data", "Divvy_Trips_2017_Q1.csv"), error_bad_lines=False, header=0, engine="python")
stations = pd.read_csv(os.path.join("data", "Divvy_Stations_2017_Q1Q2.csv"), header=0, engine="python")

chicago = gpd.read_file(shplink)

#Size of Q1 trips dataframe 
print "Q1_trips has %d rows of data and %d columns" %(Q1_trips.shape[0], Q1_trips.shape[1])

#find range of trip durations
print max(Q1_trips["tripduration"]) #There seems to be a ridiculous number of outliers 
print min(Q1_trips["tripduration"])

#Find IQR 
q75, q25 = np.percentile(Q1_trips["tripduration"], [75, 25])
iqr = q75-q25

Q1_trips[Q1_trips["tripduration"] > (q75 * 1.5)].count()

#Plot trip durations
plt.plot(Q1_trips["tripduration"])


#Plot bike station points on chicago census tracts map
f, ax = plt.subplots(figsize=(10, 10))
chicago.plot(color="white", ax = ax, edgecolor="#cccccc", alpha=0.5)
ax.scatter(stations["longitude"], stations["latitude"], alpha=0.5, marker="x")
ax.set_axis_off()

plt.show()
