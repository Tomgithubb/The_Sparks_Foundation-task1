# -*- coding: utf-8 -*-
"""Exploratory Data Analysis- Terrorism

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LWm6N0UnaU9mdh8lrAj6AeFBp5oUCMZV

#GRIP: The Sparks Foundation

#Data Science and Business Analytics Internship

#Author: Prerna Kumari

#Task4: Perform Exploratory Data Analysis on dataset 'Global Terrorism'

Dataset: https://bit.ly/2TK5Xn5
"""

import math
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

gt = pd.read_csv('/content/global-terrorism.csv',encoding='ISO-8859-1')
gt.head()

gt.columns

gt.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'state',
                       'region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed',
                       'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type',
                       'weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)

# Here I just take important data in whole dataset those I'm using further processing.

gt = gt[['Year','Month','Day','Country','state','Region','city','latitude','longitude','AttackType','Killed',
               'Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]

# Checking the null velues in data

gt.isnull().sum()

gt.info()

print("Country with the most attacks:",gt['Country'].value_counts().idxmax())
print("City with the most attacks:",gt['city'].value_counts().index[1]) #as first entry is 'unknown'
print("Region with the most attacks:",gt['Region'].value_counts().idxmax())
print("Year with the most attacks:",gt['Year'].value_counts().idxmax())
print("Month with the most attacks:",gt['Month'].value_counts().idxmax())
print("Group with the most attacks:",gt['Group'].value_counts().index[1])
print("Most Attack Types:",gt['AttackType'].value_counts().idxmax())

from wordcloud import WordCloud
from scipy import signal
cities = gt.state.dropna(False)
plt.subplots(figsize=(10,10))
wordcloud = WordCloud(background_color = 'white',
                     width = 512,
                     height = 384).generate(' '.join(cities))
plt.axis('off')
plt.imshow(wordcloud)
plt.show()

gt['Year'].value_counts(dropna = False).sort_index()

#DATA VISUALISATION
#Number of Terrorist Activities each Year#
x_year = gt['Year'].unique()
y_count_years = gt['Year'].value_counts(dropna = False).sort_index()
plt.figure(figsize = (18,10))
sns.barplot(x = x_year,
           y = y_count_years,
           palette = 'rocket')
plt.xticks(rotation = 45)
plt.xlabel('Attack Year')
plt.ylabel('Number of Attacks each year')
plt.title('Attack_of_Years')
plt.show()

#Terrorist Activities by Region in each Year through Area Plot
pd.crosstab(gt.Year, gt.Region).plot(kind='area',figsize=(15,6))
plt.title('Terrorist Activities by Region in each Year')
plt.ylabel('Number of Attacks')
plt.show()

gt['Wounded'] = gt['Wounded'].fillna(0).astype(int)
gt['Killed'] = gt['Killed'].fillna(0).astype(int)
gt['casualities'] = gt['Killed'] + gt['Wounded']

gt1 = gt.sort_values(by='casualities',ascending=False)[:40]

heat=gt1.pivot_table(index='Country',columns='Year',values='casualities')
heat.fillna(0,inplace=True)

heat.head()

gt.Country.value_counts()[:15]

"""#ANALYSIS ON CUSTOMIZED DATA

#Terrorist Attacks of a Particular year and their Locations
"""

#Let's look at the terrorist acts in the world over a certain year.
import folium
from folium.plugins import MarkerCluster
filterYear = gt['Year'] == 1980

filterData = gt[filterYear] # filter data
# filterData.info()
reqFilterData = filterData.loc[:,'city':'longitude'] #We are getting the required fields
reqFilterData = reqFilterData.dropna() # drop NaN values in latitude and longitude
reqFilterDataList = reqFilterData.values.tolist()
# reqFilterDataList

map = folium.Map(location = [0, 30], tiles='CartoDB positron', zoom_start=2)
# clustered marker
markerCluster = folium.plugins.MarkerCluster().add_to(map)
for point in range(0, len(reqFilterDataList)):
    folium.Marker(location=[reqFilterDataList[point][1],reqFilterDataList[point][2]],
                  popup = reqFilterDataList[point][0]).add_to(markerCluster)
map

"""About 20% of the incidents occurred in Latin America and another 20% in the Middle East. , Of the 5,955 international terrorist incidents recorded between 1968 and 1979, 673 incidents (II percent) involved deaths and 867 (15 percent) involved injuries. These proportions are up sliahtly in 1980.

Now let's check out which terrorist organizations have carried out their operations in each country. A value count would give us the terrorist organizations that have carried out the most attacks. we have indexed from 1 as to negate the value of 'Unknown'
"""

gt.Group.value_counts()[1:15]

test = gt[gt.Group.isin(['Shining Path (SL)','Taliban','Islamic State of Iraq and the Levant (ISIL)'])]

test.Country.unique()

gt_df_group = gt.dropna(subset=['latitude','longitude'])
gt_df_group = gt_df_group.drop_duplicates(subset=['Country','Group'])
terrorist_groups = gt.Group.value_counts()[1:8].index.tolist()
gt_df_group = gt_df_group.loc[gt_df_group.Group.isin(terrorist_groups)]
print(gt_df_group.Group.unique())

map = folium.Map(location=[20, 0], tiles="CartoDB positron", zoom_start=2)
markerCluster = folium.plugins.MarkerCluster().add_to(map)
for i in range(0,len(gt_df_group)):
    folium.Marker([gt_df_group.iloc[i]['latitude'],gt_df_group.iloc[i]['longitude']],
                  popup='Group:{}<br>Country:{}'.format(gt_df_group.iloc[i]['Group'],
                  gt_df_group.iloc[i]['Country'])).add_to(map)
map

"""The Above map looks untidy even though it can be zoomed in to view the Country in question. Hence in the next chart, I have used Folium's Marker Cluster to cluster these icons. This makes it visually pleasing and highly interactive."""

gt.head()

# Total Number of people killed in terror attack

killData = gt.loc[:,'Killed']
print('Number of people killed by terror attack:', int(sum(killData.dropna())))# drop the NaN values

# Let's look at what types of attacks these deaths were made of.

attackData = gt.loc[:,'AttackType']
# attackData
typeKillData = pd.concat([attackData, killData], axis=1)

typeKillData.head()

typeKillFormatData = typeKillData.pivot_table(columns='AttackType', values='Killed', aggfunc='sum')
typeKillFormatData

typeKillFormatData.info()

"""Armed assault and bombing/explosion are seen to be the cause of 77% of the deaths in these attacks. This rate is why these attacks are used so many times in terrorist actions. This is how dangerous weapons and explosives are to the world."""

#Number of Killed in Terrorist Attacks by Countries

countryData = gt.loc[:,'Country']
# countyData
countryKillData = pd.concat([countryData, killData], axis=1)

countryKillFormatData = countryKillData.pivot_table(columns='Country', values='Killed', aggfunc='sum')
countryKillFormatData

fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size

labels = countryKillFormatData.columns.tolist()
labels = labels[:50] #50 bar provides nice view
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[:50]
values = [int(i[0]) for i in values] # convert float to int
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange'] # color list for bar chart bar color
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize = 20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize = 20)
# print(fig_size)
plt.show()

labels = countryKillFormatData.columns.tolist()
labels = labels[50:101]
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[50:101]
values = [int(i[0]) for i in values]
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=20
fig_size[1]=20
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize = 20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize = 20)
plt.show()

labels = countryKillFormatData.columns.tolist()
labels = labels[152:206]
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[152:206]
values = [int(i[0]) for i in values]
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize = 20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize = 20)
plt.show()

"""Terrorist acts in the Middle East and northern Africa have been seen to have fatal consequences. The Middle East and North Africa are seen to be the places of serious terrorist attacks. In addition, even though there is a perception that Muslims are supporters of terrorism, Muslims are the people who are most damaged by terrorist attacks. If you look at the graphics, it appears that Iraq, Afghanistan and Pakistan are the most damaged countries. All of these countries are Muslim countries."""