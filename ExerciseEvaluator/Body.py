from typing import List
from Joint import Joint
from Imports import *
from Definitions import *

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
    joint1, joint2, joint3: joint types involved in the angle (found in Definitions.py => JointType enum)
    returns:
        float: angle in degrees
    '''

    def calculate_angle(self, joint1: JointType, joint2: JointType, joint3: JointType) -> float:
        first_joint = self.joints[joint1.value]
        mid_joint = self.joints[joint2.value]
        end_joint = self.joints[joint3.value]

        angle_rad = np.arctan2(end_joint.y - mid_joint.y, end_joint.x - mid_joint.x) \
                - np.arctan2(first_joint.y - mid_joint.y, first_joint.x - mid_joint.x)

        angle_deg = np.abs(angle_rad * 180 / np.pi)

        if angle_deg > 180:
            angle_deg = 360 - angle_deg

        return angle_deg

    def normalize(self):
        pass