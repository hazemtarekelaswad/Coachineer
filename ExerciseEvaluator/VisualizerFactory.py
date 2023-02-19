from Imports import *
from Definitions import *
from BicepsCurlsVisualizer import BicepsCurlsVisualizer

class VisualizerFactory:

    @staticmethod
    def create_visualizer(exercise_type: ExerciseType, video, evaluation: pd.DataFrame):
        if exercise_type == ExerciseType.BICEPS_CURLS:
            return BicepsCurlsVisualizer(video, evaluation)