from typing import List
from Joint import Joint

class Body:
    def __init__(self, frame_number: int):
        self.joints: List[Joint] = []
        self.frame_number = frame_number

    def normalize(self):
        pass