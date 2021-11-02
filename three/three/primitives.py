# Three.py Primitive Objects/Classes

class Cube():
    def __init__(self):
        self.isPrimitive = True
        self.vertices=((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1))
        self.edges=({0, 1}, {0, 2}, {2, 3}, {1, 3},
               {4, 5}, {4, 6}, {6, 7}, {5, 7},
               {0, 4}, {1, 5}, {2, 6}, {3, 7})