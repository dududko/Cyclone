import sys
import datetime
from matplotlib.patches import Polygon
from scipy.ndimage.filters import minimum_filter
from cyclone import Cyclone
from scipy import interpolate
import numpy as np
from utils import getPoint, distance, diff, massCenter, reproject, area_of_polygon, getAzimuth
from matplotlib import _cntr as cntr
from lxml import etree as ET

import scipy.ndimage as ndimage


class CycloneDatabase:
    def __init__(self):
        self.cyclones = []
        self.lastCyclones = []
        self.colors = ['b', 'g', 'r', 'y']

    def updateCyclonesPath(self, cycls):
        for i in range(0, len(self.lastCyclones)):
            cycl1 = self.lastCyclones[i]
            cycl1.wasChanged = False
            if len(cycls) == 0:
                continue
            distances = [distance(cycl1.getLastPosition(), cycl2.getLastPosition()) for cycl2 in cycls]
            val, idx = min((val, idx) for (idx, val) in enumerate(distances))
            distances1 = [distance(cycls[idx].getLastPosition(), cycl2.getLastPosition()) for cycl2 in
                          self.lastCyclones]
            val1 = min(distances1)
            for i in range(len(distances1)):
                if distances1[i] == val1:
                    idx1 = i
                    break

            distances2 = [distance(cycl1.pos[-1], cycl2.pos[0]) for cycl2 in cycls]

            if (val < 700 and val <= val1) or (distances2[idx] < 700) \
                    or (len(self.lastCyclones) == 1 and val < 1000):
                cycl1.appendParams(cycls[idx].pos[0],
                                   cycls[idx].ids[0],
                                   cycls[idx].msl[0],
                                   cycls[idx].vor[0])
                # cycl1.appendPos(cycls[idx].pos[0])
                cycl1.dom = cycls[idx].dom
                # if 700 > distance(cycl1.mcPos[-1], cycls[idx].mcPos[0]) < distance(cycl1.mcPos[-1], cycls[idx].pos[0]):
                # cycl1.appendMassCenter(cycls[idx].mc[0])
                # cycl1.appendMassCenterPos(cycls[idx].mcPos[0])
                #else:
                #    cycl1.appendMassCenter(cycls[idx].ids[0][::-1])
                #    cycl1.appendMassCenterPos(cycls[idx].pos[0])
                cycl1.appendMassCenter(cycls[idx].mc[0])
                cycl1.appendMassCenterPos(cycls[idx].mcPos[0])
                cycl1.time.append(cycls[idx].time[0])
                cycl1.omsl.append(cycls[idx].omsl[0])
                cycl1.area.append(cycls[idx].area[0])
                cycl1.rad.append(cycls[idx].rad[0])
                cycl1.angle.append(cycls[idx].angle[0])
                cycl1.distance += distance(cycl1.pos[-2], cycl1.pos[-1])

                cycl1.setMaximums(cycls[idx].maximums)
                cycl1.wasChanged = True
                if cycl1.isBaltik or cycls[idx].isBaltik:
                    cycl1.isBaltik = True
                cycls = np.delete(cycls, idx)
        idx = [idx for (idx, val) in enumerate(self.lastCyclones) if not val.wasChanged]
        for i in idx:
            # flag = self.filterNonCyclones(self.lastCyclones[i])
            if self.lastCyclones[i].lifetime > 12:  # and self.lastCyclones[i].isBaltik:
                self.cyclones.append(self.lastCyclones[i])
        lastIdx = list(set(range(0, len(self.lastCyclones))) - set(idx))
        res = []
        for i in lastIdx:
            res.append(self.lastCyclones[i])
        for i in idx:
            self.colors.append(self.lastCyclones[i].color)
        for i in range(len(cycls)):
            cycls[i].color = self.colors.pop()
        self.lastCyclones = res
        self.lastCyclones = np.concatenate((self.lastCyclones, cycls))


    # those, wose:
    # 1) lifetime less than 12h
    # 2)
    def filterNonCyclones(self, c):
        return c.lifetime > 12

    def saveToFile(self, year):
        root = ET.Element("root")

        for c in self.cyclones:
            cyclone = ET.SubElement(root, "cyclone")

            lifetime = ET.SubElement(cyclone, "lifetime")
            lifetime.text = str(c.lifetime)

            distance1 = ET.SubElement(cyclone, "distance")
            distance1.text = str(c.distance)

            baltik = ET.SubElement(cyclone, "baltik")
            baltik.text = str(c.isBaltik)

            for i in range(len(c.msl)):
                cycloneCenter = ET.SubElement(cyclone, "cycloneCenter")

                area = ET.SubElement(cycloneCenter, "area")
                area.text = str(c.area[i])
                time = ET.SubElement(cycloneCenter, "timestamp")
                time.text = str(c.time[i])
                press = ET.SubElement(cycloneCenter, "pressure")
                press.text = str(c.msl[i])
                oPress = ET.SubElement(cycloneCenter, "outerPressure")
                oPress.text = str(c.omsl[i])
                lat = ET.SubElement(cycloneCenter, "latitude")
                lat.text = str(c.mcPos[i][0])
                lon = ET.SubElement(cycloneCenter, "longitude")
                lon.text = str(c.mcPos[i][1])
                rmax = ET.SubElement(cycloneCenter, "radiusMax")
                rmax.text = str(c.rad[i][1])
                rmin = ET.SubElement(cycloneCenter, "radiusmin")
                rmin.text = str(c.rad[i][0])
                angle = ET.SubElement(cycloneCenter, "angle")
                angle.text = str(c.angle[i])

        tree = ET.ElementTree(root)
        tree.write('test\\result_all\\' + year + ".xml", pretty_print=True)
        return


