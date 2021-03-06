#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 22:30:13 2019
Title:Clustering via K-Means 
"""

import numpy as np 

def init_centers(X, k):
    """
    Randomly samples k observations from X as centers.
    Returns these centers as a (k x d) numpy array.
    """
    samples = np.random.choice(len(X), size=k, replace=False)
    return X[samples, :]


def compute_d2(X, centers):
    """
    Function that computes a distance matrix S=(sij), 
    sij = d2ij = squared distance from point xi to center uj
    Return to numpy matrix S[:m, :k]
    """
    m = len(X)
    k = len(centers)  
    S = np.empty((m,k))
    for i in range(m):
        S[i,:] = np.linalg.norm(X[i, :] - centers, ord=2, axis=1)**2
    return S 


def assign_cluster_labels(S):
    """
    Function that uses squared distance matrix to assign a cluster label to each point
    m x k squared distance matrix S, if sij = min.squared distance for point i,
    index j as cluster label.
    Return a col vector y of length m 
    """
    mins = []
    for i in S:
        mins.append(np.argmin(i))
    return mins
    

def update_centers(X, y):
    """
    Compute the center of each cluster
    """
    # X[:m, :d] == m points, each of dimension d
    # y[:m] == cluster labels
    m, d = X.shape 
    k = max(y) + 1 
    assert m == len(y)
    assert (min(y) >= 0)
    
    centers = np.empty((k, d))
    for j in range(k):
        # Compute the new center of cluster j, centers[j, :d]
        centers[j, :] = np.mean(X[y == j, :], axis = 0)
    return centers


def WCSS(S):
    """
    Return within-cluster sum of squares given the sequared distances 
    """
    return np.sum(np.amin(S, axis=1)) #np.amin return min of an array 


def has_converged(old_centers, centers):
    """
    Function to check whether centers have moved given two instances of the center values
    Need to account the order of centers may have changed
    """
    return set([tuple(x) for x in old_centers]) == set(([tuple(x) for x in centers]))


def kmeans(X, k, starting_centers=None, max_steps=np.inf):
    """
    Put all preceding building blocks to implement Lloyd's k-mean algorithm
    """
    if starting_centers is None:
        centers = init_centers(X, k)
    else: 
        centers = starting_centers
    
    converged = False
    labels = np.zeros(len(X))
    i = 1
    while (not converged) and (i <= max_steps):
        old_centers = centers
        
        S = compute_d2(X, old_centers)
        labels = np.asarray(assign_cluster_labels(S))
        centers = update_centers(X, labels)
        converged = has_converged(old_centers, centers)
        print("iteration", i, "WCSS =", WCSS(S))
        i += 1
    return labels 

