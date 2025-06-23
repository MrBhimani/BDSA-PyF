#!/usr/bin/ env python   
import serial
import struct
import time
import numpy as np
import cv2

Lower = (11, 100, 100)        #Orange Color Lower RGB values
Upper = (20, 255, 255)        #orange Color Upper RGB values

#Lower = (90, 90, 90)           #Blue Color Lower RGB values
#Upper = (110, 255, 255)        #Blue Color Upper RGB values

#Lower = (25, 110, 90)        #Yellow Color Lower RGB values
#Upper = (40, 255, 255)        #Yellow Color Upper RGB values

camera = cv2.VideoCapture(0)
camera.set(3,480.0)
camera.set(4,320.0)
camera.set(5,15)

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
time.sleep(2)


while True:
    ret, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=1) 
    mask = cv2.dilate(mask, None, iterations=6)
            
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    for c in contours:
        M = cv2.moments(c)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        
        if cv2.contourArea(c) > 900:
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Bird", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0,0 ), 2)
            cv2.circle(frame, (cx, cy), 8, (0,255,0), -1)
            ax = -0.12*(cx)+58.6
            ay =  0.11*(cy)+0.89 
            ax = (int(ax))
            ay = (int(ay))
            print("cx:",cx,"cy:",cy,"servo1:",ax,"servo2:",ay)
            arduino.write(struct.pack('>BB', ax,ay))
            
########### OUTPUT ##############               
    cv2.imshow("Frame", frame)
    #cv2.imshow("Rest", res)
    #cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()


