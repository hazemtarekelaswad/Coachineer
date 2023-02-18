from typing import List
from Body import Body
from Definitions import *

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

    '''
    joint1, joint2, joint3: indecies of the joints involved in the angle (found in Definitions.py)
    returns:
        List[float]: angle in degrees in each frame
    '''
    def calculate_angles(self, joint1: JointType, joint2: JointType, joint3: JointType) -> List[float]:
        return [body.calculate_angle(joint1, joint2, joint3) for body in self.bodies]

    