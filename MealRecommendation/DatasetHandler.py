from Common.Imports import *
from Common.Definitions import *

#* Meal is a pandas Series, not a class
#* all meals are in a dataframe produced from the dataset

class DatasetHandler:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
    
    # The unique ingredients are considered as the features
    def get_unique_ingredients(self) -> List[str]:
        pass

    # Filters can be used as nested functions
    def filter_on_diet_type(self, diet_type: DietType) -> pd.DataFrame:
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
    
    def filter_on_allergy(self, allergy: Allergy) -> pd.DataFrame:
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