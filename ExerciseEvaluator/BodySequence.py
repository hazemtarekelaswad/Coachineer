from typing import List
from Body import Body

class BodySequence:
    def __init__(self):
        self.bodies: List[Body] = []
    
    def __str__(self):
        string = ''
        for body in self.bodies:
            string += f'{body}\n=====================================================================\n'
        return string

    def append(self, body: Body):
        self.bodies.append(body)
    
    def clean(self): 
        pass

    def normalize(self):
        pass

    def get_torso(self):
        pass

    