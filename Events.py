#
#   File : Events.py
#   
#   Code written by : Johann Heches
#
#   Description : Manage keyboard events (camera / limb control, view mode).
#   


from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtWidgets, QtGui, QtCore

import time
import Shaders

import Definitions

""" list of all keyboard events waiting to be executed """
eventKeyList = []
eventPressList = []
eventModifierList = []

lastTime = 0 # for time between frames

""" mouse controls """
mouse_click = False
setLookAt = False
caps = False
ctrl = False

""" camera/position/orientation controls """
leftRight_acceleration = 0
leftRight_keyHold = 0
leftRight_cam = 0
leftRight_cam_cap = 5
leftRight_pos_cap = 0.1
leftRight_ori_cap = 5

upDown_acceleration = 0
upDown_keyHold = 0
upDown_cam = 0
upDown_cam_cap = 5
upDown_pos_cap = 0.1
upDown_ori_cap = 5

frontBack_acceleration = 0
frontBack_keyHold = 0
frontBack_cam = -5
frontBack_cam_cap = 0.5
frontBack_pos_cap = 0.1
frontBack_ori_cap = 5


style = 0 # rendering style
SHOW = 0
FADE = 1
HIDE = 2
showGround = True

k = 0

def manage():

    global eventKeyList
    global eventPressList
    global eventModifierList

    global lastTime

    global caps
    global ctrl

    global leftRight_acceleration
    global leftRight_keyHold
    global leftRight_cam

    global upDown_acceleration
    global upDown_keyHold
    global upDown_cam
    
    global frontBack_acceleration
    global frontBack_keyHold
    global frontBack_cam

    global k

    dt = time.clock() - lastTime
    lastTime = time.clock()
    k = 18*dt # adjust speed to time instead of frame rate

    

    """ New events """
    for i in range(0,len(eventKeyList)):
        eventKey = eventKeyList[i]
        eventModifier = eventModifierList[i]
        eventPress = eventPressList[i]
        """ Exit """
        if eventKey == QtCore.Qt.Key_Escape:
            quit()
            
        """ Special keys """
        caps = (eventModifier == QtCore.Qt.ShiftModifier)
        ctrl = (eventModifier == QtCore.Qt.ControlModifier)
        if eventModifier == QtCore.Qt.ShiftModifier:
            upDown_acceleration = 0
            leftRight_acceleration = 0
            frontBack_acceleration = 0
            
        if eventModifier == QtCore.Qt.ControlModifier:
            upDown_acceleration = 0
            leftRight_acceleration = 0
            frontBack_acceleration = 0

        """ Camera/position/orientation controller """
        if eventPress == True and eventKey == QtCore.Qt.Key_Left:
            leftRight_keyHold = 1
            if leftRight_acceleration < 0.2:
                leftRight_acceleration = 0.2
        if eventPress == True and eventKey == QtCore.Qt.Key_Right:
            leftRight_keyHold = -1
            if leftRight_acceleration > -0.2:
                leftRight_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_Left or eventKey == QtCore.Qt.Key_Right):
            leftRight_keyHold = 0
    
    
        if eventPress == True and eventKey == QtCore.Qt.Key_Up:
            upDown_keyHold = 1
            if upDown_acceleration < 0.2:
                upDown_acceleration = 0.2
        if eventPress == True and eventKey == QtCore.Qt.Key_Down:
            upDown_keyHold = -1
            if upDown_acceleration > -0.2:
                upDown_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_Up or eventKey == QtCore.Qt.Key_Down):
            upDown_keyHold = 0
    
    
        if eventPress == True and eventKey == QtCore.Qt.Key_PageUp:
            frontBack_keyHold = 1
            if frontBack_acceleration < 0.2:
                frontBack_acceleration = 0.2
        elif eventPress == True and eventKey == QtCore.Qt.Key_PageDown:
            frontBack_keyHold = -1
            if frontBack_acceleration > -0.2:
                frontBack_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_PageUp or eventKey == QtCore.Qt.Key_PageDown):
            frontBack_keyHold = 0
    
    
        


    eventKeyList = []
    eventPressList = []
    eventModifierList = []

    """ Controller acceleration update - left / right """
    if leftRight_keyHold == 0:
        if leftRight_acceleration > 0.1:
            leftRight_acceleration -= 0.1
        elif leftRight_acceleration < -0.1:
            leftRight_acceleration += 0.1
        else:
            leftRight_acceleration = 0.
    elif leftRight_keyHold == 1:
        if leftRight_acceleration < 0.9:
            leftRight_acceleration += 0.1
        else:
            leftRight_acceleration = 1
    elif leftRight_keyHold == -1:
        if leftRight_acceleration > -0.9:
            leftRight_acceleration -= 0.1
        else:
            leftRight_acceleration = -1
            
    """ Controller acceleration update - up / down """
    if upDown_keyHold == 0:
        if upDown_acceleration > 0.1:
            upDown_acceleration -= 0.1
        elif upDown_acceleration < -0.1:
            upDown_acceleration += 0.1
        else:
            upDown_acceleration = 0.
    elif upDown_keyHold == 1:
        if upDown_acceleration < 0.9:
            upDown_acceleration += 0.1
        else:
            upDown_acceleration = 1
    elif upDown_keyHold == -1:
        if upDown_acceleration > -0.9:
            upDown_acceleration -= 0.1
        else:
            upDown_acceleration = -1

    """ Controller acceleration update - front / back """
    if frontBack_keyHold == 0:
        if frontBack_acceleration > 0.1:
            frontBack_acceleration -= 0.1
        elif frontBack_acceleration < -0.1:
            frontBack_acceleration += 0.1
        else:
            frontBack_acceleration = 0.
    elif frontBack_keyHold == 1:
        if frontBack_acceleration < 0.9:
            frontBack_acceleration += 0.1
        else:
            frontBack_acceleration = 1
    elif frontBack_keyHold == -1:
        if frontBack_acceleration > -0.9:
            frontBack_acceleration -= 0.1
        else:
            frontBack_acceleration = -1


    """ Apply camera control """
    frontBack_cam += frontBack_acceleration*frontBack_cam_cap*k
    leftRight_cam += leftRight_acceleration*leftRight_cam_cap*k
    upDown_cam += upDown_acceleration*upDown_cam_cap*k
        