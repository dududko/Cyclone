class Cyclone:

    def __init__(self, msl, pos, ids, vor, filename, filetime, globaltime):
        self.msl = []
        self.omsl = []
        self.mc = []
        self.mcPos = []
        self.pos = []
        self.ids = []
        self.vor = []
        self.dom = []
        self.angle = []
        self.rad = []
        self.traj = []
        self.area = []
        self.maximums = []
        self.color = 'h'

        self.lifetime = 0
        self.distance = 0
        self.appendParams(pos, ids, msl, int((vor - 5) / 5) * 5)

        self.sizeX = -1
        self.sizeY = -1
        self.filename = filename
        self.fileTime = filetime
        self.time = [globaltime]
        self.wasChanged = False
        self.isBaltik = False
        self.part = []

    def set_size(self, size_x, size_y):
        self.sizeX = size_x
        self.sizeY = size_y

    def appendPos(self, pos):
        self.pos.append(pos)

    def appendParams(self, pos, ids, msl, vor):
        self.pos.append(pos)
        self.ids.append(ids)
        self.msl.append(msl)
        self.vor.append(vor)
        self.lifetime += 6

    def getLastPosition(self):
        #return self.pos[-1]
        return self.mcPos[-1]

    def setDomain(self, dom):
        self.dom = dom

    def setMaximums(self, maximums):
        self.maximums = maximums

    def setMassCenter(self, mc):
        self.mc = [mc]

    def appendMassCenter(self, mc):
        self.mc.append(mc)

    def appendMassCenterPos(self, mcPos):
        self.mcPos.append(mcPos)

    def setMassCenterPos(self, mcPos):
        self.mcPos = [mcPos]

    def setRadius(self, rad):
        self.rad = [rad]

    def setPart(self, part):
        self.part = [part]

    def setAngle(self, a):
        self.angle = [a]

    def setTraj(self, traj):
        self.traj.append(traj)