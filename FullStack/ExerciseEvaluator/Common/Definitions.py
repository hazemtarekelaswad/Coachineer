from ..Common.Imports import *



class ExerciseType(Enum):
    BICEPS_CURLS = 0
    SQUATS = 1
    LEG_RAISES = 2
    LATERAL_RAISES = 3

# Better naming for joints
class JointType(Enum):
    LEFT_SHOULDER = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
    RIGHT_SHOULDER = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
    LEFT_ELBOW = mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value
    RIGHT_ELBOW = mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value
    LEFT_WRIST = mp.solutions.pose.PoseLandmark.LEFT_WRIST.value
    RIGHT_WRIST = mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value
    LEFT_HIP = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
    RIGHT_HIP = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
    LEFT_KNEE = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
    RIGHT_KNEE = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
    LEFT_ANKLE = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value
    RIGHT_ANKLE = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value

class Perspective(Enum):
    LEFT = 0
    RIGHT = 1
    FRONT = 2


involved_joints = {
    ExerciseType.BICEPS_CURLS: {
        'error_1': {
            Perspective.LEFT: [
                JointType.LEFT_ELBOW,
                JointType.LEFT_WRIST
            ],
            Perspective.RIGHT: [
                JointType.RIGHT_ELBOW,
                JointType.RIGHT_WRIST
            ]
        },
        'error_2': {
            Perspective.LEFT: [
                JointType.LEFT_SHOULDER
            ],
            Perspective.RIGHT: [
                JointType.RIGHT_SHOULDER
            ]
        },
    }
}
