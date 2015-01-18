from matplotlib.widgets import Button
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
from cycloneDetector import getNextCycloneData


class Index:
    indFile = 0
    indTime = 0

    def next(self, event):
        self.indTime += 1
        print(self.indTime)

        data = getNextCycloneData(self.indFile, self.indTime)

        update(fig, data, m)
        #l.set_ydata(ydata)

    def prev(self, event):
        print self.indTime
        self.indTime -= 1
        if self.indTime < 0:
            self.indTime = 0
            self.indFile -= 1
            if self.indFile < 0:
                self.indFile = 0
        #l.set_ydata(ydata)
        #plt.draw()

fig = []
data = []
m = []
def drawPlot(data):
    lat_1 = data.lat[0]
    lat_0 = data.lat[-1]
    lon_1 = data.lon[0]
    lon_0 = data.lon[-1]

    fig = plt.figure()

    m = Basemap(llcrnrlon=lon_1, llcrnrlat=lat_0, urcrnrlon=lon_0, urcrnrlat=lat_1,
                rsphere=(6378137.00,6356752.3142),
                resolution='l', projection='merc',
                lat_0=40., lon_0=-20., lat_ts=20.
    )
    # nylat, nylon are lat/lon of New York
    nylat = 40.78;
    nylon = -73.98
    # lonlat, lonlon are lat/lon of London.
    lonlat = 51.53;
    lonlon = 0.08
    # draw great circle route between NY and London
    # m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')

    update(fig, data, m)

    axprev = plt.axes([0.4, 0.0, 0.1, 0.075])
    axnext = plt.axes([0.51, 0.0, 0.1, 0.075])

    callback = Index()

    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    # set full screen
#    mng = plt.get_current_fig_manager()
    ### works on Ubuntu??? >> did NOT working on windows
    # mng.resize(*mng.window.maxsize())
#    mng.window.state('zoomed') #works fine on Windows!
    plt.show() #close the figure to run the next section

def update(fig, data, m):
    ax = fig.add_axes([0.1, 0.15, 0.8, 0.8])

    clevs = np.arange(900, 1100., 5.)
    # find x,y of map projection grid.
    lons, lats = np.meshgrid(data.lon, data.lat)
    x, y = m(lons, lats)
    # create figure.
    cs = m.contour(x, y, data.data, clevs, colors='k', linewidths=1.)

    m.drawcoastlines()
    m.fillcontinents()
    # draw parallels
    m.drawparallels(np.arange(0, 90, 10), labels=[1, 1, 0, 1])
    # draw meridians
    m.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1])

    ax.set_title('Great Circle from New York to London')
    plt.draw()

#######################################