from Vector2 import Vector2
from Particle import Particle
from Options import Options
import Constants



def PlayUniverse(root, space, viewport, options):

	playFile = open(options.playFName, "r")

	nParticles = int(playFile.readline())

	particles = []
	for i in range(nParticles):
		mass = int(playFile.readline())
		particles.append(Particle(space, viewport, Vector2(0, 0), Vector2(0, 0), mass, \
			Constants.particleVisualRad, Constants.massToColor[mass]))

	
	closed = False
	def SetClosed():
		nonlocal closed
		closed = True

	root.protocol("WM_DELETE_WINDOW", SetClosed)

	curParticleInd = 0
	curLine = playFile.readline()
	while (len(curLine) > 0 and not closed):
		curPos = Vector2(*[int(i) for i in curLine.split(' ')])
		
		particles[curParticleInd].SetPos(curPos)
		particles[curParticleInd].Redraw()

		curParticleInd += 1
		if (curParticleInd >= nParticles):
			curParticleInd = 0
			root.update()
		
		curLine = playFile.readline()
	
	playFile.close()