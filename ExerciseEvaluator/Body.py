from typing import List
from Joint import Joint

class Body:
    def __init__(self, frame_number: int):
        self.joints: List[Joint] = []
        self.frame_number = frame_number
    
    def __str__(self):
        string = f'Frame: {self.frame_number}\n\n'
        for joint in self.joints:
            string += f'{joint}\n'
        return string
    
    def fill(self, unparsed_joints):
        for unparsed_joint in unparsed_joints:
            parsed_joint = Joint()
            parsed_joint.parse(unparsed_joint)
            self.joints.append(parsed_joint)
    
    '''
    joint1, joint2, joint3: indecies of the joints involved in the angle (found in Definitions.py)
    returns:
        float: angle in degrees
    '''

    # Todo
    def calculate_angle(self, joint1, joint2, joint3) -> float:
        pass

    def normalize(self):
        pass