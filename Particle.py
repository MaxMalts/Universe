from Vector2 import Vector2



class Particle:
    space = None

    pos = Vector2()
    vel = Vector2()
    mass = 1

    force = Vector2(0, 0)

    visualRad = 10
    visualObj = None
    viewport = None


    def __init__(self, space, viewport, pos = Vector2(0, 0), vel = Vector2(0, 0), mass = 1, visualRad = 10, color = "white"):
        self.space = space
        self.viewport = viewport

        self.pos = pos
        self.vel = vel
        self.mass = mass

        self.visualRad = visualRad

        windowPos = Vector2((self.pos.x - viewport.Pos().x) * viewport.WindowSize().x / \
            viewport.Size().x + viewport.WindowSize().x / 2, \
            (self.pos.y - viewport.Pos().y) * viewport.WindowSize().y / \
            viewport.Size().y + viewport.WindowSize().y / 2)
        
        self.visualObj = space.create_oval(windowPos.x - self.visualRad / 2, windowPos.y - self.visualRad / 2, \
            windowPos.x + self.visualRad / 2, windowPos.y + self.visualRad / 2, outline = "", fill = color)

    
    def AddForce(self, force):
        self.force += force
    

    def UpdateState(self):
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
        
        self.Redraw()
        
        self.force = Vector2(0, 0)
    
    
    def SetPos(self, newPos):
        self.pos = newPos
    
    
    def Redraw(self):
        windowPos = Vector2((self.pos.x - self.viewport.Pos().x) * self.viewport.WindowSize().x / \
            self.viewport.Size().x + self.viewport.WindowSize().x / 2, \
            (self.pos.y - self.viewport.Pos().y) * self.viewport.WindowSize().y / \
            self.viewport.Size().y + self.viewport.WindowSize().y / 2)
        
        self.space.coords(self.visualObj, \
            windowPos.x - self.visualRad / 2, windowPos.y - self.visualRad / 2, \
            windowPos.x + self.visualRad / 2, windowPos.y + self.visualRad / 2)