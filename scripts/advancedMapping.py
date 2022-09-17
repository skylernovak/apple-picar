import picar_4wd as fc
#import obstacleAvoidance as manuver
import time
import math
import numpy as np
print("Advanced Mapping")

# global variables
us = fc.Ultrasonic(fc.Pin('D8'), fc.Pin('D9'))

# Picar scans it's environment. 
# @param step: degrees it steps between readings of ultrasonic sensor
def scanAndPlot(step = 18):
    try:
        start = -90
        end = 90
        readings = []

        ### SCAN ###

        #store reading then increment
        print("scanning surroundings...")
        angle = start
        while angle <= end:
            tryAgainCount = 3
            dist = fc.get_distance_at(angle)
            time.sleep(.5)  # give servo time to move into position before taking ultrasonic reading
            if (dist > 0):
                readings.append((angle, dist))
            else: # If ultrasonic has distance reading exception, try 3 times
                while (tryAgainCount > 0):
                    dist = fc.get_distance_at(angle)
                    tryAgainCount -= 1
                    if (dist >= 0):
                        readings.append((angle, dist))
                        break
                if (readings.index(len(readings))[1] < 0): # if a distance was not found, assume no object is there
                    readings.append((angle, 100))
            angle += step
        # print("Scan readings: " + str(readings))
        printReadings(readings)
        printXY_Readings(readings)

        ### PLOT ###

        print("ploting objects to map...")

        # print euclidian distance between points for debugging
        for i in range(0, len(readings)-1):
            print("Euclidian Distance: " + str(euclidDist(readings[i], readings[i+1])))

        # get distance between points
        # if there is an object, plot into map
            # how to plot to map?
            # use logic from print for loop above
            # will have 2 points, pass both to plot_XY(p1, p2)   
        
    except Exception as e:
        fc.stop()
        print("ERROR: " + str(e))

# print readings from Ultrasonic sensor & format them
def printReadings(readings):
    print("\n\t(ANGLE, DIST)");
    for i in readings:
        print("\t" + str(i))

# print readings from Ultrasonic sensor & format them as (x, y) coordinates
def printXY_Readings(readings):
    print("\n\t(X, Y)");
    for i in readings:
        print("\t" + str(get_XY(i)))

#convert polar coordinates to cartesian coordinates
def get_XY(polarCord):
    theta = polarCord[0] + 90
    r = polarCord[1]
    x = round(r * math.cos(math.radians(theta)))
    y = round(r * math.sin(math.radians(theta)))
    return (x, y)

# plot (x, y) coordinates into map
def plot_XY(cordinates, map):
    x = cordinates[0]
    y = cordinates[1]
    npMap = np.zeros((100, 100)) # move to gloabl variables?
    npMap[x, y] # = 1?
    # fill in all values in between with 1, or add logic to fill boxes

# return the distance between 2 points 
def euclidDist(p1, p2):
    return round(math.sqrt((p2[0] - p1[0])**2+(p2[1] - p1[1])**2), 2)

# calculate the distance between two points
# if the number falls under an object detection threshold return true, else false
def identifyObstacles(p1, p2):
    objectDetectionThreshold = 20
    if (euclidDist(p1, p2) <= objectDetectionThreshold):
        return True;
    else:
        return False;


scanAndPlot()