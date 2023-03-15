from .PoseEstimator import PoseEstimator
from .VideoReader import VideoReader
from .Exercises.ExerciseFactory import ExerciseFactory
from .Visualizers.VisualizerFactory import VisualizerFactory 

from .Common.Imports import *
from .Common.Definitions import *

class Evaluator:
    def __init__(self, video_path, processed_video_path):
        self.video_path = video_path
        self.processed_video_path = processed_video_path
    
    def evaluate(self):

        # Read the input video
        video_reader = VideoReader(self.video_path)

        # Perform pose estimation
        pose_estimator = PoseEstimator(video_reader.video)
        body_sequence = pose_estimator.estimate_sequence()

        # Create new exercise
        exercise = ExerciseFactory.create_exercise(ExerciseType.BICEPS_CURLS, body_sequence)

        # Extract features from estimated pose sequence
        features = exercise.extract_features()

        # Evaluate this exercise based on the features extracted
        evaluation = exercise.evaluate()
        # evaluation.to_csv('evaluation.csv')

        # Visualizer the evaluation
        video_reader = VideoReader(self.video_path)
        visualizer = VisualizerFactory.create_visualizer(ExerciseType.BICEPS_CURLS, video_reader.video, evaluation)
        visualizer.save(self.processed_video_path)

