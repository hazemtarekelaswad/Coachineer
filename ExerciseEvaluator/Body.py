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

    def normalize(self):
        pass