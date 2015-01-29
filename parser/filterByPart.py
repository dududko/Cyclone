from math import pi
from operator import itemgetter
from lxml import etree as ET

from datetime import datetime
import datetime as dt
import random
from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString, BeautifulSoup
from cyclonep import Cyclone
from utils import distance

cyclones = []

soup = BeautifulSoup(open('..\\test\\result_all_new\\result_all.xml'))  # get the parser for the xml file
# soup = BeautifulSoup(open('..\\test\\result_baltik\\1957.xml'))  # get the parser for the xml file


for i in range(1, len(soup.root.contents), 2):
    cyclone = soup.root.contents[i]
    c = Cyclone()
    c.lifetime = float(cyclone.lifetime.text)
    c.distance = float(cyclone.distance.text)
    c.isBaltik = bool(cyclone.baltik.text == 'True')
    id = 0
    for j in range(7, len(cyclone.contents), 2):
        c.area.append(float(cyclone.contents[j].area.text))
        c.timestamp.append(
            datetime.strptime((cyclone.contents[j].timestamp.text), "%m.%d.%Y %H:%M:%S"))
        #datetime.strptime((cyclone.contents[j].timestamp.text), "%Y-%m-%d %H:%M:%S"))
        c.pressure.append(float(cyclone.contents[j].pressure.text))
        c.outerPressure.append(float(cyclone.contents[j].outerpressure.text))
        c.latitude.append(float(cyclone.contents[j].latitude.text))
        c.longitude.append(float(cyclone.contents[j].longitude.text))
        c.radiusMax.append(float(cyclone.contents[j].radiusmax.text))
        c.radiusMin.append(float(cyclone.contents[j].radiusmin.text))
        #c.radiusMaxMC.append(float(cyclone.contents[j].radiusmaxmc.text))
        #c.radiusMinMC.append(float(cyclone.contents[j].radiusminmc.text))
        c.angle.append(float(cyclone.contents[j].angle.text))
        c.part.append(cyclone.contents[j].part.text)
        if c.radiusMin[-1] > c.radiusMax[-1]:
            c.radiusMin[-1] /= 2
        #if c.radiusMinMC[-1] > c.radiusMaxMC[-1]:
        #    c.radiusMinMC[-1] /= 2
        #c.area2.append(c.radiusMaxMC[-1] * pi * c.radiusMinMC[-1])
        c.ids.append(id)
        id += 1

    cyclones.append(c)
    c.findVelocity()

cyclones = [c for c in cyclones if c.isBaltik]
idsc = []
globalid = 0
for c in cyclones:
    tmp = []
    elem = [0, 0]
    wasAll = False
    for i in c.ids:
        if c.part[i] == 'all':
            if wasAll:
                elem[1] += 1
                wasAll = True
            else:
                elem = [i, 1]
                wasAll = True
        else:
            if wasAll:
                tmp.append(elem)
            wasAll = False
    if wasAll:
        tmp.append(elem)
    globalid += 1
    if len(tmp) == 0:
        continue

    m = max(tmp, key=itemgetter(1))
    mid = tmp.index(m)
    if mid > 0:
        m1 = tmp[mid - 1]
        if m1[0] + m1[1] + 1 == m[0]:
            m[0] = m1[0]
            m[1] += 2
    if mid < len(tmp) - 1:
        m1 = tmp[mid + 1]
        if m[0] + m[1] + 1 == m1[0]:
            m[1] += 2
    if m[1] < 3:
        continue

    c.area = c.area[m[0]:m[0]+m[1]]
    c.timestamp = c.timestamp[m[0]:m[0] + m[1]]
    c.pressure = c.pressure[m[0]:m[0] + m[1]]
    c.outerPressure = c.outerPressure[m[0]:m[0] + m[1]]
    c.latitude = c.latitude[m[0]:m[0] + m[1]]
    c.longitude = c.longitude[m[0]:m[0] + m[1]]
    c.radiusMax = c.radiusMax[m[0]:m[0] + m[1]]
    c.radiusMin = c.radiusMin[m[0]:m[0] + m[1]]
    c.angle = c.angle[m[0]:m[0] + m[1]]
    c.part = c.part[m[0]:m[0] + m[1]]
    if m[1] == 1:
        c.velocity = [c.velocity[m[0]]]
    #c.area2 = c.area2[m[0]:m[0] + m[1]]
    c.ids = c.ids[m[0]:m[0] + m[1]]

    idsc.append(globalid-1)


print(len(cyclones))

cyclones = [cyclones[c] for c in range(len(cyclones)) if c in idsc]
print(len(cyclones))
#####################################################

k = 0
t = 0
t2 = 0
for i in cyclones:
    for x in range(len(i.latitude)):
        if i.part[x] == 'all':
            k += 1
            t += i.area[x] / (i.radiusMax[x] * pi * i.radiusMin[x])
            #t2 += i.area[x] / (i.radiusMaxMC[x] * pi * i.radiusMinMC[x])
print(t / k)
#print(t2 / k)

#####################################################



def isOnBoltik(lat, lon, rMin):
    points =[(6.5, 53.5), (6.5, 66), (33.5, 53.5), (33.5, 53.5)]
    points.append((lat, 53.5))
    points.append((lat, 66))
    points.append((6.5, lon))
    points.append((33.5, lon))
    d = [distance((lat, lon),p) for p in points]
    return min(d) <= rMin or (6.5 <= lon <= 33.5 and 53.5 <= lat <= 66)


def saveToFile(data, name):
    root = ET.Element("root")

    for c in data:
        cyclone = ET.SubElement(root, "cyclone")

        lifetime = ET.SubElement(cyclone, "lifetime")
        lifetime.text = str(c.lifetime)

        distance1 = ET.SubElement(cyclone, "distance")
        distance1.text = str(c.distance)

        # baltik = ET.SubElement(cyclone, "baltik")
        # baltik.text = str(c.isBaltik)

        for i in range(len(c.pressure)):
            cycloneCenter = ET.SubElement(cyclone, "cycloneCenter")

            area = ET.SubElement(cycloneCenter, "area")
            area.text = str(c.area[i])
            time = ET.SubElement(cycloneCenter, "timestamp")
            time.text = str(c.timestamp[i])
            press = ET.SubElement(cycloneCenter, "pressure")
            press.text = str(c.pressure[i])
            oPress = ET.SubElement(cycloneCenter, "outerPressure")
            oPress.text = str(c.outerPressure[i])
            lat = ET.SubElement(cycloneCenter, "latitude")
            lat.text = str(c.latitude[i])
            lon = ET.SubElement(cycloneCenter, "longitude")
            lon.text = str(c.longitude[i])
            rmax = ET.SubElement(cycloneCenter, "radiusMax")
            rmax.text = str(c.radiusMax[i])
            rmin = ET.SubElement(cycloneCenter, "radiusMin")
            rmin.text = str(c.radiusMin[i])
            angle = ET.SubElement(cycloneCenter, "angle")
            angle.text = str(c.angle[i])
            if len(c.pressure) == 1:
                velocity = ET.SubElement(cycloneCenter, "velocity")
                velocity.text = str(c.velocity[0])
            else:
                velocity = ET.SubElement(cycloneCenter, "velocity")
                velocity.text = str(0)

    tree = ET.ElementTree(root)
    tree.write('..\\test\\result_all_new\\' + name + '.xml', pretty_print=True)
    return


saveToFile(cyclones, 'baltik')