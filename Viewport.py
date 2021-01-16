from Vector2 import Vector2



class Viewport:
    pos = Vector2(0, 0)
    size = Vector2(12800, 7200)
    windowSize = Vector2(1280, 720)


    def __init__(self, windowSize=Vector2(1280, 720), initSize=Vector2(12800, 7200), initPos=Vector2(0, 0)):
        self.pos = initPos
        self.size = initSize
        self.windowSize = windowSize


    def AddMouseControl(self, canvas):
        canvas.bind_all("<MouseWheel>", self.MouseScrollCallback)
        canvas.bind_all("<B1-Motion>", self.MouseDragCallback)
        canvas.bind_all("<ButtonRelease-1>", self.MouseReleaseCallback)


    prevMousePos = None
    def MouseDragCallback(self, event):
        if (self.prevMousePos != None):
            self.pos.x -= (event.x - self.prevMousePos.x) / self.windowSize.x * self.size.x
            self.pos.y -= (event.y - self.prevMousePos.y) / self.windowSize.y * self.size.y

        self.prevMousePos = Vector2(event.x, event.y)
    

    def MouseReleaseCallback(self, event):
        self.prevMousePos = None


    def MouseScrollCallback(self, event):
        viewportDelta = 1.8 ** (-event.delta / 120)
        
        self.size *= viewportDelta

        print(int(self.size.x / self.windowSize.x))
    

    def Pos(self):
        return self.pos


    def Size(self):
        return self.size
    

    def WindowSize(self):
        return self.windowSize