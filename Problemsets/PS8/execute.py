# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:07:25 2019

@author: Devashish
"""

# Calling in the wagner-whitin function and checking the output
y=wagner_whitin(100,7,1,400,500,[70,90,140,150,120,130],0)
y

#### Min cost vs starting inventory ####
evaluated_cost={'start inv':[],'cost':[]}
for si in range(0,400,5):
    x=wagner_whitin(100,7,1,400,500,[70,90,140,150,120,130],si)
    evaluated_cost['start inv'].append(si)
    evaluated_cost['cost'].append(x['Minimum Cost'])

# Plotting Min cost vs. starting inventory:
import matplotlib.pyplot as plt
fig, ax = plt.subplots() # make figure and axes separate objects
plt.plot(evaluated_cost['start inv'],evaluated_cost['cost'])
plt.xlabel('Starting Inv')
plt.ylabel('Minimum Cost')
plt.show()
fig.savefig('Cost vs starting inventory.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")

### Plotting Min cost vs. per unit holding cost #####
comparative_stats={'holding cost':[],'cost':[]}
for hc in np.linspace(0,1,100):
    z=wagner_whitin(100,7,hc,400,500,[70,90,140,150,120,130],0)
    comparative_stats['holding cost'].append(hc)
    comparative_stats['cost'].append(z['Minimum Cost'])

fig, ax = plt.subplots() # make figure and axes separate objects
plt.plot(comparative_stats['holding cost'],comparative_stats['cost'])
plt.xlabel('Per Unit Holding Cost')
plt.ylabel('Minimum Cost')
plt.show()
fig.savefig('Total cost vs per unit holding cost.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")


#### Plot the production policy #####

fig, ax = plt.subplots() # make figure and axes separate objects
plt.step(range(1,len(y['Production_Schedule'])+2),
         y['Production_Schedule']+[0],where='post')
plt.xlabel('Time Period')
plt.ylabel('Production Amounts')
plt.show()
fig.savefig('Production Policy.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")

#### Plot the inventory policy #####
ig, ax = plt.subplots() # make figure and axes separate objects
plt.step(range(1,len(y['Inventory_Schedule'])+2),
         y['Inventory_Schedule']+[0],where='post')
plt.xlabel('Time Period')
plt.ylabel('Inventory Amounts')
plt.show() 
fig.savefig('Inventory Policy.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")


