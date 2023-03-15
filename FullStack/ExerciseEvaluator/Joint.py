from typing import Any
class Joint:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.visibility = 0.0
    
    def __str__(self):
        return f'x: {self.x}\ny: {self.y}\nz: {self.z}\nvisibility: {self.visibility}\n'
    
    '''
    data: mediapipe point (normalized to [0.0, 1.0])
    '''
    def parse(self, mp_point: Any):
        self.x = mp_point.x
        self.y = mp_point.y
        self.z = mp_point.z
        self.visibility = mp_point.visibility