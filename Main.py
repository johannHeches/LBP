import copy
from ctypes import *
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
from OpenGL.arrays import vbo
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
                                                  glBindVertexArray
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import *
import sys
import time

import Definitions
import Entity
import Events
import Graphics
import Maze
import Shaders


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        self.initialized = False
        self.displayFBO = 1 # for some reasons PyQt made a new fbo on it's own, so it's 1 and not 0 ?
        self.idFBO = None
        super(mainWindow, self).__init__(*args)
        loadUi('minimal.ui', self)


    def setupUI(self):
        self.setWindowTitle('Wearable Sensors')
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(1500,800)
        self.openGLWidget.paintGL = self.paintGL

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.openGLWidget.update) 
        timer.start(10)

        self.setMouseTracking(True)

    def paintGL(self):

        """
            first call requires initialization
        """
        if self.initialized == False:
            self.initialized = True
            self.initializeGL()
            print("initialization done")


        """  -----------------  """
        """  >>> main loop <<<  """
        """  -----------------  """
        # keep track of loop frequency
        flagStart = time.clock()



        """
            Events management.
            Keyboard interactions between the user and the software are done here.
        """
        Events.manage()

        

        """
            Preprocess entities.
            Store all needed transformations to significantly lower calculation cost when rendering (redundancy otherwise between display buffer, ID buffer and bindings)
        """
        #Scene.preprocessScene()


        
        """
            update camera
        """

        Definitions.viewMatrix.push()
        Definitions.viewMatrix.translate(0,0,Events.frontBack_cam)
        Definitions.viewMatrix.rotate(Events.upDown_cam, 1, 0, 0)
        Definitions.viewMatrix.rotate(Events.leftRight_cam, 0, 1, 0)
        glUniformMatrix4fv(Shaders.view_loc, 1, GL_FALSE, Definitions.viewMatrix.peek())
        Definitions.viewMatrix.pop()



        """
            Draw on the display buffer.
            The display buffer is what the user will see on his screen.
        """
        # bind the display buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.displayFBO)
        
        # clear the display buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glViewport(0,0,Graphics.display[0],Graphics.display[1])
        
        # draw scene
        Graphics.modelView(Graphics.blending)
        Definitions.modelMatrix.push()
        Definitions.modelMatrix.rotate(90, 0, 0, 1)
        Entity.virtuEarth.mesh.modelMatrix = Definitions.modelMatrix.peek()
        Definitions.modelMatrix.pop()
        Entity.drawEntity(Entity.virtuEarth)

        
        Graphics.modelView(Graphics.opaque)
        Definitions.modelMatrix.push()
        Definitions.modelMatrix.scale(0.1, 0.1, 0.1)
        Definitions.modelMatrix.rotate(-Events.leftRight_cam, 0, 1, 0)
        Definitions.modelMatrix.rotate(-Events.upDown_cam, 1, 0, 0)
        Definitions.modelMatrix.translate(0,0,5)
        Definitions.modelMatrix.rotate(-90, 0, 1, 0)
        Definitions.modelMatrix.scale(1, 2, 2)
        Entity.virtuShip.mesh.modelMatrix = Definitions.modelMatrix.peek()
        Definitions.modelMatrix.pop()
        Entity.drawEntity(Entity.virtuShip)

        Graphics.modelView(Graphics.opaque)
        Definitions.modelMatrix.push()
        Definitions.modelMatrix.rotate(-90, 0, 1, 0)
        Definitions.modelMatrix.translate(0.5,0,0)
        Definitions.modelMatrix.scale(3, 3, 3)
        Definitions.modelMatrix.translate(0.5,0,0)
        Entity.virtuPath.mesh.modelMatrix = Definitions.modelMatrix.peek()
        Definitions.modelMatrix.pop()
        Entity.virtuPath.mesh.surfColor = np.array([0.5*math.cos(time.clock()),0.5*math.cos(time.clock() + math.pi*2/3),0.5*math.cos(time.clock() + math.pi*4/3),0.15], dtype = np.float32)
        Entity.virtuPath.mesh.edgeColor = np.array([1*math.cos(time.clock()),1*math.cos(time.clock() + math.pi*2/3),1*math.cos(time.clock() + math.pi*4/3),0.15], dtype = np.float32)
        Entity.drawEntity(Entity.virtuPath)
        
        Graphics.modelView(Graphics.opaque)
        Definitions.modelMatrix.push()
        Definitions.modelMatrix.translate(0,0,0.5)
        Definitions.modelMatrix.scale(3, 3, 3)
        Definitions.modelMatrix.translate(0,0,1)
        Definitions.modelMatrix.scale(1/15., 1/15., 1/15.)
        Definitions.modelMatrix.rotate(90, 0, 1, 0)
        Entity.virtuAsteroid.mesh.modelMatrix = Definitions.modelMatrix.peek()
        Definitions.modelMatrix.pop()
        Entity.drawEntity(Entity.virtuAsteroid)

        print("FREQ : ", int(1./(time.clock()-flagStart)))



    def initializeGL(self):
        
        glClearColor(0.0, 0.0, 0.0, 0.0);
        """ texture for ID buffer """
        # create texture
        plane_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, plane_texture)
        # texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, Graphics.display[0], Graphics.display[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)


        """ render buffer for depth for ID buffer """
        # create render buffer
        rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, Graphics.display[0], Graphics.display[1])
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
    

        """ frame buffer object as ID buffer """
        # create frame buffer
        self.idFBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.idFBO)
        # attach texture to frame buffer
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, plane_texture, 0)
        # attach render buffer to frame buffer
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        """ Generate the VBOs """
        Graphics.VBO_init()
    

        """ Create the shaders """
        Shaders.shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(Shaders.vertex_shader,GL_VERTEX_SHADER),
                                                          OpenGL.GL.shaders.compileShader(Shaders.fragment_shader,GL_FRAGMENT_SHADER))
        glUseProgram(Shaders.shader)


        """ Enable position attrib ? """
        Shaders.position = glGetAttribLocation(Shaders.shader, "position")
        glVertexAttribPointer(Shaders.position, 3, GL_FLOAT, GL_FALSE, 0, None) 
        glEnableVertexAttribArray(Shaders.position)


        """ Initialize some more stuff"""
        glEnable(GL_TEXTURE_2D)
        glDepthFunc(GL_LEQUAL)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    

        """ Shader var. locations """
        Shaders.proj_loc = glGetUniformLocation(Shaders.shader, "projection")
        Shaders.view_loc = glGetUniformLocation(Shaders.shader, "view")
        Shaders.model_loc = glGetUniformLocation(Shaders.shader, "model")
        Shaders.setColor_loc = glGetUniformLocation(Shaders.shader, "setColor")
    
        Definitions.projectionMatrix.perspectiveProjection(90, Graphics.display[0]/Graphics.display[1], 0.1, 100.0)
        glUniformMatrix4fv(Shaders.proj_loc, 1, GL_FALSE, Definitions.projectionMatrix.peek())
        glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, Definitions.modelMatrix.peek())

        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            Events.mouse_click = True
        if event.button() == QtCore.Qt.RightButton:
            Events.setLookAt = True

    def keyPressEvent(self, event):
        Events.eventModifierList = Events.eventModifierList + [QtWidgets.QApplication.keyboardModifiers()]
        if event.isAutoRepeat() == False:
            Events.eventKeyList = Events.eventKeyList + [event.key()]
            Events.eventPressList = Events.eventPressList + [True]

    def keyReleaseEvent(self, event):
        Events.eventModifierList = Events.eventModifierList + [QtWidgets.QApplication.keyboardModifiers()]
        if event.isAutoRepeat() == False:
            Events.eventKeyList = Events.eventKeyList + [event.key()]
            Events.eventPressList = Events.eventPressList + [False]

