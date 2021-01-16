import math
import random
import time
import sys
from tkinter import *
from Vector2 import Vector2
from Viewport import Viewport
from Particle import Particle
from Options import Options
import UniPlayer
import Constants



def Distance(pos1, pos2):
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)



def Gravitation(particle1, particle2, distance):
    return Constants.gravityConstant * particle1.mass * particle2.mass / (distance ** 1) * \
        (particle2.pos - particle1.pos) / distance



def StrongForce(particle1, particle2, distance):
    return - Constants.strongForceConstant * particle1.mass * particle2.mass * \
        math.exp(-distance / Constants.strongForceRadConstant)  * \
	    (particle2.pos - particle1.pos) / (distance ** 2)



def StartUniverse(root, space, viewport, options):
    if (options.record):
        recordFile = open(options.recordFName, "x")
        recordFile.write(str(Constants.nParticles) + '\n')

    particles = []
    for i in range(Constants.nParticles):
        sideLen = int(0.005 * Constants.nParticles ** 1.65)
        pos = Vector2(random.randint(0, sideLen) - sideLen / 2, random.randint(0, sideLen) - sideLen / 2)

        mass = random.choice(list(Constants.massToColor))
        # if (i == 1 or i == 2):
        #     particles.append(Particle(space, pos, Vector2(0, 0), random.randint(1, 3) * 1, particleVisualRad * 3, "yellow"))
        # else:
        particles.append(Particle(space, viewport, pos, Vector2(0, 0), mass, \
            Constants.particleVisualRad, Constants.massToColor[mass]))

        if (options.record):
            recordFile.write(str(mass) + '\n')

    # particles[0].mass = 100
    # particles[0].pos = uniSize / 2
    # particles[0].vel = Vector2(0, 0)
    # particles[1].mass = 10
    # particles[1].pos = Vector2(uniSize.x / 2 - 5000, uniSize.y / 2)
    # particles[1].vel = Vector2(0, 1)

    root.update()

    #prevTime = time.clock()

    closed = False
    def SetClosed():
        nonlocal closed
        closed = True

    root.protocol("WM_DELETE_WINDOW", SetClosed)

    while (not closed):
        for i in range(Constants.nParticles - 1):
            for j in range(i + 1, Constants.nParticles):
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

        for i in range(Constants.nParticles):
            particles[i].UpdateState()
            
            if (options.record):
                recordFile.write(str(int(particles[i].pos.x)) + " " + str(int(particles[i].pos.y)) + '\n')
        
        #while (time.clock() - prevTime < 0.1):
        #    continue

        #prevTime = time.clock()
        
        root.update()

    if (options.record):
        recordFile.close()



def main():
    options = Options()
    options.ParseCMD(sys.argv)

    viewport = Viewport()

    root = Tk()
    space = Canvas(root, width = viewport.windowSize.x, height = viewport.windowSize.y, bg = "black")
    space.pack()

    viewport.AddMouseControl(space)

    if (options.play):
        UniPlayer.PlayUniverse(root, space, viewport, options)
    else:
        StartUniverse(root, space, viewport, options)



main()