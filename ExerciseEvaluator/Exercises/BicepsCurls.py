from typing import Dict, List
from BodySequence import BodySequence
from Common.Imports import *
from Common.Definitions import *
from Exercises.Exercise import Exercise

################### Constants ###################
ERROR_1_ANGLE = 20 # The larger, the more flexible you can rotate shoulder angle
ERROR_2_ANGLE = 70 # The larger, the more flexible the elbow angle is
REPS_THRESHOLD = 4 # The larger, the more flexible detecting reps is

REPS_UPPER_ANGLE = 130
REPS_LOWER_ANGLE = 80


class BicepsCurls(Exercise):
################### Private methods ###################
    
    def _detect_perspective(self) -> Perspective:
        left_count = 0

        # The less the z value is, the more closer this point to the screen
        for body in self.body_sequence.bodies:
            if body.joints[JointType.LEFT_SHOULDER.value].z < body.joints[JointType.RIGHT_SHOULDER.value].z \
            and body.joints[JointType.LEFT_ELBOW.value].z < body.joints[JointType.RIGHT_ELBOW.value].z \
            and body.joints[JointType.LEFT_HIP.value].z < body.joints[JointType.RIGHT_HIP.value].z:
                left_count += 1
        
        right_count = len(self.body_sequence.bodies) - left_count
        # if left_count / len(self.body_sequence.bodies) > 0.5:
        if left_count > right_count:
            print('Left detected')
            return Perspective.LEFT
        print('Right detected')
        return Perspective.RIGHT
    

    # TODO: Modify this function
    #! This function assumes that the athlete starts from releasing the weight (max elbow angle)
    
    # Iterate over elbow angles, if the angle starts decreasing then increasing, 
    # then once decreased again, it will count 1 rep. the point of increasing or decreasing
    # must be with difference greater than a threshold and must be of 2-step look-ahead
    def _fill_reps(self):
        is_increasing = False
        prev_is_increasing = False
        turning_points = 0
        start_index = 0
        end_index = 0
        
        for index in range(len(self.features[:, 1]) - 2):
            if self.features[index + 1, 1] - self.features[index, 1] > REPS_THRESHOLD \
            and self.features[index + 2, 1] - self.features[index, 1] > REPS_THRESHOLD:
                is_increasing = True
            elif self.features[index, 1] - self.features[index + 1, 1] > REPS_THRESHOLD \
            and self.features[index, 1] - self.features[index + 2, 1] > REPS_THRESHOLD:
                is_increasing = False
            
            # Changed?
            if is_increasing != prev_is_increasing: 
                prev_is_increasing = is_increasing
                turning_points += 1
            
            # Count a rep and reset
            if turning_points == 2:
                end_index = index
                self.reps.append((start_index, end_index))
                start_index = index + 1

                turning_points = 0
        
        # If you have already done half a rep or more, 
        # then consider it as a complete rep (forearm is in its way down)
        if turning_points == 1:
            self.reps.append((start_index, len(self.features[:, 1]) - 1))

    
    
    def _fill_reps_2(self):
        is_increasing = False
        prev_is_increasing = False
        turning_points = 0
        start_index = 0
        end_index = 0
        for index in range(len(self.features[:, 1])):
            if self.features[index, 1] < REPS_LOWER_ANGLE:
                is_increasing = True
            elif self.features[index, 1] > REPS_UPPER_ANGLE:
                is_increasing = False
            
            # Changed?
            if is_increasing != prev_is_increasing: 
                prev_is_increasing = is_increasing
                turning_points += 1
            
            # Count a rep and reset
            if turning_points == 2:
                end_index = index
                self.reps.append((start_index, end_index))
                start_index = index + 1

                turning_points = 0

        # If you have already done half a rep or more, 
        # then consider it as a complete rep (forearm is in its way down)
        if turning_points == 1:
            self.reps.append((start_index, len(self.features[:, 1]) - 1))

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

        for start_index, end_index in self.reps:
            minimum_angle = min(self.features[start_index : end_index, 1])
            print(f'min angle: {minimum_angle}')
            elbow_evaluation[start_index : end_index + 1] = minimum_angle > ERROR_2_ANGLE

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

        # Fill reps with its frames
        self._fill_reps_2()
        print(self.reps)
        # Evaluate shoulder joint
        shoulder_evaluation: List[bool] = self._evaluate_error_1()
        
        # Evaluate elbow joint
        elbow_evaluation: List[bool] = self._evaluate_error_2()
        
        # reps column is initially filled with -1 to indicate invalid rep
        reps_col = np.full(self.features.shape[0], -1, dtype=int)
        for index, rep_range in enumerate(self.reps):
            reps_col[rep_range[0] : rep_range[1] + 1] = index

        # Convert to data frame
        evaluation = pd.DataFrame({
            'rep': reps_col,
            'shoulder_angle': self.features[:, 0],
            'elbow_angle': self.features[:, 1],
            'error_1': shoulder_evaluation,
            'error_2': elbow_evaluation
        })

        return evaluation