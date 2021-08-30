#%%
from shapely.geometry import LineString, MultiLineString, Point, Polygon, shape
from shapely.ops import split
from Overbank import overbank
import matplotlib.pyplot as plt
import numpy as np
import math
import geopandas as gpd
from pyproj import CRS
import os
import rasterio
from rasterio.features import shapes

work_path = r"C:\Goodwin_Creek\GoodwinCreekFlow\GoodwinCreekFlow"

in_chan = "Goodwin_Creek_BEJ.cif"
outfp = "Goodwin_Creek_Channels.shp"
outfp1 = "Goodwin_Creek_Xsecs.shp"

in_chan = os.path.join(work_path, in_chan)
outfp = os.path.join(work_path, outfp)
outfp1 = os.path.join(work_path, outfp1)

# Coordinate System is NAD_1983_UTM_Zone_16N for this GSSHA Project
epsg = 26916

# Setting up Data Lists for eventually importing into the GeoDataFrame
Link = []
DS_Link = []
US_Link_1 = []
US_Link_2 = []
XSEC_Pts = []
XSEC_Lines = []
Line_X = []
Line_Y = []
temp = []
Overbank_Section = []

# Setting the Cross Section Overbank Width for each side of the channel
xsec_width = 150
increment = 10

# Setting up a Blank GeoDataFrame for holding the GSSHA Channel Information
#
# Note: Future versions of Python will not support setting the CRS before adding the 'geometry' column 
# hence the CRS is set down below after the 'geometry' column was setup
chan_data = gpd.GeoDataFrame()
xsec_data = gpd.GeoDataFrame()

# Starting to Read the GSSHA Channel Input File 

with open(in_chan) as in_chan_file:
    lines = in_chan_file.readlines()

    line_count = 0
    pos = 0
    xsec_pts_flag = 0

    for line in lines:
        line = line.rstrip()
        values = line.split()
        line_count = line_count + 1

        max_values = len(values)

        if max_values > 0:

            if values[0] == 'LINKS':
                max_links = values[1]

            if values[0] == 'MAXNODES':
                max_nodes = values[1]

            if values[0] == 'CONNECT':
                link_num = int(values[1])
                Link.append(link_num)
                DS_Link.append(values[2])

                values[3] = int(values[3])

                if values[3] == 0:
                    US_Link_1.append(0)
                    US_Link_2.append(0)

                if values[3] == 1:
                    values[4] = int(values[4])
                    US_Link_1.append(values[4])
                    US_Link_2.append(0)
  
                if values[3] == 2:
                    values[4] = int(values[4])
                    values[5] = int(values[5])
                    US_Link_1.append(values[4])
                    US_Link_2.append(values[5])

            if (values[0] == 'LINK'):
                Link_Flag = int(values[1])
                XSEC_Pts.append([])
                Line_X.append([])
                Line_Y.append([])

            if (values[0] == 'TRAPEZOID'):
                Chan_Type = 1
                Max_XSEC_Pts = int(4)
                Pt_Count = 1

            if (values[0] == 'BREAKPOINT'):
                Chan_Type = 2
                
            if (values[0] == 'NPAIRS'):
                Max_XSEC_Pts = int(values[1])
                Pt_Count = 1

            if (values[0] == 'NODES'):
                Max_Nodes = values[1]
                Node_Count = 1

            if (values[0] == 'X_Y' and Pt_Count <= Max_XSEC_Pts):
                line_pos = Link_Flag - 1
                x = float(values[1])
                y = float(values[2])
                Pt_Count = Pt_Count + 1

                if (Pt_Count > Max_XSEC_Pts):
                    Pt_Count = 1

            if (values[0] == 'ELEV'):
                elev = float(values[1])
                x_y_z = (x, y, elev)
                XSEC_Pts[line_pos].append(x_y_z)
                Line_X[line_pos].append(x)
                Line_Y[line_pos].append(y)

chan_data['Link'] = Link
chan_data['DS_Link'] = DS_Link
chan_data['US_Link_1'] = US_Link_1
chan_data['US_Link_2'] = US_Link_2

XSEC_Lines = MultiLineString(XSEC_Pts)

chan_data['geometry'] = XSEC_Lines
chan_data.crs = CRS.from_epsg(epsg)

line_pos = int(0)

for line in XSEC_Lines:
    chan_data.at[line_pos, 'geometry'] = line
    line_pos = line_pos + 1

chan_data.to_file(outfp)

line_length = len(Line_X)

line_pos = int(0)

xsec_data['Link'] = []
xsec_data['Node'] = []
xsec_data['geometry'] = []
xsec_data.crs = CRS.from_epsg(epsg)

for i in range(0, line_length):

    x = Line_X[i]
    y = Line_Y[i]

    xlink = int(i+1)

    Overbank_Section = overbank(x, y, xsec_width, increment, xlink)

    maxlines = len(Overbank_Section)

    for j in range (0, maxlines):

        ovb_line = []
        xnode = int(j+1)

        for pts in Overbank_Section[j]:
            ptsx = float(pts[0])
            ptsy = float(pts[1])
            ptsx_y = [ptsx,ptsy]

            ovb_line.append(ptsx_y)

        ovb_line_geo = LineString(ovb_line)

        xsec_data.loc[line_pos] = [xlink, xnode, ovb_line_geo]

        line_pos = line_pos + 1

xsec_data.to_file(outfp1)



 



#%%