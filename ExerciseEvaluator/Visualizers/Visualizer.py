from Common.Imports import *
from abc import ABC, abstractmethod

class Visualizer(ABC):
    def __init__(self, video, evaluation: pd.DataFrame):
        self.video = video
        self.evaluation = evaluation

    @abstractmethod
    def visualize(self):
        pass
        