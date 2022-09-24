## see line 34 to continue. Also trying to verify plotToFarObnject works, and print to csv file works as expected

import picar_4wd as fc
#import obstacleAvoidance as manuver
import time
import math
import numpy as np
import pandas as pd
import python_astar as astar

# global variables
us = fc.Ultrasonic(fc.Pin('D8'), fc.Pin('D9'))
npMap = np.zeros((100, 100))

# Picar scans it's environment & plots to numpy Map
# @param step: degrees it steps between readings of ultrasonic sensor
def scanAndPlot(step = 18):
    global npMap
    npMap = np.zeros((100, 100))
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
            if (dist > 0 and dist < 100):
                readings.append((angle, dist))
            elif (dist > 100): # Not sure this is needed. Currently getting error ERROR: index 109 is out of bounds for axis 0 with size 100
                readings.append((angle, 100))
            else: # If ultrasonic has distance reading exception, try 3 times
                while (tryAgainCount > 0):
                    dist = fc.get_distance_at(angle)
                    tryAgainCount -= 1
                    if (dist >= 0):
                        readings.append((angle, dist))
                        break
                if (dist < 0): # if a distance was not found, assume no object is there
                    print("no obj at angle: {0}".format(angle))
                    # readings.append((angle, 100))
            angle += step
        printReadings(readings)
        printXY_Readings(readings)

        ### PLOT ###
        print("ploting objects to map...")

        # print euclidian distance between points for debugging
        # for i in range(0, len(readings)-1):
        #     print("Euclidian Distance: " + str(euclidDist(readings[i], readings[i+1])))

        # get distance between points, if there is an object, plot into map
        readings = polarToCart(readings)
        # print(readings)
        for i in range(0, len(readings)-1):
            # print("Euclidian Distance: " + str(euclidDist(readings[i], readings[i+1])))
            if (identifyObstacles(readings[i], readings[i+1])):
                # print("object detected")
                plotNoDriveZone(readings[i], readings[i+1], 2)
            else:
                plotNoDriveZone(readings[i], readings[i], 1)
        csvMap = npMap.astype(int)
        print_npMap(csvMap)
        coords = astar.a_star_alg((50, 0), (65,10), 'manhattan', csvMap)

        #4: generate ordered list of actions
        actionQueue = astar.actions(coords)
        print(actionQueue)

        return csvMap
        
    except Exception as e:
        fc.stop()
        print("ERROR: " + str(e))

#convert polar coordinates to cartesian coordinates
def get_XY(polarCord):
    theta = polarCord[0] + 90
    r = polarCord[1]
    x = round((r * math.cos(math.radians(theta)))/5) + 50
    y = round((r * math.sin(math.radians(theta)))/5)
    return (x, y)

# calculate the distance between two points
# if the number falls under an object detection threshold return true, else false
def identifyObstacles(p1, p2):
    objectDetectionThreshold = 4
    if (euclidDist(p1, p2) <= objectDetectionThreshold):
        return True
    else:
        return False

# point 1 and point 2 are two opposite corners of a no drive zone. Fill zone with 1s
def plotNoDriveZone(p1, p2, buffer):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    minX = max(min(x1, x2) - buffer, 0)
    maxX = min(max(x1, x2) + buffer, 99)
    minY = max(min(y1, y2) - buffer, 0)
    maxY = min(max(y1, y2) + buffer, 99)
    for i in range(minX, maxX):
        for j in range(minY, maxY):
            npMap[i, j] = 1

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

# Print the numpy Map of obstacles
def print_npMap(csvMap):
    # np.savetxt("data/npMap.csv", csvMap, delimiter=",")
    pd.DataFrame(csvMap).to_csv("data/npMap.csv", header=None, index=None)



# plot (x, y) coordinates into map  --  depreciated?
def plot_XY(cordinates, map):
    x = cordinates[0]
    y = cordinates[1]
    npMap[x, y] = 1


    
# return the distance between 2 points 
def euclidDist(p1, p2):
    return round(math.sqrt((p2[0] - p1[0])**2+(p2[1] - p1[1])**2), 2)



# plot distance object onto map. Add buffer. fill with 1s
def plotFarObject(obj):
    x = obj[0]
    y = obj[1]
    if (x == 0 or x == 99 or y == 0 or y == 99):
        print("plotFarObject warning: index out of bounds")
    for i in range(x-1, x+1):
        for j in range(y-1, y+1):
            npMap[i, j] = 1;
    
# convert readings (angle, dist) to (x, y)
def polarToCart(readings):
    return[get_XY(i) for i in readings]

scanAndPlot()