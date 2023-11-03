'''
Created on 16 Nov 2022

Test code for pyTestbed

@author: brian
'''
from genutils import * 

import os
import sys
import pytestbed as ptb

def test1():
    """
    Basic test
    """
    
    myDir = "../TestDir"
        
    printf("Starting cur dir = {}", os.getcwd())
    printf("Starting len(sys.path) = {}", len(sys.path))
    
    runner = ptb.PyTestbed(myDir, seed=80572461469, clean=True, repeats=3)
    
    printf("Before cur dir = {}", os.getcwd())
    printf("Before len(sys.path) = {}", len(sys.path))
    
    runner.run_all()
    #runner.run_one("tst2", seed=41937211981, clean=True, repeats=5)
    
    printf("After cur dir = {}", os.getcwd())
    printf("After len(sys.path) = {}", len(sys.path))
    
    



#========================================================================
# Execution hook
#========================================================================
if __name__ == "__main__":
    test1()
    pass


