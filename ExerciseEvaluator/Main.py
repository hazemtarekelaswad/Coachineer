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
    video_reader = VideoReader('Data/V1.mp4')

    pose_estimator = PoseEstimator(video_reader.video)
    body_sequence = pose_estimator.estimate_sequence()

    exercise = ExerciseFactory.create_exercise(ExerciseType.BICEPS_CURLS, body_sequence)

    features = exercise.extract_features()
    evaluation = exercise.evaluate()

    evaluation.to_csv('evaluation.csv')
    
    # TODO: read csv file into a data frame and use it to output a visualization of the feedback


    # print(f'Reps: {exercise.reps}')

    # file = open('features.txt', 'w')
    # file.write(str(np.round(features)))
    # file.close()

    # file = open('joints.txt', 'w')
    # file.write(str(body_sequence))
    # file.close()



if __name__ == "__main__":
    main()
