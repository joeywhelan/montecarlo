'''
Created on Nov 21, 2017

@author: Joey Whelan
'''
import random
import pandas as pd
import matplotlib.pyplot as plt
import math


def simulation(numPoints):
    """Calculates an approximation to pi via the Monte Carlo method
        
        Args:
            text: Number of points
            
        Returns:
            Approximation to pi
        
        Raises:
            None
    """
    in_circle = 0
    total = 0

    for _ in range(numPoints):
        x = random.uniform(0,2)
        y = random.uniform(0,2)
    
        d = (x-1)**2 + (y-1)**2
        if d <= 1.0:
            in_circle = in_circle + 1
        total = total + 1
    
    ans = 4 * in_circle/total
    return ans

if __name__ == '__main__': 
    random.seed()
    
    
    results = {}
    for numPoints in [10,100,1000,10000,100000,1000000]:
        ans = simulation(numPoints)
        results[numPoints] = ans
        
    frame = pd.DataFrame(data=list(results.items()), columns=['NumPoints', 'Result'])
    frame['PctError'] = ((frame['Result'] - math.pi) / math.pi).abs() * 100
    del frame['Result']
    frame.sort_values(by='NumPoints', inplace=True)
    frame.reset_index(inplace=True, drop=True)
    print(frame)
    frame.plot(x='NumPoints', y='PctError', kind='bar', title='Monte Carlo Pi Calculation', color=['b'])
    plt.show()

        
    
    
