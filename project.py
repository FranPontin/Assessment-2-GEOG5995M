# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:22:32 2017

@author: fs14fp
"""
# Import modules

import random
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-poster')
import csv



# Pull in the data file 
f = open('wind.raster.txt', newline='') 
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)



# Find out the bombing point.
for i, row in enumerate(reader):
    for j, item in enumerate(row):
        if item > 0:
            x0= j
            y0= i

# Check bombing coordiantes                   
print(x0,y0)



# Plot graph to show start point

# Import empty graph, 300 x 300 (meters)
plt.ylim(0, 300)
plt.xlim(0, 300)

# Plot bombing point on graph
plt.plot(marker='.')
plt.scatter(x0,y0, marker='*')

# Produce visual output
plt.show()



# Create agents (the bacteria)
agents = []



# Print suggested inputs for user to test model
print("To test suggest: number of bacteria= 5000, building height = 75 m and updraft probability = 0.1")



# Define number of agents through user input:

# Instruct user to enter number of agents
num_of_agents_string = input('Enter number of bacteria:')

# Convert string input to an integer
num_of_agents = int(num_of_agents_string)

# Print number of agents as visual confirmation for user
print('Number of bacteria =', num_of_agents)


  
# Define building height (starting Z coordinate) through user input:

# Instruct user to enter building height
z0_string = input('Enter building heigh (m):')

# Convert string input to an integer
z0 = int(z0_string)

# Print building height as visual confirmation for user
print('Building height (m) =',z0 )



# Define probability of an updraft through user input:

# Instruct user to enter probability of an updraft
updraft_float = input('Enter probability of an updraft (enter value between 0.1 and 0.4):')

# Convert string input to a float
updraft = float(updraft_float)

# Print probability of an updraft as visual confirmation for user
print('Probability of an updraft =', updraft)



# Define number of iterations calculated from user input:

# Inform user how the number of iterations is calculated 
print('Number of iterations = probaility x 100 x building height, to ensure all bacteria have fallen to the ground when recorded')

# Calcualte number of iterations
num_of_iterations_float = (z0 * updraft * 100)

# Convert float output to an integer output
num_of_iterations = int(num_of_iterations_float)

# Print number of iterations as visual confirmation for user
print('Number of iterations', num_of_iterations)



# Define starting coordinates of the agents (the bombing point)

for i in range(num_of_agents):
    agents.append([y0,x0,z0])



# Agent movement due to updraft and wind direction

for k in range(num_of_agents):
    for l in range(num_of_iterations):
    # Movement due to updraft 
    
    # Generate random floats
    # Name random float randUP so elevation based on different random numbers to those determining NSEW direction
        randUP=random.random()
        
        # How agents will move if above the height of the building:
        if agents[k][2] >= z0:
            
            # If the generated random float is less than the inputted updraft, the bacteria will rise 1m per iteration
            if randUP < updraft:
                agents[k][2] = agents[k][2] + 1
            
            # There is a 10% chance of no elevation change
            # If: inputted updraft < generated random float < inputted updraft +0.1, the bacteria will not change elevation
            elif randUP < updraft +0.1:
                agents[k][2] = agents[k][2]
            
            # If the generated random float is greater than the inputted updraft, the bacteria will fall 1m per iteration
            else:
                agents[k][2] = agents[k][2] - 1
        
        # If the bacteria is bellow the building height there is no updraft and the bacteria falls 1m per iteration
        elif agents[k][2] > 0: 
            agents[k][2]= agents[k][2] -1
        
        # If the elevation =0 then bacteria has reached the ground and does fall any further
        else:
            agents[k][2]=agents[k][2]      
            
        # Moving NSEW
        
        # Generate random float
        # Name random float randNSEW so elevation based on different random numbers to those determining updraft
        randNSEW=random.random()
        
        # Bacteria move based on wind direction as long as their elevation is greater than 0 i.e. haven't reached the ground yet
        if agents[k][2] > 0:
            
            # There is 5% chance of the wind direction blowing the bacteria west
            # If: the generated random float < 0.05 the bacteria moves 1m west per iteration
            if randNSEW < 0.05:
                agents[k][1] = agents[k][1] - 1
            
            # There is 10% chance of the wind direction blowing the bacteria north
            # If: 0.05 < generated random float < 0.15 the bacteria moves 1m north per iteration
            elif randNSEW < 0.15:
                agents[k][0] = agents[k][0] + 1
            
            # There is 10% chance of the wind direction blowing the bacteria south
            # If: 0.15 < generated random float < 0.25 the bacteria moves 1m south per iteration
            elif randNSEW < 0.25:
                agents[k][0] = agents[k][0] - 1
            
            # There is 75% chance of the wind direction blowing the bacteria east
            # If: the generated random float > 0.25 the bacteria moves 1m east per iteratio
            else:
                agents[k][1] = agents[k][1] + 1
        
        # The bacteria do not move if they have reached the ground
        else:
            agents[k][1] = agents[k][1]
            agents[k][0] = agents[k][0]



# Find the mean of the final coordinates of the bacteria:

# Calculate mean 
mean = np.mean(agents, axis=0)

# Convert from array to list
listmean = list(mean)

# Print mean endpoint as visual information for the user
print('Mean end-point of the bacteria', listmean)



# Find the furthest east and north co-ordiantes: 

# Calculate max coordinates of the bacteria (largest x and largest y co-ordinates)
max = np.max(agents, axis=0)

# Convert from array to list
listmax = list(max)

# Print maximum endpoints as visual information for the user
print('Furthest east and north points', listmax)



# Find the furthest west and south co-ordinates:
    
# Calculate the min coordinates of the bacteria (smallest x and smallest y coordinates)
min = np.min(agents, axis=0)

# Convert from array to list
listmin = list(min)

# Print minimum endpoints as visual information for the user
print('Furthest west and sorth points', listmin)


#Create 300x300 density map of bacteria

# Plot empty graph, 300 x 300 (meters)
plt.ylim(0, 300)
plt.xlim(0, 300)

# Plot bacteria end locations
for k in range(num_of_agents):
    plt.scatter(agents[k][1],agents[k][0], marker='.', s=20)

# Plot bombing point on graph
plt.scatter(x0,y0, marker='*', color='dodgerblue')

# Plot mean end point
plt.scatter(listmean[1], listmean[0], marker='x', color='red') 

# Produce visual output
plt.show()

# Save output as an image
plt.savefig('bacterial_bomb_output.png')



#Create a zoomed and centred density map of bacteria:

# Plot graph with size based on max and min coordinates of furthest agents

# Y coordinates of graph centered around bacteria location
plt.ylim((listmin[0]-5),(listmax[0]+5))

# X coordiantes of graph centred around bacteria location and bombing point
plt.xlim(45,(listmax[1]+5))

# Plot bacteria end locations
for k in range(num_of_agents):
    plt.scatter(agents[k][1],agents[k][0], marker='.', s=20, )

# Plot bombing point on graph
plt.scatter(x0,y0, marker='*',color='dodgerblue')

# Plot mean end point
plt.scatter(listmean[1], listmean[0], marker='x', color='red') 

# Produce visual output
plt.show()

# Save output as an image
plt.savefig('bacterial_bomb_output_centered.png')


# Read out a CSV file:

# Produce CSV output of bacteria location, if all the bacteria are still within the original 300x300 parameter, of the read in data:   
if listmax[0] and listmax[1] <= 300:
    # Open csv writer
    f2 = open('dataout.csv', 'w', newline='') 
    writer = csv.writer(f2, delimiter=',')
    
    # Create blank output list
    output = []
    
    #Create a 300 by 300 environment of 0s:
    for i in range(300):
        tempList = list()
        for j in range(300):
            tempList.append(0)
        output.append(tempList)
    
    # Add agent locations to environment:
    for i, row in enumerate(agents):
        x = row[1]
        y = row[0]
    
    # If there is an agent present in a location, 1 will be added to that point
        output[x][y] += 1       
    
    # Write file
    for row in output:
        writer.writerow(row)

# If all the bacteria are not within the original 300x300 parameter, of the read in data, no CSV output is produced:    
else:
    
    # A message is displayed to the user indicating no file has been produced
    print("Output area too large to produce comparable CSV file")



# Close the files

f2.close()       
f.close()    
