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

###############################################################################

print('list of files')
for fn in os.listdir('E:\\ifmo_damb\\data\\'):
    print fn

ncfile = Dataset('E:\\ifmo_damb\\data\\netcdf_2000.nc', 'r')

press = ncfile.variables['msl']
for i in ncfile.variables:
    print(i)
print(press.units)

print("pres")
print(len(press))
print(len(press[0]))
print(len(press[0][0]))
press[0:10,0:10]

print
print("lats")
lats = ncfile.variables['latitude']
print(lats.units)
print(len(lats))
lats[60:160]

print
print("lons")
lons = ncfile.variables['longitude']
print(lons.units)
print(len(lons))
lons[268:484]

print
print("time")
time = ncfile.variables['time']
print(len(time))
print(time[0])
print(time[1])

offset = dt.timedelta(hours=0)
# List of all times in the file as datetime objects
dt_time = [dt.datetime(1900, 1, 1) + dt.timedelta(hours=t) - offset \
           for t in time]

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
    #return CycloneData(press[indTime][60:160, 268:484],
    return CycloneData(press[indTime],
                       #lats[60:160],
                       lats,
                       #lons[268:484],
                       lons,
                       dt_time[indTime].strftime("%m.%d.%Y %H:%M:%S"), indTime, gaussSigma, gaussSize)


##############################################################################################


class Index:
    indFile = 0
    # indTime = 229
    indTime = 9
    globalInd = 0
    #stopInd = len(press) - 1
    stopInd = 1360

    def next(self):
        if self.globalInd == self.stopInd:
            cycloneDatabase.updateCyclonesPath([])
            cycloneDatabase.saveToFile()
            exit()
        self.indTime += 1
        self.globalInd += 1
        data = getNextCycloneData(self.indFile, self.indTime)
        cycloneDatabase.updateCyclonesPath(data.cyclones)
        update(data)
        # l.set_ydata(ydata)
        print(self.indTime, self.indFile)

    def prev(self):
        self.indTime -= 1
        data = getNextCycloneData(self.indFile, self.indTime)
        update(data)

##############################################################################################

callback = Index()
data = getNextCycloneData(callback.indFile, callback.indTime)
cycloneDatabase = CycloneDatabase()
cycloneDatabase.updateCyclonesPath(data.cyclones)

lat_1 = data.lat[0]
lat_0 = data.lat[-1]
lon_1 = data.lon[0]
lon_0 = data.lon[-1]

fig = plt.figure()
ax = fig.add_axes([0.1, 0.15, 0.8, 0.8])
m = Basemap(llcrnrlon=lon_1, llcrnrlat=lat_0, urcrnrlon=lon_0, urcrnrlat=lat_1,
            rsphere=(6378137.00, 6356752.3142),
            resolution='l', projection='merc',
            lat_0=40., lon_0=-20., lat_ts=20.
)
# nylat, nylon are lat/lon of New York
nylat = 40.78
nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53
lonlon = 0.08
# draw great circle route between NY and London
# m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')

clevs = np.arange(900, 1100., 5.)


