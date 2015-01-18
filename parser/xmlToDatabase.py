from lxml import etree as ET

from datetime import datetime
import datetime as dt
import random
from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString, BeautifulSoup
from cyclonep import Cyclone

cyclones = []

soup = BeautifulSoup(open('..\\test\\result_all\\europe\\europe.xml'))  # get the parser for the xml file
#soup = BeautifulSoup(open('..\\test\\result_baltik\\1957.xml'))  # get the parser for the xml file


for i in range(1, len(soup.root.contents), 2):
    cyclone = soup.root.contents[i]
    c = Cyclone()
    c.lifetime = float(cyclone.lifetime.text)
    c.distance = float(cyclone.distance.text)
    #c.isBaltik = bool(cyclone.baltik.text == 'True')
    for j in range(7, len(cyclone.contents), 2):
        c.area.append(float(cyclone.contents[j].area.text))
        c.timestamp.append(
            #datetime.strptime((cyclone.contents[j].timestamp.text), "%m.%d.%Y %H:%M:%S"))
            datetime.strptime((cyclone.contents[j].timestamp.text), "%Y-%m-%d %H:%M:%S"))
        c.pressure.append(float(cyclone.contents[j].pressure.text))
        c.outerPressure.append(float(cyclone.contents[j].outerpressure.text))
        c.latitude.append(float(cyclone.contents[j].latitude.text))
        c.longitude.append(float(cyclone.contents[j].longitude.text))
        c.radiusMax.append(float(cyclone.contents[j].radiusmax.text))
        c.radiusMin.append(float(cyclone.contents[j].radiusmin.text))
        c.angle.append(float(cyclone.contents[j].angle.text))
    cyclones.append(c)

'''
fluidDates = []
fluidDatesIn = [[1957,25,10,170],
[1958,18,5,168 ],
[1961,31,3,189 ],
[1961,7,12,171 ],
[1962,13,9,175 ],
[1963,17,11,203],
[1964,14,12,214],
[1967,14,10,171],
[1967,18,10,244],
[1967,19,10,178],
[1968,30,10,175],
[1969,11,11,166],
[1971,22,12,162],
[1973,10,10,179],
[1973,20,12,240],
[1974,17,10,242],
[1975,9,1,216  ],
[1975,11,1,164 ],
[1975,29,9,281 ],
[1975,23,12,176],
[1975,31,12,187],
[1975,31,12,170],
[1976,8,1,167  ],
[1977,7,9,231  ],
[1978,15,11,204],
[1978,19,11,164],
[1978,20,11,204],
[1978,22,11,200],
[1979,14,9,195 ],
[1979,28,9,165 ],
[1979,5,12,172 ],
[1979,6,12,172 ],
[1980,30,12,166],
[1981,21,10,178],
[1982,25,11,216],
[1982,17,12,215],
[1983,14,1,178 ],
[1983,21,1,184 ],
[1983,26,9,182 ],
[1983,28,9,174 ],
[1983,20,10,190],
[1983,22,10,170],
[1983,25,10,168],
[1983,1,11,198 ],
[1983,3,11,200 ],
[1983,25,11,172],
[1984,1,1,231  ],
[1984,4,1,181  ],
[1985,26,10,216],
[1986,3,10,182 ],
[1986,2,12,207 ],
[1986,4,12,190 ],
[1986,6,12,260 ],
[1989,17,1,177 ],
[1989,30,1,173 ],
[1989,29,3,199 ],
[1990,27,1,168 ],
[1990,22,2,200 ],
[1990,27,2,161 ],
[1990,25,3,162 ],
[1991,10,1,166 ],
[1991,11,1,201 ],
[1991,22,11,173],
[1991,30,12,184],
[1992,5,1,175  ],
[1993,23,1,204 ],
[1993,21,12,168],
[1994,2,10,219 ],
[1994,4,10,184 ],
[1994,12,10,228],
[1994,16,10,163],
[1994,24,11,172],
[1998,19,10,220],
[1999,30,11,262],
[2001,15,11,216],
[2002,26,1,171 ],
[2002,5,2,182  ],
[2002,10,3,182 ]]


print len(fluidDatesIn)

for c in fluidDatesIn:
    fluidDates.append(datetime(c[0], c[2], c[1]) - dt.timedelta(days=1))
#fluidDates.append(datetime(1967, 10, 18) - dt.timedelta(days=1))
#fluidDates.append(datetime(1973, 12, 20) - dt.timedelta(days=1))
#fluidDates.append(datetime(1974, 11, 17) - dt.timedelta(days=1))#---------------- bad cyclone
#fluidDates.append(datetime(1975, 9, 29) - dt.timedelta(days=1))#----------------
#fluidDates.append(datetime(1977, 9, 7) - dt.timedelta(days=1))
#fluidDates.append(datetime(1984, 1, 1) - dt.timedelta(days=1))
#fluidDates.append(datetime(1986, 12, 6) - dt.timedelta(days=1))
#fluidDates.append(datetime(1994, 10, 12) - dt.timedelta(days=1)) #---------
#fluidDates.append(datetime(1999, 11, 30) - dt.timedelta(days=1))  # ok


#cyclones = [c for c in cyclones if c.isBaltik]
water = []
resId = []
i = 0
for c in cyclones:
    flag = False
    for ts in c.timestamp:
        id = 0
        for fd in fluidDates:
            if 1 >= abs((ts - fd).days):
                flag = True
                break
            id+=1
        if flag:
            break
    if flag:
        water.append(id)
        resId.append(i)
        flag = False
    i += 1
cyclones = [cyclones[i] for i in resId]
water = [fluidDatesIn[i][3] for i in water]

print len(cyclones)
'''
import matplotlib.pyplot as plt
import numpy as np


