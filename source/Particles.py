import numpy as np
from Map import Map
import random
from random import seed
from random import randint
from datetime import datetime
import time

import matplotlib.pyplot as plt

class Particles:
    '''
    initParticles will receive the percenteige of each types:
    eg: 2 types each 45% of the map that is passed as Input
    args = [45, 45]

    The implementation also support multiple types eg. 3 or 4
    '''

    X = 0
    Y = 1
    Type = 2
    XLETTER = 'x'
    YLETTER = 'y'
    coordLetter = ['E','W','N','S','SE','SW','NE','NW']
    E = 0
    W = 1
    N = 2
    S = 3
    SE = 4
    SW = 5
    NE = 6
    NW = 7


    coords = {
        'E':{'x': 0, 'y': 1},
        'W':{'x': 0, 'y':-1},
        'N':{'x':-1, 'y':0},
        'S':{'x':1, 'y':0},
        'SE':{'x':1, 'y':1},
        'SW':{'x':1, 'y':-1},
        'NE':{'x':-1, 'y':1},
        'NW':{'x':-1, 'y':-1},
    }



    '''
    updateUnHappyParticles
    ---------------------
    This function update the list of UnHappy particles.
    For each particle it check how many neighbours are similar to it.
    '''
    def updateUnHappyParticles(self):
        self.unHappyParticles = []
        for i in range(0, self.totalNumParticles):
            elem = self.particles[i]
            count = 0
            for neigh in self.neighbours[i]:
                if((self.particles[neigh][self.Type]) == (elem[self.Type])):
                    count=count + 1
            if(count<self.toBeHappy):
                self.unHappyParticles.append(i)


    '''
    search For Empty
    ---------------------
    This function search the first empty place to move an UnHappy Particle.
    For each unhappy particle it check the nearest (based on norm2, considering periodic boundaries)
    empty cell.
    It checks recursively if some neighbour is empty.
    -> particleToParse is the queue o nearest particles that are needed to parse.
    '''
    def searchForEmpty(self, particle):
        FOUND = 0
        part = particle
        particleToParse = []
        coordx = 0
        coordy = 0
        index = 0
        coordx = self.particles[particle][self.X]
        coordy = self.particles[particle][self.Y]

        while not FOUND:

            random.seed(datetime.now())
            #All movement (in all 8 directions) allowed
            #indexToExplore = randint(self.E, self.NW)

            #E W N S Allowed
            indexToExplore = randint(self.E, self.SE)

            #Horizontal Movements allowed
            #indexToExplore = randint(self.E, self.N)

            #Vertical Movements allowed
            #indexToExplore = randint(self.N, self.SE)

            #ARTIFACT: Random Noise that speed up the convergence by a factor of 2x (empirical)
            randomadditionx = randint(0, 5)
            randomadditiony = randint(0, 5)

            coordx = (coordx + randomadditionx+ self.coords[self.coordLetter[indexToExplore]][self.XLETTER])%self.map.rows
            coordy = (coordy + randomadditiony+ self.coords[self.coordLetter[indexToExplore]][self.YLETTER])%self.map.columns
            if(self.map.map[coordx,coordy] == self.map.EMPTY):
                FOUND=1

        #Alternative approach that move to the nearest empty cell
        '''
            random.seed(datetime.now())
            indexToExplore = randint(0, 7)
            for i in range(0,8):
                neigh = self.neighbours[part][(indexToExplore + i)%7]
                if(neigh == self.map.EMPTY):
                    FOUND = 1
                    index = self.neighbours[part].index(neigh)
                    #coordToAdd permits to recreate the real coords of neighbours
                    coordToAdd  = self.coords[self.coordLetter[index]]
                    coordx = (self.particles[part][self.X] + coordToAdd[self.XLETTER])%self.map.columns
                    coordy = (self.particles[part][self.Y] + coordToAdd[self.YLETTER])%self.map.rows
                    break
                else:
                    particleToParse.append(neigh)


            #To avoid stagnation, choose randomly a particle to be added in the queue
            if not particleToParse:
                added = 0
                while not added:
                    random.seed(datetime.now())
                    randx = randint(0, self.map.rows-1)
                    randy = randint(0, self.map.columns-1)
                    if (self.map.map[randx,randy] != self.map.EMPTY):
                        particleToParse.append(self.map.map[randx,randy])
                        added = 1

            #Pop the first added Particle and repeat untill and empty cell is founded
            part = particleToParse.pop()
            '''
        return [coordx,coordy]

    '''
    Initialization function
    -----------------------
    args:
        are the percentage of different types of population.
        eg: 2 types each 45% of the map that is passed as Input
        args = [45, 45]

        The implementation also supper multiple types eg. 3 or 4

    map:
        is the map in which place the particles

    toBeHappy:
        is the number of neihgbours that are needed to be similar to be Happy

    tolerance:
        percentage of total population that can remain unHappy
        (a kind of error tolerance, it's not possible to make everyone happy)

    '''


    def init(self, args, map, toBeHappy, tolerance, maxiteration):
        self.totalParticles = []
        self.unHappyParticles = []
        self.totalNumParticles = 0
        self.maxiteration = maxiteration
        self.map = map
        self.toBeHappy = int(toBeHappy)

        #Calculation of particles based on percenteges

        for arg in args:
            local = arg * map.size//100
            self.totalParticles.append(local)
            self.totalNumParticles += local

        if(self.totalNumParticles> self.map.size):
            print("ERROR: the percentages must totalize 100 or lower")
            exit(1)

        self.tolerance = self.totalNumParticles*tolerance//100

        #Simple PreAllocation that speed up the initializaiton
        self.particles = self.totalNumParticles*[None]
        self.neighbours = self.totalNumParticles*[None]
        self.mapToPlot = Map()
        self.mapToPlot.initMap(map.rows, map.columns)

        random.seed(datetime.now())

        for i in range(0, len(self.totalParticles)):
            for j in range(0, self.totalParticles[i]):
                ASSIGNED = 0
                while not ASSIGNED:
                    randx = randint(0, map.rows-1)
                    randy = randint(0, map.columns-1)

                    if self.map.map[randx, randy] == map.EMPTY:
                        id = i*self.totalParticles[i]+j
                        self.particles[id] = [randx, randy, i]
                        self.map.map[randx,randy] = id
                        self.mapToPlot.map[randx,randy] = i
                        ASSIGNED =1


        '''
        NEIGHBOURS INITIALIZATIONS
        it wouldn't be so necessary in this case since we are talking about grids and the concept of neighbour could be derive by the map.
        However is necessary if we want to create a framework for more complex models (even in non grid domains).
        '''
        for i in range(0, self.totalNumParticles):
            elem = self.particles[i]
            X = elem[self.X]
            Y = elem[self.Y]
            e = self.map.map[X, (Y+1)%self.map.columns]
            w = self.map.map[X, (Y-1)%self.map.columns]
            s = self.map.map[(X+1)%self.map.rows, Y]
            n = self.map.map[(X-1)%self.map.rows, Y]
            se = self.map.map[(X+1)%self.map.rows, (Y+1)%self.map.columns]
            sw = self.map.map[(X+1)%self.map.rows, (Y-1)%self.map.columns]
            ne = self.map.map[(X-1)%self.map.rows, (Y+1)%self.map.columns]
            nw = self.map.map[(X-1)%self.map.rows, (Y-1)%self.map.columns]
            self.neighbours[i] = [e, w, n, s, se, sw, ne, nw]

        #Initialize unHappyParticles
        self.updateUnHappyParticles()


    '''
    moveUnHappyParticles
    --------------------
    Move an unHappy particle to the nearest empty cell, the movement is written in searchForEmpty, the update all the neighbours
    '''
    def moveUnHappyParticles(self):
        for i in self.unHappyParticles:
            xy = self.searchForEmpty(i)
            self.updateParticle(i,xy)
            self.unHappyParticles.remove(i)

    def updateParticle(self, particle, newcoords):
        mypart = self.particles[particle]
        oldCoordx = mypart[self.X]
        oldCoordy = mypart[self.Y]

        #NEW COORDS
        self.particles[particle][self.X] = newcoords[0]
        self.particles[particle][self.Y] = newcoords[1]

        self.map.map[newcoords[0], newcoords[1]] = particle
        self.mapToPlot.map[newcoords[0], newcoords[1]] = mypart[self.Type]
        self.map.map[oldCoordx, oldCoordy] = self.map.EMPTY
        self.mapToPlot.map[oldCoordx, oldCoordy] = self.map.EMPTY

        #Update Neighbours
        self.updateNeighBours(particle)

    '''
    updateNeighBours
    --------------------
    Update the neighbours.
    An alternative implementation could be given considering empty cells as a particular type of particles.
    To maintain a semantic consistency I preferred considering Empty Cells as non-particles entities and just places in the grid.

    '''

    def updateNeighBours(self, particle):
        mypart = self.particles[particle]

        #Update OldNeighbours (to be optimized)
        neighbours = self.neighbours[particle]
        if(neighbours[self.E] != self.map.EMPTY):
            self.neighbours[neighbours[self.E]][self.W] = self.map.EMPTY
        if(neighbours[self.W] != self.map.EMPTY):
            self.neighbours[neighbours[self.W]][self.E] = self.map.EMPTY
        if(neighbours[self.N] != self.map.EMPTY):
            self.neighbours[neighbours[self.N]][self.S] = self.map.EMPTY
        if(neighbours[self.S] != self.map.EMPTY):
            self.neighbours[neighbours[self.S]][self.N] = self.map.EMPTY
        if(neighbours[self.SW] != self.map.EMPTY):
            self.neighbours[neighbours[self.SW]][self.NE] = self.map.EMPTY
        if(neighbours[self.NW] != self.map.EMPTY):
            self.neighbours[neighbours[self.NW]][self.SE] = self.map.EMPTY
        if(neighbours[self.SE] != self.map.EMPTY):
            self.neighbours[neighbours[self.SE]][self.NW] = self.map.EMPTY
        if(neighbours[self.NE]!= self.map.EMPTY):
            self.neighbours[neighbours[self.NE]][self.SW] = self.map.EMPTY

        #Update New Neihtbours
        X = mypart[self.X]
        Y = mypart[self.Y]

        s = self.map.map[(X+1)%self.map.rows, Y]
        self.neighbours[particle][self.S] = s
        if(s != self.map.EMPTY):
            self.neighbours[s][self.N] = particle

        n = self.map.map[(X-1)%self.map.rows, Y]
        self.neighbours[particle][self.N] = n
        if(n!= self.map.EMPTY):
            self.neighbours[n][self.S] = particle

        e = self.map.map[X, (Y+1)%self.map.columns]
        self.neighbours[particle][self.E] = e
        if(e!= self.map.EMPTY):
            self.neighbours[e][self.W] = particle

        w = self.map.map[X, (Y-1)%self.map.columns]
        self.neighbours[particle][self.W] = w
        if(w!= self.map.EMPTY):
            self.neighbours[w][self.E] = particle

        se = self.map.map[(X+1)%self.map.rows, (Y+1)%self.map.columns]
        self.neighbours[particle][self.SE] = se
        if(se!= self.map.EMPTY):
            self.neighbours[se][self.NW] = particle

        ne = self.map.map[(X-1)%self.map.rows, (Y+1)%self.map.columns]
        self.neighbours[particle][self.NE] = ne
        if(ne!= self.map.EMPTY):
            self.neighbours[ne][self.SW] = particle

        sw = self.map.map[(X+1)%self.map.rows, (Y-1)%self.map.columns]
        self.neighbours[particle][self.SW] = sw
        if(sw != self.map.EMPTY):
            self.neighbours[sw][self.NE] = particle

        nw = self.map.map[(X-1)%self.map.rows, (Y-1)%self.map.columns]
        self.neighbours[particle][self.NW] = nw
        if(nw!= self.map.EMPTY):
            self.neighbours[nw][self.SE] = particle

    def printParticlesLive(self):
        plt.matshow(self.mapToPlot.map)
        plt.draw()
        plt.pause(0.0001)
        plt.close()

    def printParticles(self, blockBool):
        plt.matshow(self.mapToPlot.map)
        plt.show(block=blockBool)

    '''
    improveHappyParticles
    -----------------------
    '''
    def improveHappyParticles(self):
        iter = 0
        start_time = time.time()
        self.updateUnHappyParticles()
        while((len(self.unHappyParticles) > self.tolerance) and iter<self.maxiteration):
            self.moveUnHappyParticles()
            self.updateUnHappyParticles()
            iter=iter+1

            #Uncomment to see simulation
            self.printParticlesLive()
            print(iter)
        print("--- %s seconds ---" % (time.time() - start_time))
        return iter, len(self.unHappyParticles)
