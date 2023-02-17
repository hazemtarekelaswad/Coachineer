from typing import Dict
from Imports import *
from Definitions import *
from Exercise import Exercise

class BicepsCurls(Exercise):
    ################### Private methods ###################
    # Todo: detect perspective using z values
    def _detect_perspective(self) -> Perspective:
        pass

    ################### Public methods ###################
    def extract_features(self) -> np.array:
        shoulder_angles = []
        elbow_angles = []

        perspective = self._detect_perspective()
        if perspective == Perspective.RIGHT:
            shoulder_angles = self.body_sequence.calculate_angles(
                JointType.RIGHT_ELBOW,
                JointType.RIGHT_SHOULDER,
                JointType.RIGHT_HIP
            )
            elbow_angles = self.body_sequence.calculate_angles(
                JointType.RIGHT_SHOULDER, 
                JointType.RIGHT_ELBOW, 
                JointType.RIGHT_WRIST
            )

        elif perspective == Perspective.LEFT:
            shoulder_angles = self.body_sequence.calculate_angles(
                JointType.LEFT_ELBOW,
                JointType.LEFT_SHOULDER,
                JointType.LEFT_HIP
            )
            elbow_angles = self.body_sequence.calculate_angles(
                JointType.LEFT_SHOULDER, 
                JointType.LEFT_ELBOW, 
                JointType.LEFT_WRIST
            )

        # Example of features:
        # [
        #   [shoulder_angle_1, elbow_angle_1],
        #   [shoulder_angle_2, elbow_angle_2],
        #   [shoulder_angle_3, elbow_angle_3],
        # ]
        self.features = np.array([shoulder_angles, elbow_angles]).T
        return self.features

        
    # Todo
    def evaluate(self):
        #  Error handling (if features are empty, so they are not extracted)
        if self.features.size == 0:
            print("Features are empty. Please run extract_features() first.")
            return None
