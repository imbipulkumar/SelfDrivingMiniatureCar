# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:53:56 2019

@author: BIPUL KUMAR
"""

from gpiozero import OutputDevice, PWMOutputDevice
import curses
import cv2

video=cv2.VideoCapture("http://192.168.42.129:8080/video")

motSP = OutputDevice(2)    #motorSteeringPositive  
motSN = OutputDevice(4)    #motorSteeringNegative
motSE = PWMOutputDevice(26, True, 0, 100)    #motorSteeringEnable
motEP = OutputDevice(24)    #motorEnginePositive
motEN = OutputDevice(12)    #motorEngineNegative
motEE = PWMOutputDevice(14, True, 0, 100)    #motorEngineEnable
frnt_led=OutputDevice(20)
bck_led = OutputDevice(19) 
bck_led.off()
frnt_led.off()
      
def fwd_right():
    print("right")
    #motSE.value=1.0
    motSE.on()
    motSP.on()
    motSN.off()
    motEE.value = 1.0
    motEP.on()
    motEN.off()
    
def fwd_left():
    print("left")
    #motSE.value=1.0
    motSE.on()
    motSP.off()
    motSN.on()
    motEE.value = 1.0
    motEP.on()
    motEN.off()
    
def fwd():
    motEE.value = 0.7
    print("forward")
    motEP.on()
    motEN.off()
    #frnt_led.on()
    
def rev():
    motEE.value = 1.0
    print("reverse")
    motEP.off() 
    motEN.on() 
    #bck_led.on()
    
def stop():
    motSE.value = 0
    motEE.value = 0
    print("stop")
    motSP.off()
    motSN.off()
    motEP.off()
    motEN.off()

actions = {
    curses.KEY_UP:    fwd,
    curses.KEY_DOWN:  rev,
    curses.KEY_LEFT:  fwd_left,
    curses.KEY_RIGHT: fwd_right,
}

def main(window):
    next_key = None
    fcount = 0
    lcount = 0
    rcount = 0
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
            #print(key)
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            elif key==ord('q'):
                break
            next_key = key
            while next_key == key:
                next_key = window.getch()          
            # KEY RELEASED
            stop()
            
        check,frame=video.read()
        resized_frame=cv2.resize(frame,(320,240))
        gray=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("mobCam_gray",gray)
        #cv2.imshow("mobCam_rgb",resized_frame)
        if key==260:
            lcount += 1
            cv2.imwrite("training_data/left/%d.jpg" % lcount, gray)
        elif key==261:
            rcount += 1
            cv2.imwrite("training_data/right/%d.jpg" % rcount, gray)
        elif key==259:
            fcount += 1
            cv2.imwrite("training_data/fwd/%d.jpg" % fcount, gray)


curses.wrapper(main)
stop()
video.release()
cv2.destroyAllWindows()
print("OK Bye!")