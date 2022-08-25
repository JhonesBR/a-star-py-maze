class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

        # Used for visualization
        self.highlighted = False 

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        s = ""
        if self.parent:
            s += 'Parent: ' + str(self.parent.position) + '\n'
        s += 'Position: ' + str(self.position) + '\n'
        s += 'g: ' + str(self.g) + '\n'
        s += 'h: ' + str(self.h) + '\n'
        s += 'f: ' + str(self.f)
        return s