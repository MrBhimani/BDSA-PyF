#!/usr/bin/ env python                              # For any OS systems
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


tilt = 17
pan = 27


import numpy as np  # The fundamental package for scientific computing.
import cv2          # Library of Python bindings designed to solve computer vision problem

Lower = (11, 100, 100)        #Orange Color Lower RGB values
Upper = (20, 255, 255)        #orange Color Upper RGB values

camera = cv2.VideoCapture(0)

GPIO.setup(tilt, GPIO.OUT) #  TILT
GPIO.setup(pan, GPIO.OUT) #  PAN

def setServoAngle(servo, angle):
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.2)
	pwm.stop()
	
while True:
    ret, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=1) 
    
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    for c in contours:
        if cv2.contourArea(c) > 600:
            (x,y,w,h) = cv2.boundingRect(c)             
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Birtd", (x, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0,0 ), 2)
            ###############################
            cx = (x+w)/2
            cy = (y+h)/2
            #ax = -0.26*(cx)+84.2   #x angle 30--320
            #ay = 0.18*(cy)-4.4     #y angle 30--240
            ax = -0.13*(cx)+42.6     #x angle 30--320 %40
            ay = 0.15*(cy)-3.5     #y angle 30--240 %30
            ax = (int(ax))
            ay = (int(ay))
            setServoAngle(tilt,ay)
            setServoAngle(pan,ax)
            print("cx:",cx)
            print("          cy:",cy)
            print("                   AX:",ax)
            print("                            AY:",ay)
 

###############################  
    cv2.imshow("Frame", frame)
   
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()



