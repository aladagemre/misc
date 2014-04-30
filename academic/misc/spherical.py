"""
These functions allow you to calculate spherical distance between two coordinates on the earth.
"""
import numpy as np
from math import *

def new_get_distances(loc1, loc2):
    """
    Use this to take advantage of numpy.
    Calculates spherical distance between two coordinates in miles.
    Sample input:
    loc1 = np.array([(1.0, 0.0), (0.0, 1.0), (3.0, 4.0)])
    loc2 = np.array([(1.0, 0.0), (0.0, 1.0), (3.0, 4.0)])
    
    Output:
    NxN distance matrix
    [[   0.           97.71009074  308.83105631]
     [  97.71009074    0.          293.07071058]
     [ 308.83105631  293.07071058    0.        ]]    
    """
    earth_radius = 3958.75

    locs_1 = np.deg2rad(loc1)
    locs_2 = np.deg2rad(loc2)

    lat_dif = (locs_1[:,0][:,None]/2 - locs_2[:,0]/2)
    lon_dif = (locs_1[:,1][:,None]/2 - locs_2[:,1]/2)

    np.sin(lat_dif, out=lat_dif)
    np.sin(lon_dif, out=lon_dif)

    np.power(lat_dif, 2, out=lat_dif)
    np.power(lon_dif, 2, out=lon_dif)

    lon_dif *= ( np.cos(locs_1[:,0])[:,None] * np.cos(locs_2[:,0]) )
    lon_dif += lat_dif

    np.arctan2(np.power(lon_dif,.5), np.power(1-lon_dif,.5), out = lon_dif)
    lon_dif *= ( 2 * earth_radius )

    return lon_dif
    

def distance(pos1, pos2):
    """
    Distance between two points in miles.
    Pure-python
    """
    R = 6373.0
    lat1, lon1 = pos1
    lat2, lon2 = pos2

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    result = R * c

    return result*0.621371


def ndistance(pos1, pos2):
    """
    Distance between two points in miles.
    """
    R = 6373.0
    pos1 = np.radians(pos1)
    pos2 = np.radians(pos2)
    diff = np.subtract(pos2, pos1)

    a = np.sin(diff[0]/2.0)**2 + np.cos(pos1[0]) * np.cos(pos2[0]) * np.sin(diff[1]/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c * 0.621371

def spherical_dist(pos1, pos2, r=3958.75):
    """
    Distance between two points in miles
    """
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))
    
    
loc1 = np.array([(1.0, 0.0), (0.0, 1.0), (3.0, 4.0)])
loc2 = np.array([(1.0, 0.0), (0.0, 1.0), (3.0, 4.0)])
print new_get_distances(loc1, loc2)
