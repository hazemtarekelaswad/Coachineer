from User import User
import pandas as pd
from Common.Imports import *
from Common.Definitions import *
from typing import Dict


class Filter:
    def __init__(self, dataset: pd.DataFrame, user: User):
        self.dataset = dataset
        self.user = user

    # Filters can be used as nested functions
    def _filter_on_diet_type(self, diet_type: DietType) -> pd.DataFrame:
        if diet_type == DietType.ANYTHING:
            return self.dataset

        if diet_type == DietType.KETO:
            pass
        if diet_type == DietType.VEGETERIAN:
            pass
        if diet_type == DietType.VEGAN:
            pass
        if diet_type == DietType.PALEO:
            pass
        if diet_type == DietType.MEDITERRANEAN:
            pass

        raise ValueError("Invalid diet type")

    def _filter_on_allergy(self, allergy: Allergy) -> pd.DataFrame:
        if allergy == Allergy.GLUTEN:
            pass
        if allergy == Allergy.PEANUTS:
            pass
        if allergy == Allergy.EGGS:
            pass
        if allergy == Allergy.FISH:
            pass
        if allergy == Allergy.SHELLFISH:
            pass
        if allergy == Allergy.TREE_NUTS:
            pass
        if allergy == Allergy.SOY:
            pass
        if allergy == Allergy.DAIRY:
            pass
        raise ValueError("Invalid allergy type")

    def run(self) -> pd.DataFrame:
        return self.dataset
    
        meals = self.filter_on_allergy(
                self.filter_on_diet_type(
                    self.user.diet_type),
                    self.user.allergy)
        return meals
