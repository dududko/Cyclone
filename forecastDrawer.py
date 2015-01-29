import os

from netCDF4 import Dataset
from matplotlib.widgets import Button
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math
import numpy as np
import datetime as dt

# open netCDF file for reading
from scipy.ndimage import minimum_filter
from cyclone import Cyclone
from cycloneData import CycloneData, CycloneDatabase
from utils import getPoint

###############################################################################
#####       Define sigma & size

gaussSigma = 1
gaussSize = 10
globalID = 6

###############################################################################

print('list of files')
for fn in os.listdir('E:\\ifmo_damb\\data\\'):
    print fn

class FileData:
    def __init__(self, yearNum):
        year = '%s' % yearNum
        filename = 'E:\\ifmo_damb\\data\\netcdf_' + year + '.nc'
        self.ncfile = Dataset(filename, 'r')

        self.press =    self.ncfile.variables['msl']
        self.lats =     self.ncfile.variables['latitude']
        self.lons =     self.ncfile.variables['longitude']
        self.time =     self.ncfile.variables['time']
        offset = dt.timedelta(hours=0)
        # List of all times in the file as datetime objects
        self.dt_time = [dt.datetime(1900, 1, 1) + dt.timedelta(hours=t) - offset \
           for t in self.time]
        print self.dt_time[0]

    def readYear(self, yearNum):
        year = '%s' % yearNum
        filename = 'E:\\ifmo_damb\\data\\netcdf_' + year + '.nc'
        self.ncfile = Dataset(filename, 'r')

        self.press =    self.ncfile.variables['msl']
        self.lats =     self.ncfile.variables['latitude']
        self.lons =     self.ncfile.variables['longitude']
        self.time =     self.ncfile.variables['time']
        offset = dt.timedelta(hours=6)
        # List of all times in the file as datetime objects
        self.dt_time = [dt.datetime(1900, 1, 1) + dt.timedelta(hours=t) - offset \
           for t in self.time]


    def clearFile(self):
        self.ncfile.close()

#yearNum = [1957, 1969, 1980, 1991]
yearNum = [1957, 1963, 1970, 1975, 1982, 1986, 1993, 1997][globalID]
fileData = FileData(yearNum)


##############################################################################################


def get_contour_verts(cn):
    contours = []
    # for each contour line
    for cc in cn.collections:
        paths = []
        # for each separate section of the contour line
        for pp in cc.get_paths():
            xy = []
            # for each segment of that section
            for vv in pp.iter_segments():
                xy.append(vv[0])
            paths.append(np.vstack(xy))
        contours.append(paths)

    return contours


##############################################################################################


def getNextCycloneData(indFile, indTime):
    return CycloneData(fileData.press[indTime], fileData.lats, fileData.lons, fileData.dt_time[indTime].strftime("%m.%d.%Y %H:%M:%S"), indTime, gaussSigma, gaussSize)

##############################################################################################


class Index:
    def __init__(self, year):
        self.yearNum = year
        self.indFile = 0
        self.indTime = 0
        self.globalInd = 0
        self.stopInd = len(fileData.press) - 1
        self.stopYear = [1962, 1969, 1974, 1981, 1985, 1992, 1996, 2002][globalID+1]

    def next(self):
        if self.globalInd == self.stopInd and self.yearNum == self.stopYear:
            cycloneDatabase.updateCyclonesPath([])
            cycloneDatabase.saveToFile("%s" % self.yearNum)
            exit()
        elif self.globalInd == self.stopInd:
            cycloneDatabase.updateCyclonesPath([])
            cycloneDatabase.saveToFile("%s" % self.yearNum)
            self.yearNum += 1
            self.indTime = 0
            self.globalInd = 0
            self.indFile += 1
            fileData.clearFile()
            fileData.readYear(self.yearNum)
            self.stopInd = len(fileData.press) - 1
        else:
            self.indTime += 1
            self.globalInd += 1
        data = getNextCycloneData(self.indFile, self.indTime)
        cycloneDatabase.updateCyclonesPath(data.cyclones)
        print(self.indTime, self.indFile)
        return True

    def prev(self):
        self.indTime -= 1
        data = getNextCycloneData(self.indFile, self.indTime)


##############################################################################################

callback = Index(yearNum)
data = getNextCycloneData(callback.indFile, callback.indTime)
cycloneDatabase = CycloneDatabase()
cycloneDatabase.updateCyclonesPath(data.cyclones)

while (callback.next()):
    continue

print '*** SUCCESS reading example file sfc_pres_temp.nc!'
