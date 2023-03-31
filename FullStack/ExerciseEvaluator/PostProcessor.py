from .Common.Imports import *
from .Common.Definitions import *
import os
from typing import List
import matplotlib.pyplot as plt
from app.config import Config



################### Constants ###################
SLOPE_THRESHOLD = 0.5
#################################################

class PostProcessor:

    def __init__(self):
        self.metadata = None

    def read_csv_file(self, path) -> pd.DataFrame:
        is_file_empty = os.path.isfile(path) and os.path.getsize(path) <= 0
        if is_file_empty: return None
        return pd.read_csv(path)

    def read_json_file(self, path) -> pd.Series:
        self.metadata = pd.read_json(path, typ='series')
        return self.metadata

    def get_involved_joints(self, exercise: ExerciseType, perspective: Perspective, error: int) -> List[JointType]:
        return involved_joints[exercise][f'error_{error}'][perspective]

    def get_all_involved_joints(self, exercise: ExerciseType, perspective: Perspective) -> List[List[JointType]]:
        errors_count = len(involved_joints[exercise])
        return [self.get_involved_joints(exercise, perspective, i + 1) for i in range(errors_count)]
    
    def get_all_involved_joints_flattened(self, exercise: ExerciseType, perspective: Perspective) -> List[JointType]:
        return [joint for joints in self.get_all_involved_joints(exercise, perspective) for joint in joints]

    def merge(self, stored_evaluation: pd.DataFrame, converted_evaluation: pd.DataFrame) -> pd.DataFrame:
        if stored_evaluation is None:
            return converted_evaluation
        converted_evaluation['rep'] += stored_evaluation['rep'].iloc[-1] + 1
        return pd.concat([stored_evaluation, converted_evaluation], ignore_index=True)

    def convert_structure(self, evaluation) -> pd.DataFrame:
        # data frame with columns of joint names
        converted_evaluation = pd.DataFrame(
            columns=['rep'] + [joint.name.lower() for joint in JointType])

        # add the rep column
        converted_evaluation['rep'] = evaluation['rep']

        # fill the rest of the columns with 0
        converted_evaluation.replace(np.nan, 0, inplace=True)

        # Reformat the data
        exercise = ExerciseType[self.metadata['exercise']]
        perspective = Perspective[self.metadata['perspective']]

        # Get the involved joints
        all_joints = self.get_all_involved_joints(exercise, perspective)

        # fill the columns with the data of errors
        for i in range(len(all_joints)):
            for joint in all_joints[i]:
                converted_evaluation[joint.name.lower()] = evaluation[f'error_{i + 1}']

        return converted_evaluation
    
    def analyze(self, converted_evaluation: pd.DataFrame) -> List[dict]:

        all_involved_joints = self.get_all_involved_joints_flattened(
            ExerciseType[self.metadata['exercise']], 
            Perspective[self.metadata['perspective']]
        )

        joint_info_list = []
        for joint in all_involved_joints:
            joint_info = {}
            
            name = joint.name.lower()
            x_axis = converted_evaluation['rep']
            y_axis = converted_evaluation[name].cumsum()
            weights = np.polyfit(x_axis, y_axis, 1)
            line = np.poly1d(weights)
            slope = weights[0]

            joint_info['name'] = name
            joint_info['x_axis'] = x_axis
            joint_info['y_axis'] = y_axis
            joint_info['weights'] = weights
            joint_info['line'] = line
            joint_info['slope'] = slope

            joint_info_list.append(joint_info)

        return joint_info_list

        # return [{
        #     'name': joint.name.lower(),
        #     'x_axis': converted_evaluation['rep'],
        #     'y_axis': converted_evaluation[joint.name.lower()].cumsum(),
        #     'weights': np.polyfit(converted_evaluation['rep'], converted_evaluation[joint.name.lower()].cumsum(), 1),
        #     'line': np.poly1d(np.polyfit(converted_evaluation['rep'], converted_evaluation[joint.name.lower()].cumsum(), 1)),
        #     'slope': np.polyfit(converted_evaluation['rep'], converted_evaluation[joint.name.lower()].cumsum(), 1)[0]
        # } for joint in all_involved_joints]

    def visualize(self, analyzed_data: List[dict]):
        plt.figure(figsize=(10, len(analyzed_data) * 5))
        for index, joint in enumerate(analyzed_data):
            print(f'weights: \n{joint["weights"]}')
            print(f'line equation: {joint["line"]}')
            print(f'slope: \n{joint["slope"]}')

            if joint['slope'] > SLOPE_THRESHOLD:
                print(f'🚫 Bad form, there is a potintial injury in {joint["name"]}')
            else:
                print(f'✅ Good form, no injury in {joint["name"]}')
            print('------------------------------------')

            plt.subplot(len(analyzed_data), 1, index + 1)  # rows, columns, index
            plt.plot(joint['x_axis'], joint['y_axis'], 'o')
            plt.plot(joint['x_axis'], joint['line'](joint['x_axis']), "r--")

            plt.title(joint['name'])
            plt.xlabel('Reps')
            plt.ylabel('Cumulative mistakes')
        plt.show()
    
    

    #? The only method you need to call
    @staticmethod
    def run(directory_path: str):
        post_processor = PostProcessor()

        #! For Debugging only
        # evaluation_path = './Static/evaluation.csv'
        # metadata_path = './Static/metadata.json'
        # evaluation_db_path = './Static/evaluation_db.csv'

        evaluation_path = os.path.join(directory_path, 'evaluation.csv')
        metadata_path = os.path.join(directory_path, 'metadata.json')
        evaluation_db_path = os.path.join(directory_path, 'evaluation_db.csv')


        evaluation = post_processor.read_csv_file(evaluation_path)
        metadata = post_processor.read_json_file(metadata_path)
        converted_evaluation = post_processor.convert_structure(evaluation)

        # TODO: Get stored evaluation from database not a file
        stored_evaluation = post_processor.read_csv_file(evaluation_db_path)

        # Merge stored evaluation with converted_evaluation
        merged_evaluation = post_processor.merge(stored_evaluation, converted_evaluation)

        # TODO: Save converted_evaluation to database not a file
        merged_evaluation.to_csv(evaluation_db_path, index=False)

        analyzed_data = post_processor.analyze(merged_evaluation)
        post_processor.visualize(analyzed_data)