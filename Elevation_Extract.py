#%%
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import point, LineString
import rasterio
import matplotlib.pyplot as plt
import math
import os
from pyproj import CRS

work_path = r"G:\Goodwin_Creek\GoodwinCreekFlow\GoodwinCreekFlow\GoodwinCreekGIS"

in_line = "Goodwin_Creek_Xsecs_2.shp"
in_dem = "elev.tif"
outfp = "Goodwin_Creek_Xsecs_3d.shp"
outfp1 = "Goodwin_Creek_Station_Elevation.shp"

in_line = os.path.join(work_path, in_line)
in_dem = os.path.join(work_path, in_dem)
outfp = os.path.join(work_path, outfp)
outfp1 = os.path.join(work_path, outfp1)

line = gpd.read_file(in_line)
dem = rasterio.open(in_dem, mode = 'r')

num_xsecs = len(line)

# Coordinate System is NAD_1983_UTM_Zone_16N for this GSSHA Project
epsg = 26916

elev = gpd.GeoDataFrame()
line_3d = gpd.GeoDataFrame()
station = gpd.GeoDataFrame()

dist = 0.0
xy_coords = []

pos = int(0)

line_list = list(line.geometry)

# Setting up line 3d data frame
line_3d['Link'] = []
line_3d['Node'] = []
line_3d['geometry'] = []
line_3d.crs = CRS.from_epsg(epsg)

# Setting up station data frame
station['Link'] = []
station['Node'] = []
station['geometry'] = []

for xsec in line_list:

    x_coords = xsec.xy[0]
    y_coords = xsec.xy[1]

    npts = len(x_coords)

    link = line['Link'].loc[pos]
    node = line['Node'].loc[pos]

    elev['X'] = x_coords
    elev['Y'] = y_coords
    elev['Station'] = 0

    for i in range(0,npts):

        dx = abs(x_coords[0] - x_coords[i])
        dy = abs(y_coords[0] - y_coords[i])

        dist = math.sqrt(dx**2 + dy**2)

        elev['Station'].loc[i] = dist


# elev = gpd.GeoDataFrame(elev, geometry = gpd.points_from_xy(elev.X, elev.Y))


# Starting the Elevation Extract

#dem = rasterio.open(r'G:\Goodwin_Creek\GoodwinCreekFlow\GoodwinCreekFlow\GoodwinCreekGIS\elev.tif', mode = 'r')

    elev['Elevation'] = 0
    dem_data = []

    for index, row in elev.iterrows():

        row, col = dem.index(row['X'], row['Y'])
        dem_read = dem.read(1)
        dem_data.append(round(dem_read[row, col],3))

    elev['Elevation'] = dem_data
  
    elev = gpd.GeoDataFrame(elev, geometry = gpd.points_from_xy(elev.X, elev.Y, elev.Elevation))

#    print(elev)
#    print(len(elev))
#    quit()

    temp_xyz = []
    temp_station_z = []

    for i in range(0,npts):
        x_y_z = (elev['X'].loc[i], elev['Y'].loc[i], elev['Elevation'].loc[i])
        station_z = (elev['Station'].loc[i], elev['Elevation'].loc[i])
        temp_xyz.append(x_y_z)
        temp_station_z.append(station_z)
 
    temp_xyz_geo = LineString(temp_xyz)
    temp_station_z_geo = LineString(temp_station_z)

    line_3d.loc[pos] = [link, node, temp_xyz_geo]
    station.loc[pos] = [link, node, temp_station_z_geo]

    pos = pos + 1

line_3d.to_file(outfp)
station.to_file(outfp1)

#plt.plot(elev['Station'], elev['Elevation'], color = 'brown')
#plt.show()




#%%


