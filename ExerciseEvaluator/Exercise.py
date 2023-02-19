from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from BodySequence import BodySequence
from Imports import *

class Exercise(ABC):
    def __init__(self, body_sequence: BodySequence):
        self.body_sequence: BodySequence = body_sequence
        self.features: np.ndarray = np.array([])
        self.reps: List[Tuple[int, int]] = []

    '''
    fills "reps" with tuples, each tuple contains a range of
    start_index(frame) and end_index(frame) of each rep
    '''
    @abstractmethod
    def _fill_reps(self):
        pass

    '''
    returns:
        np.array: which contains rows of features. 
                    each row represents a frame, and each column represents a feature.
        It fills the "features" attribute.
    '''
    @abstractmethod
    def extract_features(self) -> np.ndarray:
        pass

    @abstractmethod
    def evaluate(self) -> pd.DataFrame:
        pass
