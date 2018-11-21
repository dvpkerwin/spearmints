import PID
import time
import os.path
import max6675
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(13,IO.OUT)
herb = IO.PWM(13,100)
herb.start(0)

relay = 6
IO.setup(relay,IO.OUT)
IO.output(relay,IO.LOW)

heatConc = IO.PWM(relay,100)
heatConc.start(0)



targetT = 180
P = 7
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

cs0_pin = 8
cs1_pin = 7
clock_pin = 11
data_pin = 9
units = "c"
tcd = max6675.MAX6675(cs0_pin, clock_pin, data_pin, units)
tch = max6675.MAX6675(cs1_pin,clock_pin, data_pin, units)

def readConfig ():
    global targetT
    with open ('/tmp/pid.conf', 'r') as f:
        config = f.readline().split(',')
        pid.SetPoint = float(config[0])
        targetT = pid.SetPoint
        pid.setKp (float(config[1]))
        pid.setKi (float(config[2]))
        pid.setKd (float(config[3]))

def createConfig ():
    if not os.path.isfile('/tmp/pid.conf'):
        with open ('/tmp/pid.conf', 'w') as f:
            f.write('%s,%s,%s,%s'%(targetT,P,I,D))

createConfig()

tempSamplesFlower = [23,23,3]
def updateAvgTempFlower (temp):
    global tempSamplesFlower
       
    for j in range (0,2):
        tempSamplesFlower[j] = tempSamplesFlower[j+1]
        
    tempSamplesFlower[2] = temp 
    
def getAvgTempFlower ():
    global tempSamplesFlower
    total = 0
    for z in range (0,3):
        total = total + tempSamplesFlower[z]

    avg = total / 3
    return avg

running = True
onethirdcnt = 0

while running:
    #readConfig()
    #read temperature data
    try:
        #tempH = tch.get()
        tempD = tcd.get()
    except MAX6675Error as e:
        #tempH = "Error: "+ e.value
        tempD = "Error: " + e.value
        running = False
    #print("tempH: {} ".format(tempH))
    print("tempD: {} ".format(tempD))
    #updateAvgTempFlower(tempH)
    updateAvgTempFlower(tempD)
    avgTemp = getAvgTempFlower()
    print ("  avgTemp: {}".format(avgTemp))
    
    pid.update(avgTemp)
    targetPwm = pid.output
    targetPwm = max(min( int(targetPwm), 100 ),0)

    print "Target: %.1f C | Current: %.1f C | PWM: %s %%"%(targetT, avgTemp, targetPwm) 
    
    # Set PWM expansion channel 0 to the target setting
    #herb.ChangeDutyCycle(targetPwm);
    #if targetPwm >= 78:
        #if onethirdcnt >= 2:
            #IO.output(relay,IO.HIGH)
            #onethirdcnt = 0
        #else:
            #onethirdcnt += 1
            #IO.output(relay,IO.LOW)
    #else:
        #IO.output(relay,IO.LOW)
        #onethirdcnt = 0
    heatConc.ChangeDutyCycle (targetPwm)
    time.sleep(1)
    
print ("shutting down PWM")
herb.ChangeDutyCycle(0)
print ("PWM is off, end program")
