from flask import Flask

import folium
import pandas as pd
import geopandas as gpd
import requests
from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def index():

    inputFileTower = open('tower_list.csv', 'r')
    tower = defaultdict(int)
    line = inputFileTower.readline()
    line = inputFileTower.readline()
    while line:
        fields = line.split(",")
        location = (float(fields[1].strip("\'")),float(fields[2].strip("\'\\\n")))
        tower[location]=int(fields[0].strip("\'"))
        line = inputFileTower.readline()
    inputFileTower.close()  
    
    # Accessing API data using the python "requests" module
    oneUser = pd.read_csv('inputFile.csv')
    date = 624
    oneDayOneUser = oneUser.loc[oneUser["date"] == date]
    tower_filtered = set(oneDayOneUser["tower"].unique())

    lat = []
    lon = []
    name = []
    for key,value in tower.items():
        if value in tower_filtered:
            name.append(value)
            lat.append(key[0])
            lon.append(key[1])
    data = pd.DataFrame({'lat':lat,'lon':lon,'name':name}, dtype=str)
    # Make an empty map
    folium_map = folium.Map(location=[23.8139, 90.3986], tiles="OpenStreetMap", zoom_start=10)
    for i in range(0,len(data)):
        folium.Marker(
        location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
        popup=data.iloc[i]['name'],).add_to(folium_map)

    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()