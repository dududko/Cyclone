import os

from netCDF4 import Dataset


# open netCDF file for reading
from cycloneData import CycloneData, detPotCycl
from plotDrawer import drawPlot


print('list of files')
for fn in os.listdir('E:\\ifmo_damb\\data\\'):
    print fn

ncfile = Dataset('E:\\ifmo_damb\\data\\netcdf_2001.nc', 'r')

press = ncfile.variables['msl']
for i in ncfile.variables:
    print(i)
print(press.units)

print("pres")
print(len(press))
print(len(press[0]))
print(len(press[0][0]))

print
print("lats")
lats = ncfile.variables['latitude']
print(lats.units)
print(len(lats))

print
print("lons")
lons = ncfile.variables['longitude']
print(lons.units)
print(len(lons))

print
print("time")
time = ncfile.variables['time']
print(len(time))
print(time[0])
print(time[1])

cycloneData1 = CycloneData(press[0], lats, lons, time[0], 0)
cycls = detPotCycl(cycloneData1.data)
print(len(cycls))
print(cycloneData1.max)
print(cycloneData1.min)

drawPlot(cycloneData1)

ncfile.close()
print '*** SUCCESS reading example file sfc_pres_temp.nc!'

def getNextCycloneData(indFile, indTime):
    return CycloneData(press[indTime], lats, lons, time[indTime], indTime)