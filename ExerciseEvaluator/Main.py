from Preprocessor import Preprocessor
from PoseEstimator import PoseEstimator
from Joint import Joint
from Body import Body
from BodySequence import BodySequence
from VideoReader import VideoReader
from Exercises.ExerciseFactory import ExerciseFactory
from Visualizers.Visualizer import Visualizer
from Visualizers.VisualizerFactory import VisualizerFactory 

from Common.Imports import *
from Common.Definitions import *


def main():
    # TODO: is to be read from a terminal command
    video_path = 'Data/V10.mp4'

    # Read the input video
    video_reader = VideoReader(video_path)

    # Perform pose estimation
    pose_estimator = PoseEstimator(video_reader.video)
    body_sequence = pose_estimator.estimate_sequence()

    # Create new exercise
    exercise = ExerciseFactory.create_exercise(ExerciseType.BICEPS_CURLS, body_sequence)

    # Extract features from estimated pose sequence
    features = exercise.extract_features()

    # Evaluate this exercise based on the features extracted
    evaluation = exercise.evaluate()
    evaluation.to_csv('evaluation.csv')

    # Visualizer the evaluation
    video_reader = VideoReader(video_path)
    visulaizer = VisualizerFactory.create_visualizer(ExerciseType.BICEPS_CURLS, video_reader.video, evaluation)
    visulaizer.visualize()


    # print(f'Reps: {exercise.reps}')

    # file = open('features.log', 'w')
    # file.write(str(np.round(features)))
    # file.close()

    file = open('joints.log', 'w')
    file.write(str(body_sequence))
    file.close()



if __name__ == "__main__":
    main()
