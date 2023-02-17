from abc import ABC, abstractmethod
from typing import Dict, List
from BodySequence import BodySequence
from Imports import *

class Exercise(ABC):
    def __init__(self, body_sequence: BodySequence):
        self.body_sequence: BodySequence = body_sequence
        self.features: np.array = np.array([])


    '''
    returns:
        np.array: which contains rows of features. 
                    each row represents a frame, and each column represents a feature.
        It fills the "features" attribute.
    '''
    @abstractmethod
    def extract_features(self) -> np.array:
        pass

    @abstractmethod
    def evaluate(self):
        pass