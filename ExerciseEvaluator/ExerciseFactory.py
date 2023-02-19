from Definitions import *
from BicepsCurls import BicepsCurls
from BodySequence import BodySequence

class ExerciseFactory:

    # TODO: add other exercises
    @staticmethod
    def create_exercise(exercise_type: ExerciseType, body_sequence: BodySequence):
        if exercise_type == ExerciseType.BICEPS_CURLS:
            return BicepsCurls(body_sequence)