'''plt.figure(1)
x = [c.lifetime for c in cyclones]
print max(x)
hist, bins = np.histogram(x, bins=range(3, int(max(x)) + 10, 6))
width = 1 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
avg = 0
for i in range(len(hist)):
    avg += hist[i] * bins[i]
avg /= sum(hist)
plt.title("hist of lifetime of cyclones; average is %s hours" % avg)
plt.bar(center, hist, align='center', width=width)
plt.show()

plt.figure(2)
x = [c.distance for c in cyclones]
print max(x)
hist, bins = np.histogram(x, bins=range(0, int(max(x)) + 100, 200))
width = 1 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
avg = 0
for i in range(len(hist)):
    avg += hist[i] * bins[i]
avg /= sum(hist)
plt.title("histogram of traveled distance; average is %s km" % avg)
plt.bar(center, hist, align='center', width=width)
plt.show()


x = []
for c in cyclones:
    for i in c.radiusMax:
        x.append(i)
print max(x)
hist, bins = np.histogram(x, bins=range(0, int(max(x)) + 100, 20))
width = 1 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
avg = 0
for i in range(len(hist)):
    avg += hist[i] * bins[i]
avg /= sum(hist)
plt.title("histogram of cyclones max radius; average is %s km" % avg)
plt.bar(center, hist, align='center', width=width)
plt.show()


x = []
for c in cyclones:
    for i in c.radiusMin:
        x.append(i)
print max(x)
hist, bins = np.histogram(x, bins=range(0, int(max(x)) + 100, 20))
width = 1 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
avg = 0
for i in range(len(hist)):
    avg += hist[i] * bins[i]
avg /= sum(hist)
plt.title("histogram of cyclones min radius; average is %s km" % avg)
plt.bar(center, hist, align='center', width=width)
plt.show()'''



#####################################################

writer = open("lifetime.csv", "wb")
entries = ['%s\n' % i.lifetime for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("distance.csv", "wb")
entries = ['%s\n' % i.distance for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("area.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.area)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("timestamp.csv", "wb")
entries = ['%s  \n' % ",".join((x.strftime("%Y.%m.%d %H:%M:%S") for x in i.timestamp)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("pressure.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.pressure)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("latitude.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.latitude)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("longitude.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.longitude)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("radiusMax.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.radiusMax)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("radiusMin.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.radiusMin)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("angle.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.angle)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################

writer = open("outerPressure.csv", "wb")
entries = ['%s  \n' % ",".join((format(x, "10.3f") for x in i.outerPressure)) for i in cyclones]
for e in entries:
    writer.write(e)
writer.close()

#####################################################
'''
writer = open("water_traj.csv", "wb")
entries = ['%s\n' % format(i, "10.3f") for i in water]
for e in entries:
    writer.write(e)
writer.close()
'''
#####################################################



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
            rmin = ET.SubElement(cycloneCenter, "radiusmin")
            rmin.text = str(c.radiusMin[i])
            angle = ET.SubElement(cycloneCenter, "angle")
            angle.text = str(c.angle[i])

    tree = ET.ElementTree(root)
    tree.write('..\\test\\result_all\\' + name + '.xml', pretty_print=True)
    return


saveToFile(cyclones, 'baltik_flood_traj')

#cyclonesb = [c for c in cyclones if len([True for i in range(len(c.latitude)) if 6.5 <= c.longitude[i] <= 33.5 and 53.5 <= c.latitude[i] <= 66]) > 0]
#cyclonesb = [c for c in cyclones if c.isBaltik or len([True for i in range(len(c.latitude)) if 6.5 <= c.longitude[i] <= 33.5 and 53.5 <= c.latitude[i] <= 66]) > 0]
#saveToFile(cyclonesb, 'baltik1')
