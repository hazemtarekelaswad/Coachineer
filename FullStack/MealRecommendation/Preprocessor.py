
import os
import pickle
import numpy as np
from .Common.Definitions import *
import pandas as pd
from typing import Dict, Optional, Tuple
from scipy.sparse import csr_matrix


# Preprocessed directory
PROCESSED_DIR = 'Preprocessed'
# Preprocessed files paths
PROCESSED_MEALS_PATH = f'{PROCESSED_DIR}/processed_meals.csv'
PROCESSED_INTERACTIONS_PATH = f'{PROCESSED_DIR}/processed_interactions.csv'
FEATURE_MATRIX_SPARSE_PATH = f'{PROCESSED_DIR}/feature_matrix_sparse.pkl'
FEATURE_MATRIX_COLUMNS_PATH = f'{PROCESSED_DIR}/feature_matrix_columns.pkl'
#############

class Preprocessor:
    
    def __init__(self, dataset: Dict[Dataset, pd.DataFrame], path: str):
        self.datasets = dataset
        self.path = path
    
    def _get_unique_ingredients(self) -> np.ndarray:
        return self.datasets[Dataset.INGREDIENTS]['replaced'].unique()
    
    def _construct_feature_matrix(self, pp_meals: Dataset) -> np.ndarray:
        unique_ingredients = self._get_unique_ingredients()
        feature_matrix = np.zeros((len(pp_meals), len(unique_ingredients)), dtype=np.uint8)
        for index, ingrs in enumerate(pp_meals['replaced_ingredients']):
            for i in range(len(ingrs)):
                feature_matrix[index, unique_ingredients == ingrs[i]] = 1
        return feature_matrix

    def get_one_user_interactions(self, pp_interactions, user_id: int) -> pd.DataFrame:
        return pp_interactions.loc[pp_interactions['user_id'] == user_id].reset_index(drop=True)

    def _read_feature_matrix(self) -> pd.DataFrame:
        feature_matrix = None
        with open(os.path.join(self.path, FEATURE_MATRIX_SPARSE_PATH), 'rb') as f:
            feature_matrix = pickle.load(f)
        
        feature_matrix = pd.DataFrame(feature_matrix.todense(), dtype="uint8")

        with open(os.path.join(self.path, FEATURE_MATRIX_COLUMNS_PATH), 'rb') as f:
            feature_matrix_columns = pickle.load(f)

        feature_matrix.columns = feature_matrix_columns
        return feature_matrix

    def _write_feature_matrix(self, feature_matrix: pd.DataFrame):
        new_feature_matrix = csr_matrix(feature_matrix.values)
        with open(os.path.join(self.path, FEATURE_MATRIX_SPARSE_PATH), 'wb') as f:
            pickle.dump(new_feature_matrix, f)

        with open(os.path.join(self.path, FEATURE_MATRIX_COLUMNS_PATH), 'wb') as f:
            pickle.dump(feature_matrix.columns, f)

    def preprocess_interactions(self, pp_meals, read_files: bool = True) -> pd.DataFrame:

        if read_files and not os.path.exists(os.path.join(self.path, PROCESSED_INTERACTIONS_PATH)):
            read_files = False

        if read_files:
            pp_interactions = pd.read_csv(os.path.join(self.path, PROCESSED_INTERACTIONS_PATH))
            return pp_interactions

        ### preprocess interactions
        pp_interactions = self.datasets[Dataset.INTERACTIONS][['u', 'recipe_id', 'rating']]
        pp_interactions['rating'] = pd.to_numeric(pp_interactions['rating'], downcast='integer')
        pp_interactions = pp_interactions.rename(columns={'u': 'user_id'})

        pp_interactions['recipe_id'] = pp_interactions['recipe_id'].apply(lambda x: pp_meals[pp_meals['id'] == x].index[0])
        pp_interactions.to_csv(os.path.join(self.path, PROCESSED_INTERACTIONS_PATH), index=False)
        return pp_interactions

    def preprocess_meals(self, read_files: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # read preprocessed (meals, interactions, feature matrix) files if they exist
        # check for files existence
        
        if read_files and \
            (not os.path.exists(os.path.join(self.path, PROCESSED_MEALS_PATH)) \
             or not os.path.exists(os.path.join(self.path, FEATURE_MATRIX_SPARSE_PATH)) \
            or not os.path.exists(os.path.join(self.path, FEATURE_MATRIX_COLUMNS_PATH))):
            read_files = False
            
        if read_files:
            pp_meals = pd.read_csv(os.path.join(self.path, PROCESSED_MEALS_PATH))
            feature_matrix = self._read_feature_matrix()
            return pp_meals, feature_matrix

            
        ### preprocess meals
        pp_meals = self.datasets[Dataset.MEALS][['id', 'calorie_level', 'ingredient_ids']]
        pp_meals = pp_meals.join(self.datasets[Dataset.RAW_MEALS].set_index('id'), on='id')
        pp_meals = pp_meals.drop(columns=['contributor_id', 'submitted', 'tags', 'n_steps', 'description', 'n_ingredients'])

        ingredient_dict = dict(zip(self.datasets[Dataset.INGREDIENTS]['id'], self.datasets[Dataset.INGREDIENTS]['replaced']))
        pp_meals['ingredient_ids'] = pp_meals['ingredient_ids'].apply(lambda x: [ingredient_dict[ingredient_id] for ingredient_id in eval(x)])

        pp_meals = pp_meals.rename(columns={'ingredient_ids': 'replaced_ingredients'})

        pp_meals.to_csv(os.path.join(self.path, PROCESSED_MEALS_PATH), index=False)

        ### construct feature matrix
        feature_matrix = self._construct_feature_matrix(pp_meals)
        feature_matrix = pd.DataFrame(feature_matrix, columns = self._get_unique_ingredients())
        self._write_feature_matrix(feature_matrix)

        return pp_meals, feature_matrix

