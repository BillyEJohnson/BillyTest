#%%
import math

def overbank(xcoordinates, ycoordinates, width, increment, link):

    xlink = link
    inc = increment

    npts = len(xcoordinates)

    angle = [0]
    xsec_angle = [0]
    ave_angle = [0]
    ave_profile = [0]
    quad_flag = [0]
    ave_quad_flag = [0]
    lob_dx = []
    lob_dy = []
    rob_dx = []
    rob_dy = []
    overbank_section = []
    temp1 = []

    
    for i in range(0,npts-1):

        dx = float(xcoordinates[i+1]) - float(xcoordinates[i])
        dy = float(ycoordinates[i+1]) - float(ycoordinates[i])

        if (dx == 0.0):
            dx = 0.0001
        if (dy == 0.0):
            dy = 0.0001

        angle1 = math.degrees(math.atan(dy/dx))


# Quadrant I - 0 degrees to 90 degrees

        if (dx > 0.0 and dy > 0.0):
            ave_angle1 = angle1 + 90
            angle1 = angle1
            xsec_angle1 = 180 - ave_angle1
            quad_flag1 = 1

# Quadrant II - 270 degress to 360 degress
 
        if (dx > 0.0 and dy < 0.0):
            angle1 = 360 + angle1
            ave_angle1 = angle1 + 90 - 360
            xsec_angle1 = ave_angle1
            quad_flag1 = 2

# Quadrant III - 180 degrees to 270 degrees
 

        if (dx < 0.0 and dy < 0.0):
            angle1 = 180 + angle1
            ave_angle1 = angle1 + 90
            xsec_angle1 = 360 - ave_angle1
            quad_flag1 = 3

# Quadrant IV - 90 degrees to 180 degrees     

        if (dx < 0.0 and dy > 0.0):
            angle1 = 180 - abs(angle1)
            ave_angle1 = angle1 + 90
            xsec_angle1 = ave_angle1 - 180
            quad_flag1 = 4

        angle.append(angle1)
        ave_angle.append(ave_angle1)
        xsec_angle.append(xsec_angle1)
        quad_flag.append(quad_flag1)

    for i in range(0,npts):

        if (i == 0):

            if (quad_flag[1] == 1):
                l_x = -1
                l_y = 1

            if (quad_flag[1] == 2):
                l_x = 1
                l_y = 1

            if (quad_flag[1] == 3):
                l_x = 1
                l_y = -1

            if (quad_flag[1] == 4):
                l_x = -1
                l_y = -1


            l_x = l_x * math.cos(xsec_angle[1]*3.1415927/180)*width
            l_y = l_y * math.sin(xsec_angle[1]*3.1415927/180)*width
            r_x = -1 * l_x
            r_y = -1 * l_y

            lob_dx.append(l_x)
            lob_dy.append(l_y)
            rob_dx.append(r_x)
            rob_dy.append(r_y)
        
        if (i == npts -1):

            if (quad_flag[i] == 1):
                l_x = -1
                l_y = 1

            if (quad_flag[i] == 2):
                l_x = 1
                l_y = 1

            if (quad_flag[i] == 3):
                l_x = 1
                l_y = -1

            if (quad_flag[i] == 4):
                l_x = -1
                l_y = -1

            l_x = l_x * math.cos(xsec_angle[npts-1]*3.1415927/180)*width
            l_y = l_y * math.sin(xsec_angle[npts-1]*3.1415927/180)*width
            r_x = -1 * l_x
            r_y = -1 * l_y

            lob_dx.append(l_x)
            lob_dy.append(l_y)
            rob_dx.append(r_x)
            rob_dy.append(r_y)

        if (i > 0 and i < npts -1):

            if (quad_flag[i] == 1):
                l_x = -1
                l_y = 1

            if (quad_flag[i] == 2):
                l_x = 1
                l_y = 1

            if (quad_flag[i] == 3):
                l_x = 1
                l_y = -1

            if (quad_flag[i] == 4):
                l_x = -1
                l_y = -1

            l_x = l_x * math.cos(xsec_angle[i]*3.1415927/180)*width
            l_y = l_y * math.sin(xsec_angle[i]*3.1415927/180)*width
            r_x = -1 * l_x
            r_y = -1 * l_y

            lob_dx.append(l_x)
            lob_dy.append(l_y)
            rob_dx.append(r_x)
            rob_dy.append(r_y)

        l_x = float(xcoordinates[i]) + l_x
        l_y = float(ycoordinates[i]) + l_y
        r_x = float(xcoordinates[i]) + r_x
        r_y = float(ycoordinates[i]) + r_y

