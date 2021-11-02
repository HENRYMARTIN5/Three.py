# Heya! This is the core code for the three.py renderer and it contains base function and class definitions for pretty much everything.
# Three.py is under the MIT license, which can be found in the root directory of this repo.
"""
Three.py is a brand new 3D renderer written in pure python and pygame. Three.py is NOT a wrapper for OpenGL and it is NOT a wrapper for DirectX. All the calculations are done directly via python code.
"""

import pygame
from numpy import array
from math import cos, sin
from os import system, name
from pygame.math import Vector3



######################
#                    #
#   class section    #
#                    #
######################


# Errors
class ObjTypeError(Exception):
    pass

# Main Renderer class
class Renderer():
    def __init__(self, title, tickrate=40, debug=False):
        clearconsole()
        print("Three.py Version 0.01 Alpha")
        self.debug = debug
        self.tickrate = tickrate
        self.objs = []
        self.ontick = []
        print("Created new scene with name: "+title)
        pygame.init()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        print("Window created.")

    def render(self, keyhandler):
        for obj in self.objs:
            Paint(obj, keyhandler)
        for tickItem in self.ontick:
            tickItem()

    def createPhysical(self, name, vertices, edges, isPrimitive=False):
        if self.debug:
            print(f"Creating new Physical \"{name}\".")
        obj = Physical(name, vertices, edges)
        self.objs.append(obj)
        return obj

    def createPrimitive(self, name, primitiveType):
        primitive = primitiveType()
        if self.debug:
            print(f"Creating new Primitive \"{name}\" of type {primitive.__class__.__name__}.")
        if not primitive.isPrimitive:
            raise ObjTypeError
        obj = Physical(name, primitive.vertices, primitive.edges)
        self.objs.append(obj)
        return obj

    def getPhysicalByName(self, name):
        objReturns = []
        for obj in self.objs:
            if obj.name == name:
                objReturns.append(obj)
        if len(objReturns) > 1:
            return objReturns
        else:
            return objReturns[0]


######################
#                    #
#    math section    #
#                    #
######################



def rotation_matrix(α, β, γ):
    sα, cα = sin(α), cos(α)
    sβ, cβ = sin(β), cos(β)
    sγ, cγ = sin(γ), cos(γ)
    return (
        (cβ*cγ, -cβ*sγ, sβ),
        (cα*sγ + sα*sβ*cγ, cα*cγ - sγ*sα*sβ, -cβ*sα),
        (sγ*sα - cα*sβ*cγ, cα*sγ*sβ + sα*cγ, cα*cβ)
    )


class Physical:
    def __init__(self, name, vertices, edges):
        self.__vertices = array(vertices)
        self.__edges = tuple(edges)
        self.__rotation = Vector3(0, 0, 0)
        self.__position = Vector3(0, 0, 0)
        self.name = name

    def rotate(self, axis, θ):
        if axis.lower() == "x":
            self.__rotation.x += θ
        elif axis.lower() == "y":
            self.__rotation.y += θ
        elif axis.lower() == "z":
            self.__rotation.y += θ
        else:
            raise Exception("Axis does not exist. Options are: X, Y, Z")

    @property
    def lines(self):
        location = self.__vertices.dot(rotation_matrix(*self.__rotation))
        return ((location[v1], location[v2]) for v1, v2 in self.__edges)

    @property
    def position(self):
        return self.__position


######################
#                    #
# rendering section  #
#                    #
######################


BLACK, RED = (0, 0, 0), (255, 128, 128)


class Paint:
    def __init__(self, shape, keys_handler):
        self.__shape = shape
        self.__keys_handler = keys_handler
        self.__size = 450, 450
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(self.__size)
        self.__mainloop()

    def __fit(self, vec):
        return [round(70 * coordinate + frame / 2) for coordinate, frame in zip(vec, self.__size)]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self.__keys_handler(pygame.key.get_pressed())

    def __draw_shape(self, thickness=4):
        for start, end in self.__shape.lines:
            pygame.draw.line(self.__screen, RED, self.__fit(start), self.__fit(end), thickness)

    def __mainloop(self):
        while True:
            self.__handle_events()
            self.__screen.fill(BLACK)
            self.__draw_shape()
            pygame.display.flip()
            self.__clock.tick(75)


######################
#                    #
#    misc section    #
#                    #
######################
def keyCode(name):
    return pygame.key.key_code(name)

class DefaultControls():
    def __init__(self, obj, speed=0.05):
        self.speed=speed
        self.obj = obj
    def tick(self, keys):
        counter_clockwise = self.speed
        clockwise = -counter_clockwise
        params = {
            keyCode("q"): ("X", clockwise),
            keyCode("w"): ("X", counter_clockwise),
            keyCode("a"): ("Y", clockwise),
            keyCode("s"): ("Y", counter_clockwise),
            keyCode("z"): ("Z", clockwise),
            keyCode("x"): ("Z", counter_clockwise),
        }

        for key in params:
            if keys[key]:
                self.obj.rotate(*params[key])

def clearconsole():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
        


if __name__ == "__main__":
    print("sup")