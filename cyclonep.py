from utils import distance


class Cyclone:

    def __init__(self):
        self.lifetime = 0
        self.distance = 0
        self.isBaltik   = False

        self.area           = []
        self.timestamp      = []
        self.pressure       = []
        self.outerPressure  = []
        self.latitude       = []
        self.longitude      = []
        self.radiusMax      = []
        self.radiusMin      = []
        self.radiusMaxMC    = []
        self.radiusMinMC    = []
        self.angle          = []
        self.part           = []
        self.area2          = []
        self.ids            = []
        self.depth          = []
        self.velocity       = []

    def findVelocity(self):
        if len(self.longitude) == 1:
            return
        self.velocity = []
        lon1 = self.longitude[0]
        lat1 = self.latitude[0]

        for i in range(1, len(self.longitude)):
            lon2 = self.longitude[i]
            lat2 = self.latitude[i]
            d = distance((lat1, lon1), (lat2, lon2))
            lon1 = lon2
            lat1 = lat2
            if d < 500:
                self.velocity.append(d/6)
            else:
                self.velocity.append(450/6)

    def filterByID(self, idin):
        self.lifetime = 0
        self.distance = 0
        self.isBaltik   = False

        self.area           = [self.area         [id] for id in range(len(self.area         ))  if id in idin]
        self.timestamp      = [self.timestamp    [id] for id in range(len(self.timestamp    ))  if id in idin]
        self.pressure       = [self.pressure     [id] for id in range(len(self.pressure     ))  if id in idin]
        self.outerPressure  = [self.outerPressure[id] for id in range(len(self.outerPressure))  if id in idin]
        self.latitude       = [self.latitude     [id] for id in range(len(self.latitude     ))  if id in idin]
        self.longitude      = [self.longitude    [id] for id in range(len(self.longitude    ))  if id in idin]
        self.radiusMax      = [self.radiusMax    [id] for id in range(len(self.radiusMax    ))  if id in idin]
        self.radiusMin      = [self.radiusMin    [id] for id in range(len(self.radiusMin    ))  if id in idin]
        #self.radiusMaxMC    =[ self.radiusMaxMC [id] for id in range(len( self.radiusMaxMC ))  if id in idin]]
        #self.radiusMinMC    =[ self.radiusMinMC [id] for id in range(len( self.radiusMinMC ))  if id in idin]]
        self.angle          = [self.angle        [id] for id in range(len(self.angle        ))  if id in idin]
        #self.part           =[ self.part        [id] for id in range(len( self.part        ))  if id in idin]]
        #self.area2          =[ self.area2       [id] for id in range(len( self.area2       ))  if id in idin]]
        #self.ids            =[ self.ids         [id] for id in range(len( self.ids         ))  if id in idin]]
        self.depth          = [self.depth        [id] for id in range(len(self.depth        ))  if id in idin]
        if len(self.velocity) == idin[0]:
            idin[0] -= 1
        self.velocity       = [self.velocity[idin[0]]]