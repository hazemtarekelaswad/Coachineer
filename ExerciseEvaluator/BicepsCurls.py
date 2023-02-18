from typing import Dict, List
from BodySequence import BodySequence
from Imports import *
from Definitions import *
from Exercise import Exercise

################### Constants ###################
ERROR_1_ANGLE = 35
ERROR_2_REPS_THRESHOLD = 1
ERROR_2_ANGLE = 70


class BicepsCurls(Exercise):
################### Private methods ###################
    # Todo: detect perspective using z values
    def _detect_perspective(self) -> Perspective:
        return Perspective.RIGHT

    '''
    Error 1: deals with shoulder angle
    '''
    def _evaluate_error_1(self) -> List[bool]:
        shoulder_evaluation: List[bool] = []
        for angle in self.features[:, 0]:
            shoulder_evaluation.append(angle > ERROR_1_ANGLE)

        return shoulder_evaluation

    '''
    Error 2: deals with elbow angle
    '''
    def _evaluate_error_2(self) -> List[bool]:
        # Assume initilally that all reps are wrong
        elbow_evaluation = np.ones(self.features.shape[0], dtype=bool)

        is_increasing = False
        prev_is_increasing = False
        turning_points = 0
        minimum_angle = 360.0
        start_index = 0
        end_index = 0
        for index in range(len(self.features[:, 1]) - 1):
            if self.features[index + 1, 1] - self.features[index, 1] > ERROR_2_REPS_THRESHOLD:
                is_increasing = True
            elif self.features[index, 1] - self.features[index + 1, 1] > ERROR_2_REPS_THRESHOLD:
                is_increasing = False
            
            # Changed?
            if is_increasing != prev_is_increasing: 
                prev_is_increasing = is_increasing
                turning_points += 1
            
                if turning_points == 1:
                    minimum_angle = self.features[index, 1]
            
            if turning_points == 2:
                end_index = index
                self.reps.append((start_index, end_index))
                elbow_evaluation[start_index : end_index] = minimum_angle > ERROR_2_ANGLE
                start_index = index + 1

                turning_points = 0
        
        return elbow_evaluation.tolist()


################### Public methods ###################
    def extract_features(self) -> np.ndarray:
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

        
    def evaluate(self) -> pd.DataFrame:
        #  Error handling (if features are empty, so they are not extracted)
        if self.features.size == 0:
            print("Features are empty. Please run extract_features() first.")
            return None

        # Evaluate shoulder joint
        shoulder_evaluation: List[bool] = self._evaluate_error_1()
        
        # Evaluate elbow joint
        elbow_evaluation: List[bool] = self._evaluate_error_2()
        
        # reps column is initially filled with -1 to indicate invalid rep
        reps_col = np.full(self.features.shape[0], -1, dtype=int)
        for index, rep_range in enumerate(self.reps):
            reps_col[rep_range[0] : rep_range[1]] = index

        # Convert to data frame
        evaluation = pd.DataFrame({
            'rep': reps_col,
            'shoulder_angle': self.features[:, 0],
            'elbow_angle': self.features[:, 1],
            'error_1': shoulder_evaluation,
            'error_2': elbow_evaluation
        })

        return evaluation