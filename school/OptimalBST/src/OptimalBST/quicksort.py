#! /usr/bin/python
#*- encoding: utf8 -*

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="emre"
__date__ ="$Mar 10, 2010 9:19:44 PM$"

import random

def partition (array, left, right, pivotIndex):
    pivotValue = array[pivotIndex]
    array[pivotIndex], array[right] = array[right], array[pivotIndex]
    storeIndex = left
    for i in range(left, right):
        if array[i] <= pivotValue:
            array[i], array[storeIndex] = array[storeIndex], array[i]
            storeIndex+=1
    array[storeIndex], array[right] = array[right], array[storeIndex]
    return storeIndex

def quicksort_recursive(array, left, right):
    if right > left:
        pivotIndex = (left+right)/2 #random.randint(left, right) #(left+right)/2
        pivotNewIndex = partition(array, left, right, pivotIndex)
        quicksort_recursive(array, left, pivotNewIndex - 1)
        quicksort_recursive(array, pivotNewIndex + 1, right)

def quicksort(array):
    quicksort_recursive(array, 0, len(array)-1)

def quicksort2(array):
    less = []
    greater = []

    if len(array) <= 1:
        return array
    
    pivot_index = random.choice(range(len(array)))
    pivot_value = array.pop(pivot_index)

    for x in array:
        if x <= pivot_value:
            less.append(x)
        else:
            greater.append(x)

    x = quicksort2(less)
    y = quicksort2(greater)
    
    #print x
    #print y
    return x + [ pivot_value ] + y
    
            

def quicksort3(A, p, r):
    if p < r:
        q = partition3(A,p,r)
        quicksort3(A,p,q)
        quicksort3(A,q+1,r)
        
def partition3(A,p,r):
    x = A[p]                # first element
    i = p-1                 # index first-1
    j = r+1                 # index last+1
    while True:
        # Move j: ......... <=j
        j-=1
        while not A[j] <= x:
            j-=1
        # Move i: i=>.........
        i+=1
        while not A[i] >= x:
            i+=1

        # If i and j still not crossed
        if i < j:
            A[i], A[j] = A[j], A[i]
        else:
            return j
    
        

    




if __name__ == "__main__":
    l = [9,8,7,6,5,4,3,2,1]
    print "Before:", l
    l = quicksort2(l)
    print "After:", l

    print
    l = [-3,10,-25,198,38,393,3443,44,-1059]
    print "Before:", l
    l = quicksort2(l)
    print "After:", l

    print
    l = [135,763,11,3,0,33,-134,34,3039,231]
    print "Before:", l
    l = quicksort2(l)
    print "After:", l
