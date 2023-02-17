from Imports import *

class ExerciseType(Enum):
    BICEPS_CURLS = 0

# Better naming for joints
class JointType(Enum):
    NOSE = mp.solutions.pose.PoseLandmark.NOSE.value
    LEFT_EYE_INNER = mp.solutions.pose.PoseLandmark.LEFT_EYE_INNER.value
    LEFT_EYE = mp.solutions.pose.PoseLandmark.LEFT_EYE.value
    LEFT_EYE_OUTER = mp.solutions.pose.PoseLandmark.LEFT_EYE_OUTER.value
    RIGHT_EYE_INNER = mp.solutions.pose.PoseLandmark.RIGHT_EYE_INNER.value
    RIGHT_EYE = mp.solutions.pose.PoseLandmark.RIGHT_EYE.value
    RIGHT_EYE_OUTER = mp.solutions.pose.PoseLandmark.RIGHT_EYE_OUTER.value
    LEFT_EAR = mp.solutions.pose.PoseLandmark.LEFT_EAR.value
    RIGHT_EAR = mp.solutions.pose.PoseLandmark.RIGHT_EAR.value
    MOUTH_LEFT = mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value
    MOUTH_RIGHT = mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value
    LEFT_SHOULDER = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
    RIGHT_SHOULDER = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
    LEFT_ELBOW = mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value
    RIGHT_ELBOW = mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value
    LEFT_WRIST = mp.solutions.pose.PoseLandmark.LEFT_WRIST.value
    RIGHT_WRIST = mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value
    LEFT_PINKY = mp.solutions.pose.PoseLandmark.LEFT_PINKY.value
    RIGHT_PINKY = mp.solutions.pose.PoseLandmark.RIGHT_PINKY.value
    LEFT_INDEX = mp.solutions.pose.PoseLandmark.LEFT_INDEX.value
    RIGHT_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_INDEX.value
    LEFT_THUMB = mp.solutions.pose.PoseLandmark.LEFT_THUMB.value
    RIGHT_THUMB = mp.solutions.pose.PoseLandmark.RIGHT_THUMB.value
    LEFT_HIP = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
    RIGHT_HIP = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
    LEFT_KNEE = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
    RIGHT_KNEE = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
    LEFT_ANKLE = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value
    RIGHT_ANKLE = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value
    LEFT_HEEL = mp.solutions.pose.PoseLandmark.LEFT_HEEL.value
    RIGHT_HEEL = mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value
    LEFT_FOOT_INDEX = mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX.value
    RIGHT_FOOT_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value

class Perspective(Enum):
    LEFT = 0
    RIGHT = 1