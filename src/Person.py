class Person:
    def __init__(self, pos):
        self.face = None
        self.pos = pos
        self.clothes = []

    def getPos(self):
        return self.pos[0], self.pos[1], self.pos[2], self.pos[3]

    def addClothes(self, clothes_name):
        self.clothes.append(clothes_name)
    
    def isInside(self, clothes_pos):
        if self.pos[0] < clothes_pos[0] and self.pos[1] < clothes_pos[1] and self.pos[2] > clothes_pos[2] and self.pos[3] > clothes_pos[3]:
            return True
        return False

    def findClothes(self, clothes_name):
        for c in self.clothes:
            if c == clothes_name:
                return True
        return False
    