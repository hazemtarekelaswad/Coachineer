from Preprocessor import Preprocessor
from PoseEstimator import PoseEstimator
from Joint import Joint
from Body import Body
from BodySequence import BodySequence
from VideoReader import VideoReader
from ExerciseFactory import ExerciseFactory

from Imports import *
from Definitions import *


def main():
    video_reader = VideoReader('Data/V3.mp4')

    pose_estimator = PoseEstimator(video_reader.video)
    body_sequence = pose_estimator.estimate_sequence()

    exercise = ExerciseFactory.create_exercise(ExerciseType.BICEPS_CURLS, body_sequence)

    features = exercise.extract_features()
    exercise.evaluate()
    
    # print(body_sequence)
    file = open('shit', 'w')
    file.write(str(body_sequence))
    file.close()



if __name__ == "__main__":
    main()
