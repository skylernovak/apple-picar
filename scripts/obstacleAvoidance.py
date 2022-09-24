import picar_4wd as fc
import time
import random
print("testing")
print(fc.get_distance_at(0))

def backup(speed):
    fc.stop()
    fc.backward(speed)
    time.sleep(.3)
    fc.stop()

def turn():
    fc.stop()
    if random.choice([1,2]) == 1:
        turnRight()
    else:
        turnLeft()


def turnRight():
    fc.turn_right(50)
    time.sleep(1.0)
    fc.stop()
    

def turnLeft():
    fc.turn_left(50)
    time.sleep(1.0)
    fc.stop()

def objectDetected():
    dist = fc.get_distance_at(0)
    print("Servo output: " + str(dist))
    return(dist < 20 and dist > 0)

# main
def environmentScanning(carSpeed, timer, interval):
    try :
        speed4 = fc.Speed(25)
        speed4.start()

        #start forward movement
        fc.forward(carSpeed)
        x = 0
        #perform actions every (interval) seconds
        i = 0
        while i < timer:
            # print(i)
            time.sleep(interval)
            
            #detect objects in front
            if (objectDetected()):
                print("object detected")
                backup(carSpeed/2)
                turn()
                fc.forward(carSpeed)
            i += interval
        print("Done driving")
        speed4.deinit()
        fc.stop()
    except Exception as e:
        fc.stop()
        print("ERROR: " + str(e))
        return

environmentScanning(20, 6, .1)