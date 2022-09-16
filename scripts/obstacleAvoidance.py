import picar_4wd as fc
import time
import random
print("testing")
print(fc.get_distance_at(0))



#reference
def func1():
    try:
        speed4 = fc.Speed(25)
        speed4.start()
        x = 0
        fc.forward(10)
        for i in range(20):
            time.sleep(0.1)
            speed = speed4()
            x += speed * .01
            dist = fc.get_distance_at(0)
            if dist < 30:
                fc.stop()
                fc.backward(10)
            elif dist > 30:
                fc.stop()
                fc.forward(10) 
            print(fc.get_distance_at(0))
        print(x)
        speed4.deinit()
        fc.stop()
    except Exception as e:
        fc.stop()
        print("ERROR: " + e)


def backup(currTime, speed, backTime, interval):
    fc.stop()
    time.sleep(.5)
    fc.backward(speed)
    print("backing up")
    totalTime = currTime + backTime
    while currTime < totalTime:
        # print(currTime)
        time.sleep(interval)
        currTime += interval
    fc.stop()
    return currTime

def turn(currTime, speed, interval):
    fc.stop()
    duration = 1 # how long it turns for
    coin = random.choice([1, 2, 3])
    print("turning")
    if coin == 1:
        fc.turn_left(speed)
    else:
        fc.turn_right(speed)
    print(duration)
    totalTime = currTime + duration
    while (currTime < totalTime):
        time.sleep(interval)
        # print("turning")
        currTime += interval
    fc.stop()
    return currTime

def objectDetected():
    dist = fc.get_distance_at(0)
    # print("Servo output: " + str(dist))
    return(dist < 30 and dist > 0)

# main
def environmentScanning(carSpeed, timer, interval):
    try :
        speed4 = fc.Speed(25)
        speed4.start()

        #start forward movement
        fc.forward(carSpeed)
        x = 0
        #perform actions every .1 second
        i = 0
        while i < timer:
            # print(i)
            time.sleep(interval)
            
            #detect objects in front
            if (objectDetected()):
                # print("object detected")
                i = backup(i, carSpeed/2, 1, interval)
                i = turn(i, carSpeed/2, interval)
                fc.forward(carSpeed)
            i += interval
        print("Done driving")
        speed4.deinit()
        fc.stop()
    except Exception as e:
        fc.stop()
        print("ERROR: " + str(e))
        return
    

# environmentScanning(25 , 10, .1)
# fc.stop()


us = fc.Ultrasonic(fc.Pin('D8'), fc.Pin('D9'))


def swivel():
    start = -90
    end = 90

    curr = start

    readings = []
    while curr <= end:
        #store reading then increment
        fc.servo.set_angle(curr)
        time.sleep(.5)
        dist = us.get_distance()
        # while dist == -2:
        #     dist = fc.get_distance_at(curr)
        readings.append([(curr, dist)])
        curr+= 10
    print(readings)
        


swivel()
# print(fc.get_distance_at(-90))
# print(fc.get_distance_at(-80))
# print(fc.get_distance_at(0))
# print(fc.get_distance_at(45))
# print(fc.get_distance_at(90))