# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 17:47:46 2021

@author: Owner
"""
import pandas as pd

import numpy as np

 

#import distance matrix, format correctly, put into numpy array

df = pd.read_csv("C:/Users/Owner/OneDrive/Documents/OSU 4/ISE/distance_matrix.csv")

df = df.iloc[:,1:66]

dist = df.to_numpy()

 

for i in range(len(dist)):

    for j in range(len(dist)):

        dist[i,j] = dist[j,i]

 

print(dist)

 

import cvxpy as cp
x = cp.Variable((65,65), boolean = True)

m,n=x.shape

 

t = cp.Variable(65, nonneg = True)

 

c = dist

 

print(len(c))

 

obj_func=cp.trace(c.T @ x)

 

constraints = []

for j in range(n):

    #Each j index is only included once

    constraints.append(cp.sum(x[:,j]) == 1)

 

for i in range(m):
    
    #each i index is only included once

    constraints.append(cp.sum(x[i,:]) == 1)

 

for i in range(m):
    
    #never include i=j

    constraints.append(cp.sum(x[i,i]) == 0)

    

############ No subtours

for i in range(0,65):

    for j in range(1,65):

        constraints.append(t[i] - t[j] + 65*x[i,j] <= 64)

 

############# Constraints for each Conference

 
#ACC conference
constraints.append(cp.sum(x[36:51,36:51]) == 14)
#travel to ACC from another conference
constraints.append(cp.sum(x[0:36,36:51]) + cp.sum(x[51:65,36:51]) == 1)               

  
#Pac 12 conference
constraints.append(cp.sum(x[24:36,24:36]) == 11)
#travel to ACC before Pac 12
constraints.append(cp.sum(x[36:51,24:36]) == 1)

 
#Big 10 conference
constraints.append(cp.sum(x[0:14,0:14]) == 13)
#travel to Ohio State from SEC
constraints.append(cp.sum(x[51:65,0]) == 1)    

 
#Big 12 conference
constraints.append(cp.sum(x[14:24,14:24]) == 9)
#Travel to Big 12 from another conference
constraints.append(cp.sum(x[0:14,14:24]) + cp.sum(x[24:65,15:24]) == 1)

 
#SEC conference
constraints.append(cp.sum(x[51:65,51:65]) == 13)
#Travel to SEC from another conference
constraints.append(cp.sum(x[0:51,51:65])  == 1) 

 

##############No Duplicate state names

#Michigans
constraints.append(x[3,4] + x[4,3] == 0)
#Iowas
constraints.append(x[8,15] + x[15,8] == 0)
#Kansas
constraints.append(x[16,17] + x[17,16] == 0)
#Oklahoma
constraints.append(x[18,19] + x[19,18] == 0)
#Arizona
constraints.append(x[24,25] + x[25,24] == 0)
#California
constraints.append(x[26,27] + x[27,26] + x[26,31] + x[31,26] + x[27,31] + x[31,27] == 0)
#Oregon
constraints.append(x[29,30] + x[30,29] == 0)
#Washington
constraints.append(x[34,35] + x[35,34] == 0)
#Carolina
constraints.append(x[40,47] + x[47,40] + x[40,55] + x[55,40] + x[47,55] + x[55,47] == 0)
#Mississippi
constraints.append(x[62,63] + x[63,62] == 0)
#Virginia
constraints.append(x[49,50] + x[50,49] == 0)
#Georgia
constraints.append(x[52,45] + x[45,52] == 0)
#Florida
constraints.append(x[51,38] + x[38,51] == 0)
#Texas
constraints.append(x[20,21] + x[21,20] + x[20,22] + x[22,20] + x[20,64] + x[64,20] + x[21,22] + x[22,21] + x[21,64] + x[64,21] + x[22,64] + x[64,22] == 0)

  

problem = cp.Problem(cp.Minimize(obj_func), constraints)

 

#problem.solve(solver=cp.CVXOPT,verbose = True)

problem.solve(solver=cp.GUROBI,verbose = True)




print("obj_func =")

print(obj_func.value)

print("x =")

print(x.value)

print("t=")

print(t.value)

x_output =  np.asarray(x.value)

np.savetxt("C:/Users/Owner/OneDrive/Documents/OSU 4/ISE/xoutput.csv", x_output, delimiter=",")

