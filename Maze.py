from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

import math
import numpy as np
import random

import Definitions
import Shaders

X = 10
Y = 10
Z = 10
Xwall = []
Ywall = []
Zwall = []
room = []
S = [0,0,0]
E = [X-1,Y-1,Z-1]

def mazeInit():
    global Xwall
    global Ywall
    global Zwall
    global room

    #bool(random.getrandbits(1))

    Xwall = [[[True     for z in range(0,Z)]    for y in range(0,Y)]    for x in range(0,X+1)]
    Ywall = [[[True     for z in range(0,Z)]    for y in range(0,Y+1)]  for x in range(0,X)]
    Zwall = [[[True     for z in range(0,Z+1)]  for y in range(0,Y)]    for x in range(0,X)]
    room =  [[[False    for z in range(0,Z)]    for y in range(0,Y)]    for x in range(0,X)]
    
    room[S[0]][S[1]][S[2]] = True
    room[E[0]][E[1]][E[2]] = True
    genPath(S,E)
    
    for i in range(0,10000):
        I = chooseRandomRoom(False)
        F = chooseRandomRoom(True)
        if I[0] == -1 or F[0] == -1:
            break
        room[I[0]][I[1]][I[2]] = True
        room[F[0]][F[1]][F[2]] = True
        genPath(I,F)
    
    breakWalls()


def chooseRandomRoom(used):
    
    countMax = 0
    for x in range(0,X):
        for y in range(0,Y):
            for z in range(0,Z):
                if room[x][y][z] == used:
                    countMax += 1
    if countMax == 0:
        return [-1,-1,-1]
    countMax = random.randint(1,countMax)

    count = 0
    for x in range(0,X):
        for y in range(0,Y):
            for z in range(0,Z):
                if room[x][y][z] == used:
                    count += 1
                    if count == countMax:
                        return [x,y,z]

def genPath(S,E):
    if S[0] == E[0] and S[1] == E[1] and S[2] == E[2]:
        return

    choose = []
    if S[0] != E[0]:
        choose = choose + [0,]
    if S[1] != E[1]:
        choose = choose + [1,]
    if S[2] != E[2]:
        choose = choose + [2,]
    choose = choose[random.randint(0,len(choose)-1)]

    if choose == 0:
        if S[0] < E[0]:
            S[0] = S[0] + 1
            Xwall[S[0]][S[1]][S[2]] = False
        elif S[0] > E[0]:
            Xwall[S[0]][S[1]][S[2]] = False
            S[0] = S[0] - 1
    elif choose == 1:
        if S[1] < E[1]:
            S[1] = S[1] + 1
            Ywall[S[0]][S[1]][S[2]] = False
        elif S[1] > E[1]:
            Ywall[S[0]][S[1]][S[2]] = False
            S[1] = S[1] - 1
    elif choose == 2:
        if S[2] < E[2]:
            S[2] = S[2] + 1
            Zwall[S[0]][S[1]][S[2]] = False
        elif S[2] > E[2]:
            Zwall[S[0]][S[1]][S[2]] = False
            S[2] = S[2] - 1

    #if room[S[0]][S[1]][S[2]] == True:
    #    return

    room[S[0]][S[1]][S[2]] = True
    genPath(S,E)


def breakWalls():
    global Xwall
    global Ywall
    global Zwall
    global room

    for x in range(0,X):
        for y in range(0,Y):
            for z in range(0,Z):
                if room[x][y][z] == False:
                    if x-1 >= 0 and room[x-1][y][z] == False:
                        Xwall[x][y][z] = False
                    if x+1 < X and room[x+1][y][z] == False:
                        Xwall[x+1][y][z] = False
                    if y-1 >= 0 and room[x][y-1][z] == False:
                        Ywall[x][y][z] = False
                    if y+1 < Y and room[x][y+1][z] == False:
                        Ywall[x][y+1][z] = False
                    if z-1 >= 0 and room[x][y][z-1] == False:
                        Zwall[x][y][z] = False
                    if z+1 < Z and room[x][y][z+1] == False:
                        Zwall[x][y][z+1] = False

