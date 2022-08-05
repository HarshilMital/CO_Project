import matplotlib.pyplot as plt
import numpy as np
#import 
#import 

#temp values
CyclesX = [10,20,30,40,50]
MemY = [4,11,5,4,6]


plt.scatter(Cycles, Memory, color='teal', marker='.')
plt.title('Memory Address vs Cycle Number', fontsize=14)
plt.xlabel('Cycle Number', fontsize=14)
plt.ylabel('Memory Address', fontsize=14)
plt.show()