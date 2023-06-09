# -*- coding: utf-8 -*-
"""HW4_Q3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HgLUigwMJr4O04xIyYoeyChftsIO6kTf
"""

import numpy as np
import scipy 
import math
from numpy.linalg import inv
import matplotlib.pyplot as plt

def PF_Propagation(t1, Xt1, phiL, phiR, t2, r, w, sigmaL, sigmaR, N):#question: for each point of Xt1, calculte Xt2 with one ibL and one ibR? Where did I get N points?
  if len(Xt1) == 2: #if x0 is the initial pose
    Xt1.append([0,0,1])
    Xt2 = []
    phiL0 = phiL
    phiR0 = phiR
    ibL = np.random.normal(0,sigmaL,N)
    ibR = np.random.normal(0,sigmaR,N)
    Xt2 = []
    for i in range(0,N-1):
      phiL1 = phiL0+ibL[i]
      phiR1 = phiR0+ibR[i]
      velocity = np.array([[0,(-r/w)*(phiR1-phiL1),(r/2)*(phiR1+phiL1)],[(r/w)*(phiR1-phiL1),0,0],[0,0,0]])
      xt2 = np.dot(Xt1,scipy.linalg.expm((t2-t1)*velocity))
      Xt2.append(xt2)
  else: #for non-initial pose
    Xt2 = []
    for i in range(0,N-1):
      ibL = np.random.normal(0,sigmaL)
      ibR = np.random.normal(0,sigmaR)
      phiL1 = phiL+ibL
      phiR1 = phiR+ibR
      xt1 = Xt1[i]
      velocity = np.array([[0,-r/w*(phiR1-phiL1),r/2*(phiR1+phiL1)],[r/w*(phiR1-phiL1),0,0],[0,0,0]])
      xt2 = np.dot(xt1,scipy.linalg.expm((t2-t1)*velocity))
      Xt2.append(xt2)
  return Xt2

def PF_updateStep(Xt, zt, mu, sigmaP):
  w = []
  sigma = sigmaP*np.identity(2)
  for x in Xt:
    eb = x[0]-zt[i,0]
    w[i] = scipy.stats.norm(mu,sigma).pdf(eb)
  Xbar = []
  Xbar = np.random.choice(w, len(Xt))    
  return Xbar

x0 = [[1,0,0],[0,1,0]]
N = 1000
phiL = 1.5
phiR = 2
r = 0.25
w = 0.5
sigmaL = 0.05
sigmaR = 0.05
sigmaP = 0.10
t1 = 0
t2 = 10

points = PF_Propagation(t1, x0, phiL, phiR, t2, r, w, sigmaL, sigmaR, N)
i = 0
l = []
R = []
for p in points:
  l.append([p[0,2],p[1,2]])
  R.append([[p[0,0],p[0,1],[p[1,0],p[1,1]]]])

mean = np.mean(l, axis=0)
cov = np.cov(l)
cov = np.cov(np.array(l)[:,0],np.array(l)[:,1])
print("mean is",mean,"covariance is",cov)

x = np.array(l)[:,0]
y = np.array(l)[:,1]
plt.scatter(x, y, s=1)
plt.show()

t1 = [0,5,10,15]
t2 = [5,10,15,20]
x0 = [[1,0,0],[0,1,0]]
X1 = x0
N = 1000
phiL = 1.5
phiR = 2
r = 0.25
w = 0.5
sigmaL = 0.05
sigmaR = 0.05
sigmaP = 0.10
points = []
color = ["r","g","b","y"]
i = 0

for i in range(len(t2)):
  X1 = PF_Propagation(t1[i], X1, phiL, phiR, t2[i], r, w, sigmaL, sigmaR, N)
  for points_subset in X1:
    l = []
    R = []
    for p in X1:
      # print("points is",p)
      l.append([p[0,2],p[1,2]])
      R.append([[p[0,0],p[0,1],[p[1,0],p[1,1]]]])
    
    x = np.array(l)[:,0]
    y = np.array(l)[:,1]
    plt.scatter(x, y, c=color[i], s=1)
print("i is",i)
plt.show()