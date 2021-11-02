# A basic demo of three.py, a new 3d renderer for Python

import three
from three import primitives

renderer = three.Renderer("Three.py Demo", tickrate=75) # Create a new three.Renderer object with the window name "Three.py Demo" with a tickrate of 75 (75 fps)

renderer.createPrimitive("cube", primitives.Cube) # Create a new three.Cube called "cube"

controls = three.DefaultControls(renderer.getPhysicalByName("cube")) # Attach default rotation controls to the object "cube"

renderer.render(controls.tick)