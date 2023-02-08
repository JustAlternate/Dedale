class Button():
    def __init__(self,name,x,y,width,height):
        self.name=name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
