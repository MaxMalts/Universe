import math
import random
import time
from tkinter import *


nParticles = 100
particleVisualRad = 3

gravityConstant = 24
strongForceConstant = 20
strongForceRadConstant = 100


class Vector2:
    x = 0
    y = 0


    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    

    def __add__(self, other): 
        return Vector2(self.x + other.x, self.y + other.y)
    

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    

    def __mul__(self, num):
        return Vector2(self.x * num, self.y * num)
    

    def __rmul__(self, num):
        return Vector2(self.x * num, self.y * num)
    

    def __truediv__(self, num):
        return Vector2(self.x / num, self.y / num)
    

    def __rtruediv__(self, num):
        return Vector2(self.x / num, self.y / num)


    def __neg__(self):
        return Vector2(-self.x, -self.y)



class Viewport:
    pos = Vector2(0, 0)
    size = Vector2(12800, 7200)
    windowSize = Vector2(1280, 720)

viewport = Viewport()



def Distance(pos1, pos2):
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)



class Particle:
    space = None

    pos = Vector2()
    vel = Vector2()
    mass = 1

    force = Vector2(0, 0)

    visualRad = 10
    visualObj = None

    def __init__(self, space, pos = Vector2(0, 0), vel = Vector2(0, 0), mass = 1, visualRad = 10, color = "white"):
        self.space = space

        self.pos = pos
        self.vel = vel
        self.mass = mass

        self.visualRad = visualRad

        windowPos = Vector2((self.pos.x - viewport.pos.x) * viewport.windowSize.x / viewport.size.x + viewport.windowSize.x / 2, \
            (self.pos.y - viewport.pos.y) * viewport.windowSize.y / viewport.size.y + viewport.windowSize.y / 2)
        
        self.visualObj = space.create_oval(windowPos.x - self.visualRad / 2, windowPos.y - self.visualRad / 2, \
            windowPos.x + self.visualRad / 2, windowPos.y + self.visualRad / 2, outline = "", fill = color)
    
    
    def AddForce(self, force):
        self.force += force
    

    def UpdateState(self):
        #oldPos = Vector2(oldVisualCoords[0] + self.visualRad / 2, oldVisualCoords[1] + self.visualRad / 2)

        self.vel += self.force / self.mass
        self.pos += self.vel

        # if (self.pos.x < 0):
        #     self.pos.x = uniSize.x
        # elif (self.pos.x > uniSize.x):
        #     self.pos.x = 0

        # if (self.pos.y < 0):
        #     self.pos.y = uniSize.y
        # elif(self.pos.y > uniSize.y):
        #     self.pos.y = 0

        windowPos = Vector2((self.pos.x - viewport.pos.x) * viewport.windowSize.x / viewport.size.x + viewport.windowSize.x / 2, \
            (self.pos.y - viewport.pos.y) * viewport.windowSize.y / viewport.size.y + viewport.windowSize.y / 2)
        
        self.space.coords(self.visualObj, \
            windowPos.x - self.visualRad / 2, windowPos.y - self.visualRad / 2, \
            windowPos.x + self.visualRad / 2, windowPos.y + self.visualRad / 2)
        #self.space.move(self.visualObj, self.pos.x - oldPos.x, self.pos.y - oldPos.y)

        self.force = Vector2(0, 0)



def Gravitation(particle1, particle2, distance):
    return gravityConstant * particle1.mass * particle2.mass / (distance ** 1) * \
        (particle2.pos - particle1.pos) / distance


def StrongForce(particle1, particle2, distance):
    return -strongForceConstant * particle1.mass * particle2.mass * math.exp(-distance / strongForceRadConstant)  * \
	    (particle2.pos - particle1.pos) / (distance ** 2)



prevMousePos = None
def ViewportDrag(event):
    global prevMousePos

    if (prevMousePos != None):
        viewport.pos.x -= (event.x - prevMousePos.x) / viewport.windowSize.x * viewport.size.x
        viewport.pos.y -= (event.y - prevMousePos.y) / viewport.windowSize.y * viewport.size.y

    prevMousePos = Vector2(event.x, event.y)



def MouseRelease(event):
    global prevMousePos

    prevMousePos = None


def ViewportZoom(event):
    global viewport

    viewportDelta = 1.8 ** (-event.delta / 120)
    
    viewport.size *= viewportDelta

    print(int(viewport.size.x / viewport.windowSize.x))



root = Tk()
space = Canvas(root, width = viewport.windowSize.x, height = viewport.windowSize.y, bg = "black")
space.pack()

space.bind_all("<MouseWheel>", ViewportZoom)
space.bind_all("<B1-Motion>", ViewportDrag)
space.bind_all("<ButtonRelease-1>", MouseRelease)



particles = []
for i in range(nParticles):
    sideLen = 54 #int(0.005 * nParticles ** 1.65)
    pos = Vector2(random.randint(0, sideLen) - sideLen / 2, random.randint(0, sideLen) - sideLen / 2)

    massToColor = {1: "white", 20: "yellow", 80: "red"}
    mass = random.choice(list(massToColor))
    # if (i == 1 or i == 2):
    #     particles.append(Particle(space, pos, Vector2(0, 0), random.randint(1, 3) * 1, particleVisualRad * 3, "yellow"))
    # else:
    particles.append(Particle(space, pos, Vector2(0, 0), mass, particleVisualRad, massToColor[mass]))

# particles[0].mass = 100
# particles[0].pos = uniSize / 2
# particles[0].vel = Vector2(0, 0)
# particles[1].mass = 10
# particles[1].pos = Vector2(uniSize.x / 2 - 5000, uniSize.y / 2)
# particles[1].vel = Vector2(0, 1)

root.update()

#prevTime = time.clock()
while (True):
    for i in range(nParticles - 1):
        for j in range(i + 1, nParticles):
            particle1 = particles[i]
            particle2 = particles[j]

            pos1 = particle1.pos
            pos2 = particle2.pos

            firstParticleForce = Vector2(0, 0)

            distance = Distance(pos1, pos2)

            if (0 == distance):
                firstParticleForce = Vector2(particle1.mass * particle2.mass, 0)

            else:
                firstParticleForce += Gravitation(particle1, particle2, distance)
                strongForce = StrongForce(particle1, particle2, distance)
                firstParticleForce += strongForce

            particle1.AddForce(firstParticleForce)
            particle2.AddForce(-firstParticleForce)

    for curParticle in particles:
        curParticle.UpdateState()
    
    #while (time.clock() - prevTime < 0.1):
    #    continue

    #prevTime = time.clock()
    
    root.update()