if __name__ == '__main__':
    
    """ Application """
    app = QtWidgets.QApplication(sys.argv)
    Maze.mazeInit()
    
    Entity.virtuEarth = Entity.entity()
    Entity.virtuEarth.mesh = Graphics.VBO_sphere()
    Graphics.buildVBO(Entity.virtuEarth)
    Entity.virtuEarth.mesh.surfColor = np.array([0, 0, 0.5, 0.15], dtype = np.float32)
    Entity.virtuEarth.mesh.edgeColor = np.array([0, 0, 1, 0.15], dtype = np.float32)
    
    
    Entity.virtuShip = Entity.entity()
    Entity.virtuShip.mesh = Graphics.VBO_circle()
    Graphics.buildVBO(Entity.virtuShip)
    Entity.virtuShip.mesh.surfColor = np.array([0.5, 0.5, 0.5, 0.15], dtype = np.float32)
    Entity.virtuShip.mesh.edgeColor = np.array([1, 1, 1, 0.15], dtype = np.float32)
        
    
    Entity.virtuPath = Entity.entity()
    Entity.virtuPath.mesh = Graphics.VBO_dashed(10)
    Graphics.buildVBO(Entity.virtuPath)
    Entity.virtuPath.mesh.surfColor = np.array([0.5, 0, 0, 0.15], dtype = np.float32)
    Entity.virtuPath.mesh.edgeColor = np.array([1, 0, 0, 0.15], dtype = np.float32)


    
    Entity.virtuAsteroid = Entity.entity()
    Entity.virtuAsteroid.mesh = Graphics.VBO_maze()
    Graphics.buildVBO(Entity.virtuAsteroid)
    Entity.virtuAsteroid.mesh.surfColor = np.array([0.35, 0.08, 0.02, 0.15], dtype = np.float32)
    Entity.virtuAsteroid.mesh.edgeColor = np.array([0.65, 0.15, 0.04, 0.15], dtype = np.float32)


    """ 3D Scene """
    window = mainWindow()
    window.setupUI()
    window.show()
    
    """ EXIT Application """
    sys.exit(app.exec_())
