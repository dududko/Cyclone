from math import sin, cos, sqrt, atan2, radians, asin, degrees, acos
from numpy import meshgrid, arange
import numpy
from scipy.interpolate import interp2d


def distance(p1, p2):
    R = 6373.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def getPoint(p, d, a):
    R = 6373.0
    l = d / R
    lat1 = radians(p[0])
    lon1 = radians(p[1])
    a = radians(a)

    lat2 = asin(sin(lat1) * cos(l) + cos(lat1) * sin(l) * cos(a))
    dl = atan2(sin(a) * sin(l) * cos(lat1), cos(l) - sin(lat1) * sin(lat2))
    lon2 = lon1 + dl

    return degrees(lat2), degrees(lon2)

def getAzimuth(p1, p2):
    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    b = acos(cos(radians(90) - lat2) * cos(radians(90) - lat1) + sin(radians(90) - lat2) * sin(radians(90) - lat1) * cos(lon2 - lon1))
    A = degrees(asin(sin(radians(90) - lat2) * sin(lon2 - lon1) / sin(b)))

    if A < 0:
        A += 360

    return A


def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def massCenter(points):
    sx = sy = sL = 0
    for i in range(len(points)):  # counts from 0 to len(points)-1
        x0, y0 = points[i - 1]  # in Python points[-1] is last element of points
        x1, y1 = points[i]
        L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        sx += (x0 + x1) / 2 * L
        sy += (y0 + y1) / 2 * L
        sL += L
    xc = sx / sL
    yc = sy / sL
    return xc, yc


def reproject(latitude, longitude):
    """Returns the x & y coordinates in meters using a sinusoidal projection"""
    from math import pi, cos, radians

    earth_radius = 6371009  # in meters
    lat_dist = pi * earth_radius / 180.0

    y = [lat * lat_dist for lat in latitude]
    x = [long * lat_dist * cos(radians(lat))
         for lat, long in zip(latitude, longitude)]
    return x, y


def area_of_polygon(x, y):
    """Calculates the area of an arbitrary polygon given its verticies"""
    area = 0.0
    for i in xrange(-1, len(x) - 1):
        area += x[i] * (y[i + 1] - y[i - 1])
    return abs(area) / 2.0 / 10 ** 6