
import numpy as np
from Common.Definitions import *
import pandas as pd
from typing import Dict, Optional


class Preprocessor:
    def __init__(self, dataset: Dict[Dataset, pd.DataFrame]):
        self.datasets = dataset
    
    def get_unique_ingredients(self) -> np.ndarray:
        return self.datasets[Dataset.INGREDIENTS]['replaced'].unique()
    
    def _construct_feature_matrix(self, pp_meals: Dataset) -> np.ndarray:
        unique_ingredients = self.get_unique_ingredients()
        feature_matrix = np.zeros((len(pp_meals), len(unique_ingredients)), dtype=np.uint8)
        for index, ingrs in enumerate(pp_meals['replaced_ingredients']):
            for i in range(len(ingrs)):
                feature_matrix[index, unique_ingredients == ingrs[i]] = 1
        return feature_matrix

    def run(self, feat_mat: bool) -> Dict[Dataset, pd.DataFrame]:
        pp_meals = self.datasets[Dataset.MEALS][['id', 'calorie_level', 'ingredient_ids']]
        pp_meals = pp_meals.join(self.datasets[Dataset.RAW_MEALS].set_index('id'), on='id')
        pp_meals = pp_meals.drop(columns=['contributor_id', 'submitted', 'tags', 'n_steps', 'description', 'n_ingredients'])

        ingredient_dict = dict(zip(self.datasets[Dataset.INGREDIENTS]['id'], self.datasets[Dataset.INGREDIENTS]['replaced']))
        pp_meals['ingredient_ids'] = pp_meals['ingredient_ids'].apply(lambda x: [ingredient_dict[ingredient_id] for ingredient_id in eval(x)])

        pp_meals = pp_meals.rename(columns={'ingredient_ids': 'replaced_ingredients'})

        pp_interactions = self.datasets[Dataset.INTERACTIONS][['u', 'recipe_id', 'rating']]
        pp_interactions = pp_interactions.rename(columns={'u': 'user_id'})

        feature_matrix = None
        if feat_mat:
            feature_matrix = self._construct_feature_matrix(pp_meals)

        return {
            Dataset.MEALS: pp_meals,
            Dataset.INTERACTIONS: pp_interactions
        }, feature_matrix

