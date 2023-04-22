from .Common.Imports import *
from .Common.Definitions import *
import os
from typing import Any, List, Optional, Dict
import matplotlib.pyplot as plt
from app.config import Config



################### Constants ###################
SLOPE_THRESHOLD = 0.5
#################################################

class PostProcessor:

    # initialize the metadata object that contain information about the exercise
    def __init__(self):
        self.metadata = None

    # read the csv file and 
    #   return:  - a data frame
    #            - None if the file is empty 
    def read_csv_file(self, path) -> Optional[pd.DataFrame]:
        is_file_empty = os.path.isfile(path) and os.path.getsize(path) <= 0
        if is_file_empty: return None
        return pd.read_csv(path)
    
    # read the json file and set the metadata object
    def read_json_file(self, path) -> pd.Series:
        self.metadata = pd.read_json(path, typ='series')
        return self.metadata

    # get the affected joints based on the exerciese, perspective, and the error type
    # return: a list of the affected joints
    def get_involved_joints(self, exercise: ExerciseType, perspective: Perspective, error: int) -> List[JointType]:
        return involved_joints[exercise][f'error_{error}'][perspective]

    # get all the affected joints across all error types based on the exercise and perspective
    # return: a list where each row represents the error type and the columns represent the affected joints for each error type
    def get_all_involved_joints(self, exercise: ExerciseType, perspective: Perspective) -> List[List[JointType]]:
        errors_count = len(involved_joints[exercise])
        return [self.get_involved_joints(exercise, perspective, i + 1) for i in range(errors_count)]
    
    # flatten the joints across all error types
    # return: a list of all the affected joints
    def get_all_involved_joints_flattened(self, exercise: ExerciseType, perspective: Perspective) -> List[JointType]:
        return [joint for joints in self.get_all_involved_joints(exercise, perspective) for joint in joints]

    # merge the stored evaluation in the evaluation.db with the converted evaluation (current evaluation) by appending them together
    def merge(self, stored_evaluation: pd.DataFrame, converted_evaluation: pd.DataFrame) -> pd.DataFrame:
        if stored_evaluation is None:
            return converted_evaluation
        converted_evaluation['rep'] += stored_evaluation['rep'].iloc[-1] + 1
        return pd.concat([stored_evaluation, converted_evaluation], ignore_index=True)

    # Convert structure of evaluation.csv comes from Evaluator to another structure where
    # each row represents a rep and each column represents a joint type
    def convert_structure(self, evaluation) -> pd.DataFrame:
        # data frame with columns of joint names
        converted_evaluation = pd.DataFrame(
            columns=['rep'] + [joint.name.lower() for joint in JointType])

        # add the rep column
        converted_evaluation['rep'] = evaluation['rep']

        # fill the rest of the columns with -1
        converted_evaluation.replace(np.nan, -1, inplace=True)

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
    
    # get cumulative sum of all reps on all joints in evaluation_db with ignoring -1 values
    # return: a list of objects where each object represents a joint analysis

    # this object contains:
    #   - name: the name of the joint
    #   - x_axis: the x axis (reps)
    #   - y_axis: the y axis (cumulative sum ignoring -1)
    #   - weights: the weights of the line
    #   - line: the line equation
    #   - slope: the slope of the line
    #   - reps: the number of reps
    #   - available: a boolean value that indicates if the joint has data or not
    def analyze(self, converted_evaluation: pd.DataFrame) -> List[Dict[str, Any]]:

        # all_involved_joints = self.get_all_involved_joints_flattened(
        #     ExerciseType[self.metadata['exercise']], 
        #     Perspective[self.metadata['perspective']]
        # )

        all_joints = [jointType for jointType in JointType]

        joint_info_list = []
        for joint in all_joints:
            joint_info = {}

            name = joint.name.lower()
            converted_evaluation_dropped = converted_evaluation[converted_evaluation[name] != -1]
            y_axis = converted_evaluation_dropped[name].cumsum()
            x_axis = pd.Series(list(range(y_axis.shape[0])))

            if y_axis.empty:
                weights = 'No weights available'
                line = 'No line available'
                slope = 0
            else:
                weights = np.polyfit(x_axis, y_axis, 1)
                line = np.poly1d(weights)
                slope = weights[0]

            joint_info['available'] = not y_axis.empty
            joint_info['name'] = name
            joint_info['x_axis'] = x_axis
            joint_info['y_axis'] = y_axis
            joint_info['weights'] = weights
            joint_info['line'] = line
            joint_info['slope'] = slope
            joint_info['reps'] = x_axis.shape[0]

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

    # get the feedback of a joint based on the analysis done in the "analyze()" function
    # based on the slope of the line
    def get_joint_feedback(self, joint_graph: Dict[str, Any]) -> Dict[str, Any]:
        joint_graph['feedback'] = joint_graph['slope'] <= SLOPE_THRESHOLD
        return joint_graph

    # get the feedback of all joints
    def get_all_joints_feedback(self, analyzed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return list(map(self.get_joint_feedback, analyzed_data))

    # Construct plots for each joint and save them in the graphs_path folder
    def visualize(self, analyzed_data: List[Dict], graphs_path: Optional[str]):
        for index, joint in enumerate(analyzed_data):
            plt.figure(figsize=(10, 10))
            print(f'weights: \n{joint["weights"]}')
            print(f'line equation: {joint["line"]}')
            print(f'slope: \n{joint["slope"]}')

            # if self.get_joint_feedback(joint) == False:
            #     print(f'🚫 Bad form, there is a potintial injury in {joint["name"]}')
            # else:
            #     print(f'✅ Good form, no injury in {joint["name"]}')
            print('------------------------------------')

            # plt.subplot(len(analyzed_data), 1, index + 1)  # rows, columns, index

            if joint['available']:
                plt.plot(joint['x_axis'], joint['y_axis'], 'o')
                plt.plot(joint['x_axis'], joint['line'](joint['x_axis']), "r--")

                plt.title(joint['name'])
                plt.xlabel('Reps')
                plt.ylabel('Cumulative mistakes')
            
            else:
                plt.title(joint['name'])
                plt.xlabel('Reps')
                plt.ylabel('Cumulative mistakes')
                plt.text(
                    0.5, 
                    0.5, 
                    'No data available', 
                    horizontalalignment='center', 
                    verticalalignment='center', 
                    transform=plt.gca().transAxes, 
                    fontdict={'fontsize': 20}
                )
        
            if graphs_path:
                plt.savefig(os.path.join(graphs_path, f'{joint["name"]}.png'))
            else:
                plt.show()
    
    
    # Merge evaluation.csv to evaluation_db.csv and analyze evaluation_db.csv)
    #? The only method you need to call for post processing
    @staticmethod
    def run_with_merge(directory_path: str, graphs_path: str) -> List[Dict[str, Any]]:
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
        post_processor.visualize(analyzed_data, graphs_path=graphs_path)
        return post_processor.get_all_joints_feedback(analyzed_data)
    
    # Analyze the evaluation_db.csv file
    #? The only method you need to call for analysis page
    @staticmethod
    def run_without_merge(directory_path: str, graphs_path: str) -> Optional[List[Dict[str, Any]]]:
        post_processor = PostProcessor()
        #! For Debugging only
        # evaluation_db_path = './Static/evaluation_db.csv'

        evaluation_db_path = os.path.join(directory_path, 'evaluation_db.csv')


        # TODO: Get stored evaluation from database not a file
        stored_evaluation = post_processor.read_csv_file(evaluation_db_path)
        if stored_evaluation is None: return None

        # TODO: Save converted_evaluation to database not a file
        stored_evaluation.to_csv(evaluation_db_path, index=False)

        analyzed_data = post_processor.analyze(stored_evaluation)
        post_processor.visualize(analyzed_data, graphs_path=graphs_path)
        return post_processor.get_all_joints_feedback(analyzed_data)