# This Section averages the Overbank Cross Section Profile from U/S to D/S

    for i in range (0, npts):
           
        if (i == 0):

            ave_angle[i] = ave_angle[1]
            xsec_angle[i] = xsec_angle[1]
            ave_quad_flag[i] = quad_flag[1]

            if (ave_quad_flag[i] == 1):
                l_x = -1
                l_y = 1

            if (ave_quad_flag[i] == 2):
                l_x = 1
                l_y = 1

            if (ave_quad_flag[i] == 3):
                l_x = 1
                l_y = -1

            if (ave_quad_flag[i] == 4):
                    l_x = -1
                    l_y = -1
            
        if(i == npts-1):

            ave_angle[i] = ave_angle[i]
            xsec_angle[i] = xsec_angle[i]
            ave_quad_flag.append(quad_flag[i])

            if (ave_quad_flag[i] == 1):
                l_x = -1
                l_y = 1

            if (ave_quad_flag[i] == 2):
                l_x = 1
                l_y = 1

            if (ave_quad_flag[i] == 3):
                l_x = 1
                l_y = -1

            if (ave_quad_flag[i] == 4):
                l_x = -1
                l_y = -1

        if (i > 0 and i < npts-1):

            ave_angle[i] = (ave_angle[i] + ave_angle[i+1])/2

            if (ave_angle[i] == 0.0):
                ave_angle[i] == 0.0001
            if (ave_angle[i] == 90.0):
                ave_angle[i] = 90.0001
            if (ave_angle[i] == 180.0):
                ave_angle[i] == 180.0001
            if (ave_angle[i] == 270.0):
                ave_angle[i] == 270.0001
            if (ave_angle[i] == 360.0):
                ave_angle[i] == 0.0001

            if ((ave_angle[i] - 90) > 0):
                ave_profile.append(ave_angle[i] - 90)
            else:
                ave_profile.append(360 + (ave_angle[i] - 90))

            if (ave_profile[i] >0.0 and ave_profile[i]<= 90.0):
                ave_quad_flag.append(1)
                xsec_angle[i] = 180 - ave_angle[i]
                l_x = -1
                l_y = 1

            if (ave_profile[i] >270.0 and ave_profile[i]<= 360.0):
                ave_quad_flag.append(2)
                xsec_angle[i] = ave_angle[i]
                l_x = 1
                l_y = 1

            if (ave_profile[i] >180.0 and ave_profile[i]<= 270.0):
                ave_quad_flag.append(3)
                xsec_angle[i] = 360 - ave_angle[i]
                l_x = 1
                l_y = -1

            if (ave_profile[i] >90.0 and ave_profile[i]<= 180.0):
                ave_quad_flag.append(4)
                xsec_angle[i] = ave_angle[i] - 180
                l_x = -1
                l_y = -1

        l_x = l_x * math.cos(xsec_angle[i]*3.1415927/180)*width
        l_y = l_y * math.sin(xsec_angle[i]*3.1415927/180)*width
        r_x = -1 * l_x
        r_y = -1 * l_y

        if (i == npts-1):

            dx1 = float((xcoordinates[i-1] - xcoordinates[i]))
            dy1 = float((ycoordinates[i-1] - ycoordinates[i]))

            dx1 = dx1 + 0.0001

            slope = dy1/dx1

# Moving the last overbank cross section back by a specified distance 

            move = 0.1 * dx1

            x = xcoordinates[i] + move
            y = ycoordinates[i] + slope * (x-xcoordinates[i])

            l_x = x + l_x
            l_y = y + l_y
            r_x = x + r_x
            r_y = y + r_y

        else:

            x = xcoordinates[i]
            y = ycoordinates[i]

            l_x = x + l_x
            l_y = y + l_y
            r_x = x + r_x
            r_y = y + r_y

#  Computing the Incremental Points for each Overbank Cross Section

#  Left Overbank Computations

        temp1 = [(l_x, l_y)]

        slope = (y - l_y)/(x - l_x)

        num_inc = int(width / inc)

        dx1 = (x - l_x)/num_inc

        for i in range(1, num_inc):
            x1 = l_x + i * dx1
            y1 = l_y + slope * (x1 - l_x)

            x_y = (x1, y1)
            temp1.append(x_y)

#  Right Overbank Computations
        
        slope = (r_y - y)/(r_x - x)

        dx1 = (r_x - x)/num_inc

        for i in range(1, num_inc):
            x1 = x + i * dx1
            y1 = y + slope * (x1 - x)

            x_y = (x1, y1)
            temp1.append(x_y)

        overbank_section.append(temp1)

    return overbank_section 


#%%