class CycloneData:
    def __init__(self, msl, lat, lon, time, timeID, sigma, size):
        self.sigma = sigma
        self.size = size
        self.timeID = timeID
        self.time = time
        self.lon = lon
        self.lat = lat
        self.msl = 0.01 * msl
        ###################################################################################
        # need to detect contours
        self.mslArr = np.array(self.msl)
        # self.mslArr += 5
        # self.mslArr = ndimage.gaussian_filter(self.mslArr, sigma=(sigma, size), order=0)
        # self.mslArr -= 5
        self.x, self.y = np.mgrid[:self.mslArr.shape[0], :self.mslArr.shape[1]]
        # self.y = self.y.max() - self.y
        self.c = cntr.Cntr(self.y, self.x, self.mslArr)

        ###################################################################################
        self.mins = self.extrema(self.msl)
        self.func = self.interpolate()
        self.lati = interpolate.interp1d(range(len(lat)), lat)
        self.loni = interpolate.interp1d(range(len(lon)), lon)
        self.mins = self.filterByMaxValue(self.mins)
        res = []

        t = datetime.datetime.now()
        t1 = []
        self.cyclones = []
        for i in range(len(self.mins[0])):
            isCycl, meanMSL, maximums = self.isCyclone([self.mins[0][i], self.mins[1][i]])
            if isCycl:
                res.append(i)
                self.cyclones.append(Cyclone(self.msl[(self.mins[0][i], self.mins[1][i])],
                                             (lat[self.mins[0][i]], lon[self.mins[1][i]]),
                                             (self.mins[0][i], self.mins[1][i]),
                                             meanMSL, "", 0, time))
                self.cyclones[-1].setMaximums(maximums)
        self.cyclones = self.concatNeighbours(self.cyclones)
        t1.append((datetime.datetime.now() - t).total_seconds())
        t = datetime.datetime.now()
        # self.cyclones = self.filterBorders(self.cyclones)
        # self.defineDomain()
        self.outerIsobar()
        t1.append((datetime.datetime.now() - t).total_seconds())
        # self.findRauses()
        # self.massCenter()
        print t1


    def extrema(self, msl, mode='wrap', window=3):
        """find the indices of local extrema (min and max)
        in the input array."""
        mn = minimum_filter(msl, size=window, mode=mode)
        # mx = maximum_filter(mat, size=window, mode=mode)
        # (mat == mx) true if pixel is equal to the local max
        # (mat == mn) true if pixel is equal to the local in
        # Return the indices of the maxima, minima
        return np.nonzero(msl == mn)

    def isCyclone(self, pID):
        lo = self.lon[pID[1]]
        la = self.lat[pID[0]]

        dirs = range(0, 359, 45)
        # dists = range(50, 851, 50)
        dists = range(50, 851, 50)
        mDists = range(0, 8)
        mMSL = range(0, 8)
        mLatLon = range(0, 8)
        count = 0
        maximums = []
        for a in dirs:
            grad = 0
            maximum = []
            for d in dists:
                p1 = getPoint((la, lo), d, a)
                msl1 = self.func(p1[1], p1[0])
                msl0 = self.func(lo, la)
                # grad1 = (msl1 - self.msl[pID[0]][pID[1]]) / d
                grad1 = (msl1 - msl0) / d
                if grad < grad1:
                    grad = grad1
                if grad1 > 0.015:
                    mDists[a / 45] = d
                    mMSL[a / 45] = msl1
                    mLatLon[a / 45] = p1
            if grad > 0.015:
                count += 1
                # for i in range(len(self.lat)):
                # if mLatLon[a / 45][0] >= self.lat[i]:
                # break
                # for j in range(len(self.lon)):
                # if mLatLon[a / 45][1] <= self.lon[j]:
                # break
                # x1 = [i for i, x in enumerate(self.lat) if (len(maximum) > 0.) & (abs(x - maximum[0]) < 0.125)]
                #y1 = [i for i, x in enumerate(self.lon) if (len(maximum) > 0.) & (abs(x - maximum[1]) < 0.125)]
                #if (len(x1) > 0) & (len(y1) > 0):
                #maximums.append([i, j])
        res = 0
        if count >= 6:
            res = sum(mMSL) / count

        return count >= 6, res, maximums

    def interpolate(self):
        return interpolate.interp2d(self.lon, self.lat, self.mslArr)

    def filterByMaxValue(self, m):
        v = self.msl[m]
        res = []
        for i in range(0, len(v)):
            if v[i] < 985:
                res.append(i)
        return m[0][res], m[1][res]

    def concatNeighbours(self, m):
        m = np.array(m)
        remove = []
        for i in range(0, len(m)):
            for j in range(i + 1, len(m)):
                if distance(m[i].pos[0], m[j].pos[0]) < 1000:
                    if m[i].msl < m[j].msl:
                        remove.append(j)
                    else:
                        remove.append(i)
        res = diff(range(0, len(m)), remove)
        return m[res]

    def outerIsobar(self):
        remove = []
        for j in range(len(self.cyclones)):
            c = self.cyclones[j]

            msl = c.msl[0] + 1
            isClosed = True
            k = 0
            area = 1
            area1 = 1
            delta = 1
            d = 1
            d1 = 1

            s1 = []
            dom = []
            # print("#######################")
            # print ("segments")

            while isClosed:
                k += 1
                isClosed = False
                res = self.c.trace(msl)
                nseg = len(res) // 2
                segments, codes = res[:nseg], res[nseg:]

                for i in range(len(segments)):

                    s = segments[i]
                    if s[0][1] == 0 and s[-1][1] == 0:
                        point = self.getMidPoint(s[0], s[-1])
                        point = self.lonToIdx(point[0]), self.latToIdx(point[1])
                        s = np.vstack((s, [point[0], 0]))
                        #s = np.vstack((s, [(s[0][0] + s[-1][0]) / 2, 0]))
                    if s[0][0] == 0 and s[-1][0] == 0:
                        point = self.getMidPoint(s[0], s[-1])
                        point = self.lonToIdx(point[0]), self.latToIdx(point[1])
                        s = np.vstack((s, [0, point[1]]))
                        #s = np.vstack((s, [0, c.ids[0][0]]))
                    if s[0][0] == len(self.lon) - 1 and s[-1][0] == len(self.lon) - 1:
                        point = self.getMidPoint(s[0], s[-1])
                        point = self.lonToIdx(point[0]), self.latToIdx(point[1])
                        s = np.vstack((s, [len(self.lon) - 1, point[1]]))
                        #s = np.vstack((s, [len(self.lon) - 1, (s[0][1] + s[-1][1]) / 2]))
                    if s[0][1] == 0 and s[-1][0] == 0:
                        s = np.vstack((s, [0, 0]))
                    if s[0][1] == 0 and s[-1][0] == len(self.lon) - 1:
                        s = np.vstack((s, [len(self.lon) - 1, 0]))

                    # last added point was top right corner
                    if s[-1][0] == len(self.lon) - 1 and s[-1][1] == 0:
                        point = self.getMidPoint(s[0], s[-1])
                        point = self.lonToIdx(point[0]), self.latToIdx(point[1])
                        s = np.vstack((s, [point[0], 0]))

                    # last added point was top left corner
                    if s[-1][0] == 0 and s[-1][1] == 0:
                        point = self.getMidPoint(s[0], s[-1])
                        point = self.lonToIdx(point[0]), self.latToIdx(point[1])
                        s = np.vstack((s, [point[0], 0]))

                    p = Polygon(s)

                    if p.contains_point([c.ids[0][1], c.ids[0][0]]) or \
                            (c.ids[0][0] == 0 and s[0][0] <= c.ids[0][1] <= s[-1][0]) or \
                            (c.ids[0][0] == 0 and s[0][0] <= c.ids[0][1] <= s[-2][0]) or \
                            (c.ids[0][1] == 0 and s[0][1] >= c.ids[0][0] >= s[-2][1]) or \
                            (c.ids[0][1] == 0 and s[0][1] >= c.ids[0][0] >= s[-1][1]):
                        #(s[0][1] == c.ids[0][0] and s[0][0] <= c.ids[0][1]) or \

                        s2 = s1
                        s1 = s
                        area1 = area
                        d1 = d

                        x, y = zip(*s)
                        x = self.loni(list(x))
                        y = self.lati(list(y))
                        x, y = reproject(y, x)

                        area = area_of_polygon(list(x), list(y))

                        #print k, "msl:", msl, area / area1

                        la1 = self.lat[int(s[0][1])]
                        lo1 = self.lon[int(s[0][0])]
                        la2 = self.lat[int(s[-1][1])]
                        lo2 = self.lon[int(s[-1][0])]

                        d = distance((la1, lo1), (la2, lo2))

                        if d <= 1000:
                            dom = s
                            isClosed = True

                        delta1 = area / area1 - delta
                        delta = area / area1
                        #print (k, msl, delta, d, area)
                        if (((area / area1) > 1.19) and (14 > k > 12) and msl > 980) \
                                or (((area / area1) > 5) and (k >= 5)) \
                                or (((area / area1) > 1.5) and (k >= 10) and msl > 970) \
                                or (30 > k > 20 and delta1 > 0.08) \
                                or (35 > k > 30 and delta1 > 0.06) \
                                or (k >= 35 and delta1 > 0.10) \
                                or (k > 40 and d1 != 0 and d / d1 > 1.5 and d > 500) \
                                or (k < 10 and d > 500):
                            dom = s2
                            isClosed = False

                        if isClosed and 5 >= abs(msl - c.msl[0]):
                            mc = massCenter(dom)
                            mcPos = (self.lat[int(mc[1])], self.lon[int(mc[0])])
                            c.setMassCenter(mc)
                            c.setMassCenterPos(mcPos)

                        if isClosed and k < 20:
                            dists = [distance(c.mcPos[0], (self.lati(i[1]), self.loni(i[0]))) for i in
                                     dom[0:(len(dom) - 4)]]
                            c.setRadius((min(dists), max(dists)))
                            maxIdx = dists.index(max(dists))
                            maxPos = (self.lati(dom[maxIdx][1]), self.loni(dom[maxIdx][0]))
                            c.setAngle(getAzimuth(c.mcPos[0], maxPos))

                if len(dom) == 0:
                    remove.append(j)

                msl += 0.5

            c.omsl.append(msl - 0.5)
            c.area.append(area1)
            c.setDomain(dom)
            self.checkBaltik(c)

        res = diff(range(0, len(self.cyclones)), remove)
        self.cyclones = self.cyclones[res]

    def filterBorders(self, m):
        m = np.array(m)
        remove = []
        for i in range(0, len(m)):
            x0 = m[i].ids[0][0]
            y0 = m[i].ids[0][1]
            if any([x0 == 0, y0 == 0, x0 == self.x[-1][0], y0 == self.y[0][-1]]):
                remove.append(i)
        res = diff(range(0, len(m)), remove)
        return m[res]

    def findRauses(self):
        for c in self.cyclones:
            dists = [distance(c.mcPos[0], (self.lati(i[1]), self.loni(i[0]))) for i in c.dom]
            c.setRadius((min(dists), max(dists)))

    def getMidPoint(self, p1, p2):
        p = ((self.lon[int(p1[0])] + self.lon[int(p2[0])]) / 2, (self.lat[int(p1[1])] + self.lat[int(p2[1])]) / 2)
        return p

    def latToIdx(self, l):
        k = 0
        for i in self.lat:
            if i <= l:
                return k
            k += 1

    def lonToIdx(self, l):
        k = 0
        for i in self.lon:
            if i >= l:
                return k
            k += 1

    def checkBaltik(self, c):
        isB = False
        for p in c.dom:
            plat = self.lat[int(p[1])]
            plon = self.lon[int(p[0])]
            if 6.5 <= plon <= 33.5 and 53.5 <= plat <= 66:
                isB = True
                break
        if isB:
            c.isBaltik = True
