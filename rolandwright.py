from numpy.random import randint
import pandas as pd

def roland_wright(x:int)->dict:
    """
    param: x
    roll die x times, record how many rolls were required before a six resulted in a dictionary
    """
    
    results = dict()
    
    for _ in range(x):
        count = 0
        res = 0
    
        while res != 6:
            count += 1
            res = randint(1, 7)
        
        if count in results.keys():
            results[count] +=1
        else:
            results[count] = 1
        
        
    return(results)