# -*- coding: utf-8 -*-
"""
@author: Dave
"""
import ReTree as rt

#data must be a list
def cross_validation(data, k = 6, height = 7):
    accuracy = []
    slice_size = int(len(data)/k)
    y = 0
    for x in range(k):
        y = 0
        tree = rt.ReTree(data[(x+1) * slice_size: ] + data[:x * slice_size], height)
        tree.build()
        for row in data[x * slice_size: (x+1) * slice_size]:
            
            if (tree.classify(row[0]) and row[1]) or (not tree.classify(row[0]) and not row[1]):
                y += 1
        accuracy.append(y/slice_size)
    return sum(accuracy)/k



def confusion_matrix(data, height):
    tp, tn, fp, fn =(0,0,0,0)
    
    size = int(0.8 * len(data))
    tree = rt.ReTree(data[:size] , height)
    tree.build()
    for row in data[size:]:
        cl = tree.classify(row[0])
        if cl and row[1]:
            tp += 1
        elif cl and not row[1]:
            fp += 1
        elif not cl and row[1]:
            fn += 1
        else:
            tn += 1
    
    return [[tp,fp],[tn,fn]]
