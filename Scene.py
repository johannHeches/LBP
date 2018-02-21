#
#   File : Scene.py
#   
#   Code written by : Johann Heches
#
#   Description : Fancy background. Not required for the purpose of this project. Could be uterly changed to add a room for the avatar to move in (or stairs, obstacles, ...).
#   


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

import math
import numpy as np

import Definitions
import Events
import Graphics
import Maze
import Shaders
    


class characteristics(object):
    """
        characteristics
        .o      rotation angle
        .xyz    rotation axis
    """


    def __init__(self, ini = 1.70): # add orientation here or keep it on origin limb ?
        """ constructor """
        self.tag = ""
        self.size = ini # change to a 3D scale after ?
        self.position = [0, 0, 0]
        self.orientation = [1, 0, 0, 0]
        self.limbs = []
        self.mesh = None
        self.muscles = []

groundPreprocess = []
def preprocessScene():
    global groundPreprocess
    #preprocess only if something changed (empty groundPreprocess)
    if groundPreprocess != []:
        return
    
    Definitions.modelMatrix.push()
    #Definitions.modelMatrix.translate(0, -1, 0)
    Definitions.modelMatrix.rotate(90, 0, 0, 1)
    
    
    """ Xwall """
    for x in range(0,Maze.X+1):
        for y in range(0,Maze.Y):
            for z in range(0,Maze.Z):
                Definitions.modelMatrix.push()
                Definitions.modelMatrix.translate(x-(Maze.X)/2.,y-(Maze.Y-1)/2.,z-(Maze.Z-1)/2.)

                if Maze.Xwall[x][y][z] == True:
                    Definitions.modelMatrix.push()
                    Definitions.modelMatrix.scale(0,0.95,0.95)
                    groundPreprocess = groundPreprocess + [Definitions.modelMatrix.peek(),]
                    Definitions.modelMatrix.pop()

                Definitions.modelMatrix.pop()
            

    """ Ywall """
    for x in range(0,Maze.X):
        for y in range(0,Maze.Y+1):
            for z in range(0,Maze.Z):
                Definitions.modelMatrix.push()
                Definitions.modelMatrix.translate(x-(Maze.X-1)/2.,y-(Maze.Y)/2.,z-(Maze.Z-1)/2.)

                if Maze.Ywall[x][y][z] == True:
                    Definitions.modelMatrix.push()
                    Definitions.modelMatrix.scale(0.95,0,0.95)
                    groundPreprocess = groundPreprocess + [Definitions.modelMatrix.peek(),]
                    Definitions.modelMatrix.pop()

                Definitions.modelMatrix.pop()
            
    
    """ Zwall """
    for x in range(0,Maze.X):
        for y in range(0,Maze.Y):
            for z in range(0,Maze.Z+1):
                Definitions.modelMatrix.push()
                Definitions.modelMatrix.translate(x-(Maze.X-1)/2.,y-(Maze.Y-1)/2.,z-(Maze.Z)/2.)

                if Maze.Zwall[x][y][z] == True:
                    Definitions.modelMatrix.push()
                    Definitions.modelMatrix.scale(0.95,0.95,0)
                    groundPreprocess = groundPreprocess + [Definitions.modelMatrix.peek(),]
                    Definitions.modelMatrix.pop()

                Definitions.modelMatrix.pop()


    Definitions.modelMatrix.pop()


tile = None
def drawScene():
    if Events.style == Graphics.idBuffer:
        return
    if Events.showGround == False:
        return
    
    
    """ bind surfaces vbo """
    tile.mesh.surfIndexPositions.bind()
    tile.mesh.vertexPositions.bind()
    glVertexAttribPointer(Shaders.position, 3, GL_FLOAT, GL_FALSE, 0, None)
    for pack in groundPreprocess:

        """ choose color """
        color = np.array([0.5,0.,1,0.05], dtype = np.float32)

        """ send color to shader """
        glUniform4fv(Shaders.setColor_loc, 1, color)

        """ send matrix to shader """
        glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, pack)

        """ draw vbo """
        glDrawElements(tile.mesh.surfStyleIndex, tile.mesh.surfNbIndex, GL_UNSIGNED_INT, None)
        

    """ bind edges vbo """
    tile.mesh.edgeIndexPositions.bind()
    tile.mesh.vertexPositions.bind()
    glVertexAttribPointer(Shaders.position, 3, GL_FLOAT, GL_FALSE, 0, None)
    for pack in groundPreprocess:

        """ choose color """
        color = np.array([0.5,0.,1,0.2], dtype = np.float32)

        """ send color to shader """
        glUniform4fv(Shaders.setColor_loc, 1, color)

        """ send matrix to shader """
        glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, pack)

        """ draw vbo """
        glDrawElements(tile.mesh.edgeStyleIndex, tile.mesh.edgeNbIndex, GL_UNSIGNED_INT, None)