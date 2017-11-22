'''
Created on Nov 21, 2017

@author: Joey Whelan
'''

import random
import math
import multiprocessing as mp
import pandas as pd
import matplotlib.pyplot as plt

class Yard(object):
    '''Class defining a 3000 sq ft yard with varying numbers of mounds and active ants and 1 human
    '''
    length = 100 #3000 sq ft yard
    width = 30
    numMounds = 5
    numAnts = numMounds * 100000 #100K ants per mound
    pctAntsActive = .5 #percentage of the ants that moving at any given time step
    
    def __init__(self):
        """Yard class initializer.  Provides a random distribution of ant mounds, ants, and 1 human
        
            Args:
                none
            
            Returns:
                none
        
            Raises:
                None
        """    
        random.seed()
        self.__setMounds()
        self.__setAnts()
        self.__setHuman()
        
    def __setMounds(self):
        """Provides a random distribution of ant mounds across a grid.  Mound positions are stored as an object variable.
        
            Args:
                none
            
            Returns:
                none
        
            Raises:
                None
        """    
        self.moundPositions = []
        xlist = random.sample(range(0, Yard.length+1), Yard.numMounds)
        ylist = random.sample(range(0, Yard.width+1), Yard.numMounds)
        for i in range(Yard.numMounds):
            mound = (xlist[i], ylist[i])
            self.moundPositions.append(mound)
    
    def __setAnts(self):
        """Provides a random distribution of antx across the mound positions.
        
            Args:
                none
            
            Returns:
                none
        
            Raises:
                None
        """    
        self.ants = []
        for _ in range(Yard.numAnts):
            mound = random.choice(self.moundPositions)
            self.ants.append(Ant(mound))
                
    def __setHuman(self):
        """Chooses a position for 1 human in the model.  Will not allow the human to be positioned on a mound position.
        
            Args:
                none
            
            Returns:
                none
        
            Raises:
                None
        """    
        done = False
        while not done:
            x = random.randint(0, Yard.length)
            y = random.randint(0, Yard.width)
            if (x, y) not in self.moundPositions: 
                done = True
            else:
                pass
            
        self.humanPosition = (x, y)
    
    def clockTick(self):
        """Main simulation routine.  Simulates 1 time step where ants move positions.  A random distribution
        of a percentage of the ants move on a time step.  The others are idle.
        
            Args:
                none
            
            Returns:
                Number of ants that are in proximity of (attacking) the human.
        
            Raises:
                None
        """    
        antsAttacking = 0
        activeAnts = random.sample(range(0, Yard.numAnts), int(Yard.numAnts*Yard.pctAntsActive))
        
        for ant in activeAnts:
            state = self.ants[ant].move(self.humanPosition)
            if state == 'attacking':
                antsAttacking += 1
                break
            else:
                pass
        
        return antsAttacking
    
class Ant(object):
    '''Class encapsulating the essence of an ant
    '''
    __directions = ['NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
    
    def __init__(self, position):
        """Ant class initializer.  Provides for random movement of an individual ant.
        
            Args:
                position: current grid position in the yard
            
            Returns:
                none
        
            Raises:
                None
        """    
        self.position = position
        self.state = 'foraging'
    
    def __checkAttack(self, humanPosition):
        """Determines if the ant is within 1 foot of the human's position.  If so, the ant's state is changed to 'attacking'.
        
            Args:
                position: current grid position in the yard
            
            Returns:
                the ant's state
        
            Raises:
                None
        """    
        distance = math.sqrt((self.position[0] - humanPosition[0])**2 + (self.position[1] - humanPosition[1])**2)
        if distance <= 1:
            return 'attacking'
        else:
            return 'foraging'
    
    def move(self, humanPosition):
        """Makes a 1 foot move in a random direction.  Will not allow the ant to move outside of the yard boundaries.
        Checks if the ant is within 'attacking' distance of the human.  If so, the ant's state is set to 'attacking."
        At that point, the ant remains in the 'attacking' state and does not move again.
        
            Args:
                position: current grid position in the yard
            
            Returns:
                the ant's state
        
            Raises:
                None
        """    
        if self.state == 'foraging':
            direction = random.choice(Ant.__directions)
              
            if direction == 'NW':
                x = self.position[0] - 1
                y = self.position[1] + 1
            elif direction == 'N':
                x = self.position[0] 
                y = self.position[1] + 1
            elif direction == 'NE':
                x = self.position[0] + 1
                y = self.position[1] + 1
            elif direction == 'E':
                x = self.position[0] + 1
                y = self.position[1] 
            elif direction == 'SE':
                x = self.position[0] + 1
                y = self.position[1] - 1
            elif direction == 'S':
                x = self.position[0] 
                y = self.position[1] - 1
            elif direction == 'SW':
                x = self.position[0] - 1
                y = self.position[1] - 1
            elif direction == 'W':
                x = self.position[0] - 1
                y = self.position[1]
            else:
                pass
              
            if x >= 0 and x <= Yard.length and y >= 0 and y <= Yard.width:
                self.position = (x, y)
            else:
                pass
            self.state = self.__checkAttack(humanPosition)
        else:
            pass
        
        return self.state

def simulation(): 
    """Main driver of the simulation.  Creates the Yard and then starts 4 second time steps during which ants move randomly
    in 1 foot increments.  The simulation ends when at least 1 ant is attacking the human.
        
        Args:
            none
            
        Returns:
            Number of seconds until the ant attacks the human.
        
        Raises:
            None
    """    
    yard = Yard()
    seconds = 0
    numAttacking = 0
    
    while numAttacking == 0:
        numAttacking = yard.clockTick()
        seconds += 4
    
    return seconds
        
if __name__ == '__main__': 
    simIters = [25,50,75,100]
    avg = {}
    
    for iters in simIters:
        tot = 0
        pool = mp.Pool()
        results = []
        for _ in range(iters):
            results.append(pool.apply_async(simulation))       
        pool.close()
        pool.join()
        for res in results:
            tot += res.get()
        avg[iters] = round(tot / iters)
        print(iters, avg[iters])
    
    
    frame = pd.DataFrame(data=list(avg.items()), columns=['Iterations', 'Seconds'])
    frame.sort_values(by='Iterations', inplace=True)
    frame.reset_index(inplace=True, drop=True)
    print(frame)
    frame.plot(x='Iterations', y='Seconds', kind='bar', title='Monte Carlo Fire Ant Attack Simulation', color=['r'])
    plt.show()        
        
        