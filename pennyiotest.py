import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(19,IO.OUT)
IO.setup(26,IO.OUT)
IO.setup(13,IO.OUT)
IO.setup(6,IO.OUT)
IO.output(6,IO.LOW)

relay = 6
r1 = 22
g1 = 10
b1 = 5
r2 = 14
g2 = 17
b2 = 27
IO.setup(r1,IO.OUT)
IO.output(r1,IO.LOW)
IO.setup(g1,IO.OUT)
IO.output(g1,IO.LOW)
IO.setup(b1,IO.OUT)
IO.output(b1,IO.LOW)

IO.setup(r2,IO.OUT)
IO.output(r2,IO.LOW)
IO.setup(g2,IO.OUT)
IO.output(g2,IO.LOW)
IO.setup(b2,IO.OUT)
IO.output(b2,IO.LOW)

herb = IO.PWM(13,100)
herb.start(0)
fan = IO.PWM(26,100)
fan.start(0)
cool = IO.PWM(19,100)
cool.start(0)



while 1 :
  inputStr = input("on/off herb 1/2  cooling  3/4  fan 5/6  dab 7/8  allOff 0)")
  if inputStr==1:
       herb.ChangeDutyCycle(95);
  elif inputStr==2:
       herb.ChangeDutyCycle(0);
  elif inputStr==3:
       cool.ChangeDutyCycle(95);
  elif inputStr==4:
       cool.ChangeDutyCycle(0);
  elif inputStr==5:
       fan.ChangeDutyCycle(95);
  elif inputStr==6:
       fan.ChangeDutyCycle(0);
  elif inputStr==7:
       IO.output(relay,IO.HIGH)
  elif inputStr==8:
       IO.output(relay,IO.LOW)
  elif inputStr==11:
       IO.output(r1,IO.HIGH)
  elif inputStr==12:
       IO.output(r1,IO.LOW)
  elif inputStr==13:
       IO.output(g1,IO.HIGH)
  elif inputStr==14:
       IO.output(g1,IO.LOW)
  elif inputStr==15:
       IO.output(b1,IO.HIGH)
  elif inputStr==16:
       IO.output(b1,IO.LOW)

  elif inputStr==21:
       IO.output(r2,IO.HIGH)
  elif inputStr==22:
       IO.output(r2,IO.LOW)
  elif inputStr==23:
       IO.output(g2,IO.HIGH)
  elif inputStr==24:
       IO.output(g2,IO.LOW)
  elif inputStr==25:
       IO.output(b2,IO.HIGH)
  elif inputStr==26:
       IO.output(b2,IO.LOW)
  elif inputStr==0:
       herb.ChangeDutyCycle(0);
       fan.ChangeDutyCycle(0);
       cool.ChangeDutyCycle(0);
       IO.output(6,IO.LOW)
  else:
       print 'Input was invalid'



