#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:41:41 2021

@author: yasi
"""

import random
import sys
import math
import numpy as np
import csv
from matplotlib import pyplot as plt

# initialize prototype values randomly in the range (min_p, max_p)
def initPrototypes(k, num_dim, min_p, max_p):
    prototypes = []
    for i in range(k):
        proto = []
        for j in range(num_dim):
            proto.append(random.uniform(min_p, max_p))
        prototypes.append(proto)
    return prototypes

# returns finalized cluster mean values along with the clustered datapoints when given the initial data-set by X
# k - number of clusters required
# min_p/max_p - minimum/maximum value for initial prototype values
def kmeans(X, k, min_p, max_p):
    num_dim = len(X[0])
    
    # intializing protoptypes as random points
    prototypes = initPrototypes(k, num_dim, min_p, max_p)
        
    val_changed = True    
    # check if prtototype values have not been changed    
    while(val_changed):
        val_changed = False
        # initializing a map to store resultant clusters
        clusters = {}
        for i in range(k):
            clusters[i] = []
            
        for x_i in range(len(X)):
            min_dis = sys.maxsize * 2
            c_i = 0
            # checking with each prototype
            for p_i in range(k):
                dis_sq = 0
                for dim_i in range(num_dim):
                    dis_sq += math.pow(X[x_i][dim_i] - prototypes[p_i][dim_i], 2)
                new_dis = math.sqrt(dis_sq)
                if new_dis < min_dis:
                    min_dis = new_dis
                    c_i = p_i
            clusters[c_i].append(X[x_i])
            
        # re-initialize prototype values if there is any cluster with zero elements
        null_cluster = False
        for c_i in clusters:
            if len(clusters[c_i]) == 0:
                null_cluster = True
        if null_cluster:
            prototypes = initPrototypes(k, num_dim, min_p, max_p)
            val_changed = True
            continue
        
        # update new prototype values
        for c_i in clusters:
            new_val = np.mean(np.array(clusters[c_i]), axis=0)
            if np.all(new_val != prototypes[c_i]):
                val_changed = True
            prototypes[c_i] = new_val
    return prototypes, clusters

# util functions
def readDataBlobs():
    Y = []
    X = []
    with open('data/blobs.csv') as file:
        reader = csv.reader(file)
        line_index = 0
        for row in reader:
            if line_index > 1:
                Y.append([int(row[0][0])])
                x_list = row[0][2:].split()
                X.append([float(x_list[0]), float(x_list[1])])
            line_index += 1
    return X, Y

def readDataFlame():
    Y = []
    X = []
    with open('data/flame.csv') as file:
        reader = csv.reader(file)
        line_index = 0
        for row in reader:
            if line_index > 4:
                Y.append([int(row[0][0])])
                x_list = row[0][2:].split()
                X.append([float(x_list[0]), float(x_list[1])])
            line_index += 1
    return X, Y

# plots visually the formation of clusters
def plot(prototypes, clusters):
    if len(P[0]) != 2:
        return        
    fig=plt.figure()
    ax=fig.add_axes([0,0,1,1])
    colors = ['b', 'g', 'y', 'cyan', 'grey']
    for c_i in clusters:
        x = []
        y = []
        for i in range(len(clusters[c_i])):
            x.append(clusters[c_i][i][0])
            y.append(clusters[c_i][i][1])
        ax.scatter(x, y, color=colors[c_i])
        
    p_x = []
    p_y = []
    for i in range(len(P)):
        p_x.append(prototypes[i][0])
        p_y.append(prototypes[i][1])
        
    ax.scatter(p_x, p_y, color='r')
    plt.show()

X, Y = readDataBlobs()
P, clusters = kmeans(X, 3, -0.5, 0.5)
plot(P, clusters)

X, Y = readDataFlame()
P, clusters = kmeans(X, 4, 1, 5)
plot(P, clusters)