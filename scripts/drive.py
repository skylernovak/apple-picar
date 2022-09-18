import getopt
import time
import advancedMapping
import python_astar as astar
import picar_4wd as fc
from collections import deque
import sys
#globals

#distance counter
distTilNextScan = 25

#total distance traveled in x and y directions
currLocation = [0, 0]

speed4 = fc.Speed(25)

def driveToTarget(target):
    global speed4
    global distTilNextScan
    global currLocation
    scanCounter = 0
    stepCounter = 0
    coords = []
    actionQueue = []

    speed4.start()
    try :
        while True:
            if (scanCounter <= 0):
                #time to rescan
                #stop the car
                fc.stop()    

                #0: update currLocation
                if coords:
                    currLocation[0] += coords[stepCounter][0]
                    currLocation[1] += coords[stepCounter][1]
                print("currLocation=({0})".format(currLocation))
                stepCounter = 0       

                #2a: reset car direction
                print("resetting position to scan")
                resetAction = astar.resetToNorth()
                runActions(resetAction)
                #2b: scan and plot obstacles
                obstacleMap = advancedMapping.scanAndPlot()

                #1: calculate new target - slope * distTilNextScan
                xDist = target[0] - currLocation[0]
                yDist = target[1] - currLocation[1]
                slope = [xDist/(xDist + yDist), yDist/(xDist + yDist)]
                print("slope:{0},{1}".format(xDist, yDist))
                tempTarget = (round(slope[0] * distTilNextScan), round(slope[1] * distTilNextScan))

                if (advancedMapping.euclidDist((0,0), (xDist, yDist)) <= advancedMapping.euclidDist((0,0), tempTarget)):
                    tempTarget = (xDist + 50, yDist)
                else:
                    newTargetCount = 1
                    recalcTempTarget = tempTarget
                    while (obstacleMap[recalcTempTarget[0]+50, recalcTempTarget[1]] == 1):
                        newTargetCount += .25
                        recalcTempTarget = (round(tempTarget[0] * newTargetCount), round(tempTarget[1] * newTargetCount))
                    tempTarget = (recalcTempTarget[0] + 50, recalcTempTarget[1])

                #3: calculate a_star
                print(tempTarget)
                coords = astar.a_star_alg((50, 0), tempTarget, 'manhattan', obstacleMap)

                #4: generate ordered list of actions
                actionQueue = astar.actions(coords)

                #5: reset distTilNextScan
                scanCounter = distTilNextScan
            elif len(actionQueue) == 0:
                fc.stop()
                print("Reached Final Destination")
                return
            else:
                actions = actionQueue.pop(0)
                runActions(actions)
                stepCounter += 1
                scanCounter -= 1
    except Exception as e:
        speed4.deinit()
        fc.stop()
        raise Exception(e)

def runActions(actions):
    for action in actions:
        if action == "LEFT":
            turnLeft()
            print("LEFT")
        elif action == "RIGHT":
            turnRight()
            print("RIGHT")
        else :
            goForward()
            print("FORWARD")

def turnRight():
    fc.turn_right(50)
    time.sleep(spinTime)
    fc.stop()
    

def turnLeft():
    fc.turn_left(50)
    time.sleep(spinTime)
    fc.stop()

def goForward():
    fc.forward(10)
    time.sleep(forwardTime)

# driveToTarget((100, 200))
xdestination = 0
ydestination = 0
spinTime = 0
forwardTime = 0
def main(argv):
    global xdestination, ydestination, spinTime, forwardTime
    try:
        opts, args = getopt.getopt(argv, "x:y:t:f:", ["xdest=","ydest=","sTime=", "fTime="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-x':
            xdestination = int(arg)
        elif opt == '-y':
            ydestination = int(arg)
        elif opt =='-t':
            spinTime = float(arg)
        elif opt == '-f':
            forwardTime = float(arg)
    print("destination:({0}, {1})".format(xdestination,ydestination))
    print("spin time = {0}s".format(spinTime))
    print("forward time = {0}s".format(forwardTime))
    driveToTarget((xdestination, ydestination))
    # turnLeft()


if __name__ == "__main__":
    main(sys.argv[1:])



