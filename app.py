from flask import Flask

import folium
import pandas as pd
from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def index():

    # Load tower informaiton
    inputFileTower = open('tower_list.csv', 'r')
    tower = defaultdict(int)
    line = inputFileTower.readline()
    line = inputFileTower.readline()
    while line:
        fields = line.split(",")
        location = [float(fields[1].strip("\'")),float(fields[2].strip("\'\\\n"))]
        tower[int(fields[0].strip("\'"))]=location
        line = inputFileTower.readline()

    inputFileTower.close() 

    # Accessing API data using the python "requests" module
    oneUser = pd.read_csv('inputFile.csv')
    oneUser['lat'] =  oneUser.apply (lambda row: tower[row.tower][0], axis=1)
    oneUser['lon'] =  oneUser.apply (lambda row: tower[row.tower][1], axis=1)
    data = oneUser
    # Make an empty map
    m = folium.Map(location=[23.8139, 90.3986], tiles="OpenStreetMap", zoom_start=12)
    for index, row in data.iterrows():
        folium.CircleMarker([row['lat'], row['lon']],
                        radius=15,fill_color=row['date'],fill=True, popup = (row)).add_to(m)
    m                                                           
    return m._repr_html_()

if __name__ == "__main__":
    app.run()