def update(data):
    ax.cla()
    # draw parallels
    m.drawparallels(np.arange(0, 90, 10), labels=[1, 1, 0, 1])
    # draw meridians
    m.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1])

    # find x,y of map projection grid.
    lons, lats = np.meshgrid(data.lon, data.lat)
    x, y = m(lons, lats)

    # draw levels
    cs = m.contour(x, y, data.msl, clevs, colors='k', linewidths=1.)
    fmt = '%.0f'
    plt.clabel(cs, cs.levels, inline=1, fmt=fmt, fontsize=10)

    # p = get_contour_verts(cs)
    #
    # p = cs.collections[20].get_paths()[0]
    # v = p.vertices
    # x = v[:, 0]
    #y = v[:, 1]

    m.drawcoastlines()
    m.fillcontinents()

    mins = ([], [])
    for i in data.cyclones:
        mins[0].append(i.ids[0][0])
        mins[1].append(i.ids[0][1])
    mins = (np.array(mins[0]), np.array(mins[1]))
    if len(mins[0]) == 0:
        mins = []
    xlows = x[mins]
    # xhighs = x[local_max]
    ylows = y[mins]
    # yhighs = y[local_max]
    lowvals = data.msl[mins]
    #highvals = prmsl[local_max]
    # plot lows as blue L's, with min pressure value underneath.
    xyplotted = []
    # don't plot if there is already a L or H within dmin meters.
    yoffset = 0.022 * (m.ymax - m.ymin)
    dmin = yoffset

    for cycl in cycloneDatabase.lastCyclones:
        p1 = cycl.mcPos[0]
        for i in range(1, len(cycl.pos)):
            p2 = cycl.mcPos[i]
            m.drawgreatcircle(p2[1], p2[0], p1[1], p1[0], linewidth=1.0, color='r')
            p1 = p2

    for i in range(0, len(data.cyclones)):
        for j in range(0, 8):
            d = 100
            a = j * 45
            p0 = data.cyclones[i].pos[0]
            p1 = getPoint(p0, d, a)
            m.drawgreatcircle(p0[1], p0[0], p1[1], p1[0], linewidth=1, color='b')

    for x1, y1, p in zip(xlows, ylows, lowvals):
        if x1 < m.xmax and x1 > m.xmin and y1 < m.ymax and y1 > m.ymin:
            dist = [np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) for x0, y0 in xyplotted]
            if not dist or min(dist) > dmin:
                plt.text(x1, y1, 'L', fontsize=14, fontweight='bold',
                         ha='center', va='center', color='r')
                plt.text(x1, y1 - yoffset, repr(int(p)), fontsize=9,
                         ha='center', va='top', color='r',
                         bbox=dict(boxstyle="square", ec='None', fc=(1, 1, 1, 0.5)))
                xyplotted.append((x1, y1))

    cur_time = dt_time[callback.indTime]

    colors = ['g', 'b', 'r']
    for k in range(len(cycloneDatabase.lastCyclones)):
        c = cycloneDatabase.lastCyclones[k]
        for i in range(len(c.dom)):
            c.dom[i][0] = x[0][c.dom[i][0]]
            c.dom[i][1] = y[c.dom[i][1]][0]
        p = plt.Polygon(c.dom, fill=False, color=c.color, linewidth=2)
        ax.add_artist(p)

        p1 = c.mc[-1]
        #p = plt.Circle([y[-1][0] - y[int(p1[1])][0], x[0][-1] - x[0][int(p1[0])]], 100000, color='g')
        p = plt.Circle([x[0][int(p1[0])], y[int(p1[1])][0]], 10000, color='r')
        #p = plt.Circle([x[0][i[1]], y[i[0]][0]], 100000, color=colors[k])
        ax.add_artist(p)
        for i in c.maximums:
            #p = plt.Circle([y[i[1]][0], x[0][-1] - x[0][i[0]]], 100000)
            p = plt.Circle([x[0][i[1]], y[i[0]][0]], 100000, color=colors[k])
            ax.add_artist(p)

    plt.title("time %s" % cur_time)
    #fig.savefig('result_traj\\figure_' + `gaussSigma` + '_' + `gaussSize` + '_' + `callback.indTime` + '.png', dpi=100)
    fig.savefig('result_pics\\figure_1994_' + `callback.indTime` + '.png', dpi=100)
    plt.draw()

# set full screen
mng = plt.get_current_fig_manager()
### works on Ubuntu??? >> did NOT working on windows
mng.window.state('zoomed')  # works fine on Windows!

update(data)


def key_event(e):
    global curr_pos

    if e.key == "right":
        while (True):
            callback.next()
    elif e.key == "left":
        callback.prev()
    elif e.key == 'escape':
        exit()
    else:
        return


fig.canvas.mpl_connect('key_press_event', key_event)

plt.show()  # close the figure to run the next section

ncfile.close()
print '*** SUCCESS reading example file sfc_pres_temp.nc!'