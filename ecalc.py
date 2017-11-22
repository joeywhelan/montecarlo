'''
Created on Nov 21, 2017

@author: Joey Whelan
'''

import random
import pandas as pd
import matplotlib.pyplot as plt
import math

def simulation(numIters):
    """Calculates an approximation to e via the Monte Carlo method
        
        Args:
            text: Number of iterations
            
        Returns:
            Approximation to e
        
        Raises:
            None
    """
    nsum = 0
    for _ in range(numIters):
        xsum = 0
        n = 0
        while xsum < 1:
            x = random.uniform(0,1)
            xsum = xsum + x 
            n = n + 1
    
        nsum = nsum + n
    
    return nsum/numIters

if __name__ == '__main__': 
    random.seed()
    
    results = {}
    for numIters in [10,100,1000,10000,100000,1000000]:
        ans = simulation(numIters)
        results[numIters] = ans
        
    frame = pd.DataFrame(data=list(results.items()), columns=['Iterations', 'Result'])
    frame['PctError'] = ((frame['Result'] - math.e) / math.e).abs() * 100
    del frame['Result']
    frame.sort_values(by='Iterations', inplace=True)
    frame.reset_index(inplace=True, drop=True)
    print(frame)
    frame.plot(x='Iterations', y='PctError', kind='bar', title='Monte Carlo e Calculation', color=['g'])
    plt.show()
