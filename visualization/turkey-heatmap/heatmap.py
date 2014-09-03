#encoding: utf-8
import sys
from scipy import interpolate
import math
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
import numpy as np
import networkx as nx
import pylab as P #
import random

from matplotlib import pyplot as plt
from matplotlib import mlab

f = open("turkey2.csv")
lons = []
lats = []
stations = []
dusts = []


for line in f:
    line = line.strip()
    if not line.replace(";",""):
        continue
    print line
    station, dust, lat, lon = line.split(";")
    if not dust:
        dust = random.randint(0,20)
        
    lons.append(lon)
    lats.append(lat)
    stations.append(station)
    dusts.append(dust)


def conv(x):
    try:
        x = x.encode("utf-8")
    except:
        x = x.decode("utf-8")
    return x
lons = map(float, lons)
lats = map(float, lats)
dusts = map(float, dusts)
stations = map(conv, stations)
print dusts
def meshgrid(x,y):
    """
    Return coordinate matrices from two coordinate vectors.

    Parameters
    ----------
    x, y : ndarray
        Two 1-D arrays representing the x and y coordinates of a grid.

    Returns
    -------
    X, Y : ndarray
        For vectors `x`, `y` with lengths ``Nx=len(x)`` and ``Ny=len(y)``,
        return `X`, `Y` where `X` and `Y` are ``(Ny, Nx)`` shaped arrays
        with the elements of `x` and y repeated to fill the matrix along
        the first dimension for `x`, the second for `y`.

    See Also
    --------
    index_tricks.mgrid : Construct a multi-dimensional "meshgrid"
                         using indexing notation.
    index_tricks.ogrid : Construct an open multi-dimensional "meshgrid"
                         using indexing notation.

    Examples
    --------
    >>> X, Y = np.meshgrid([1,2,3], [4,5,6,7])
    >>> X
    array([[1, 2, 3],
           [1, 2, 3],
           [1, 2, 3],
           [1, 2, 3]])
    >>> Y
    array([[4, 4, 4],
           [5, 5, 5],
           [6, 6, 6],
           [7, 7, 7]])

    `meshgrid` is very useful to evaluate functions on a grid.

    >>> x = np.arange(-5, 5, 0.1)
    >>> y = np.arange(-5, 5, 0.1)
    >>> xx, yy = np.meshgrid(x, y)
    >>> z = np.sin(xx**2+yy**2)/(xx**2+yy**2)

    """
    x = np.asarray(x)
    y = np.asarray(y)
    numRows, numCols = len(y), len(x)  # yes, reversed
    x = x.reshape(1,numCols)
    X = x.repeat(numRows, axis=0)

    y = y.reshape(numRows,1)
    Y = y.repeat(numCols, axis=1)
    return X, Y
    
def draw():
    
    print max(lons)
    print min(lats)
    delta = 0.1
    xmin = min(lons) - 4
    xmax =  max(lons) + 5
    ymin = min(lats) - 14
    ymax = max(lats) + 14
#    m = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=90, #Y
#                llcrnrlon=-90,urcrnrlon=90,resolution='c')     # X
    m = Basemap(projection='cyl',llcrnrlat=ymin,urcrnrlat=ymax,\
                llcrnrlon=xmin,urcrnrlon=xmax,resolution='c')

    m.drawcoastlines()
    m.drawcountries(linewidth=0.1)

    #m.bluemarble() 
    #m.fillcontinents(color='white',lake_color='aqua')
    # draw parallels and meridians.

    #m.drawparallels(np.arange(-90.,91.,30.))
    #m.drawmeridians(np.arange(-180.,181.,60.))
    #m.drawmapboundary(fill_color='aqua')

    plt.title("Saudi Arabia")

    
    print ymin, ymax
    xdelta = xmax - xmin
    ydelta = ymax - ymin
    if ydelta > xdelta:
        xmax += ydelta - xdelta
    elif ydelta < xdelta:
        ymax += xdelta - ydelta
    x = np.arange(xmin, xmax, delta)
    y = np.arange(ymin, ymax, delta)

    X, Y = P.meshgrid(x, y)
    print x.shape
    print y.shape
    #Z = dusts
    #X, Y = meshgrid(lons,lats)
#    print X
#    print Y
#    I2 = interpolate.interp2d(rows, cols, z, kind='linear')

    #Z = (P.sqrt(X)**2 + P.sqrt(Y)**2) #
    #Z = np.sin(X**2+Y**2)/(X**2+Y**2)    
    Z = np.zeros(X.shape)
#    Z[1:4,...] = 30
    
    for i in xrange(len(lats)):
        xx = float("%.1f" % lons[i])
        xi = (xx-xmin)/delta        
        yy = float("%.1f" % lats[i])
        yi = (yy-ymin)/delta
        dust = dusts[i]
        Z[xi,yi] = dust
        #print dust        
        
    #print X
#    print Y
    print Z
#    f = interpolate.interp2d(X, Y, Z)
    grid_x, grid_y = np.mgrid[xmin:xmax:delta, ymin:ymax:delta]
#    print grid_x
    coords = np.array([lats, lons]).T
 #   print coords.shape
    grid_z0 = griddata(coords, np.array(dusts), (grid_x, grid_y), method='cubic')
 #   print grid_z0.shape
    

    #print f
#    print x
#    print X
    CP1 = P.contourf(X,Y,grid_z0, cmap="OrRd")
    P.clabel(CP1, inline=True, fontsize=10)
#    plt.clim(-4,4)
    P.colorbar(CP1)

    

    # lat/lon coordinates of five cities.
    #lats = [40.02, 32.73, 38.55, 48.25, 17.29]
    #lons = [-105.16, -117.16, -77.00, -114.21, -88.10]
    #cities=['Boulder, CO','San Diego, CA',
    #        'Washington, DC','Whitefish, MT','Belize City, Belize']
    cities = stations
    # compute the native map projection coordinates for cities.
    xc,yc = m(lons,lats)
    # plot filled circles at the locations of the cities.
    m.plot(xc,yc,'y.')
    # plot the names of those five cities.
    for name,xpt,ypt in zip(cities,xc,yc):
        plt.text(xpt+50000,ypt+50000,name)
        
    fig = plt.gcf()
    fig.set_size_inches(18.5,10.5)

    plt.savefig('map.png',dpi=200)
    

draw()
