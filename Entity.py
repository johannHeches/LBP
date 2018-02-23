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
    


class entity(object):
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
        self.mesh = None

        
def drawEntity(entity):
    
    
    """ bind surfaces vbo """
    entity.mesh.surfIndexPositions.bind()
    entity.mesh.vertexPositions.bind()
    glVertexAttribPointer(Shaders.position, 3, GL_FLOAT, GL_FALSE, 0, None)

    """ send color to shader """
    glUniform4fv(Shaders.setColor_loc, 1, entity.mesh.surfColor)

    """ send matrix to shader """
    glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, entity.mesh.modelMatrix)

    """ draw vbo """
    glDrawElements(entity.mesh.surfStyleIndex, entity.mesh.surfNbIndex, GL_UNSIGNED_INT, None)
        

    """ bind edges vbo """
    entity.mesh.edgeIndexPositions.bind()
    entity.mesh.vertexPositions.bind()
    glVertexAttribPointer(Shaders.position, 3, GL_FLOAT, GL_FALSE, 0, None)

    """ send color to shader """
    glUniform4fv(Shaders.setColor_loc, 1, entity.mesh.edgeColor)

    """ send matrix to shader """
    glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, entity.mesh.modelMatrix)

    """ draw vbo """
    glDrawElements(entity.mesh.edgeStyleIndex, entity.mesh.edgeNbIndex, GL_UNSIGNED_INT, None)