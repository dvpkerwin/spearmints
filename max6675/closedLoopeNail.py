#!/usr/bin/python
# Copyright 2018 Denver Easy Inc.  All rights reserved.

# This file contains test code for closed loop enail with max6675 thermocouple sensor

import max6675
import time
import RPi.GPIO as IO

IO.setmode(IO.BCM)
IO.setwarnings(False)
pinRelay = 6
IO.setup(pinRelay,IO.OUT)
IO.output(pinRelay,IO.LOW)

print ("yay")
# default example
cs_pin = 8
clock_pin = 11
data_pin = 9
units = "c"
thermocouple = max6675.MAX6675(cs_pin, clock_pin, data_pin, units)
running = True

targetTemp = 220

PHASE_BRon = 1
PHASE_BRoff = 1
PHASE_LRon = 1
PHASE_LRoff = 3
PHASE_HoverOn = 1
PHASE_HoverOff = 9


sampleEnailTemp = 23
phaseOnValue = PHASE_BRon
phaseOffValue = PHASE_BRoff
phaseState = 0

phasingCount = 0

def toggleEnailPhase ():
  global phasingCount
  global phaseState
  if phaseState == 0:
    phaseState = 1
    IO.output(pinRelay,IO.HIGH)
    phasingCount = 0
  elif phaseState == 1:
    phaseState = 0
    IO.output(pinRelay,IO.LOW)
    phasingCount = 0
  else:
    IO.output(pinRelay,IO.LOW)
  print ("  toggle, phaseSt:{}".format(phaseState))

def setEnailPhaseSettings (sampleTemp):
  global phaseOnValue
  global phaseOffValue
  global phaseState
  diff = targetTemp - sampleTemp
  difint = int(diff)
  #print ("  phase set, diff: {}".format(diff) )
  
  if difint >= 30.0:
    phaseOnValue = PHASE_BRon
    phaseOffValue = PHASE_BRoff
    print ("  dif:{} phase BR".format(difint))
  elif 9 <= difint <= 29: 
    phaseOnValue = PHASE_LRon
    phaseOffValue = PHASE_LRoff
    print ("  dif:{} phase LR".format(difint))
  elif -9 <= difint <= 8:
    phaseOnValue = PHASE_HoverOn
    phaseOffValue = PHASE_HoverOff
    print ("  dif:{} phase Hover".format(difint))
  else:
    phaseState = -1
    print ("  dif:{} phase - turned off".format(difint))
    
  
  
print ("before running loop")
while(running):
    try:            
        print ("in loop now")
        try:
            tc = thermocouple.get()        
        except MAX6675Error as e:
            tc = "Error: "+ e.value
            running = False
        diffV = targetTemp - tc
        #print("tc: {} target:{}  diff:{}".format(tc,targetTemp,diffV))
        
        setEnailPhaseSettings(tc)
        phasingCount += 1
        if phaseState == 0:
          if phasingCount >= phaseOffValue:
            toggleEnailPhase()
        elif phaseState == 1:
          if phasingCount >= phaseOnValue:
            toggleEnailPhase()
        elif phaseState == -1:
            IO.output(pinRelay,IO.LOW)
        
        time.sleep(1)
    except KeyboardInterrupt:
        IO.output(pinRelay,IO.LOW)
        running = False
thermocouple.cleanup()