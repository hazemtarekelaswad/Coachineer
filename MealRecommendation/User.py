from Common.Definitions import *
from Common.Imports import *


class User:
    def __init__(
        self,
        uid: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,

        gender: Gender,
        age: int,
        weight: float,
        height: float,
        body_fat: BodyFat,
        goal: Goal,
        activity_level: ActivityLevel,
        diet_type: DietType,
        allergies: List[Allergy],
    ):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.body_fat = body_fat
        self.goal = goal
        self.activity_level = activity_level
        self.diet_type = diet_type
        self.allergies = allergies
        # self.bmi = None # BMI is calculated based on weight and height

    #! can be changed, not sure of it
    def _calculate_bmi(self) -> float:
        self.bmi = self.weight / ((self.height / 100) ** 2)

    def _calculate_calories(self) -> float:
        pass

    def _calculate_protein(self) -> float:
        pass
    
    def _calculate_carbs(self) -> float:
        pass

    def _calculate_fat(self) -> float:
        pass

    ########################################

    #! Should take other parameters to calculate that score
    def _calculate_score(self, meal: pd.Series, rating: int) -> float:
        pass
    
    # Calculate the similarity between the user vecotor and the meal vector
    def calculate_similariy(self, meal: pd.Series) -> float:
        pass
    
    #! Should return an array of ingredients and a number for each
    #! ingredient that represents his preference for it 
    def calculate_user_vector(self) -> np.ndarray:
        pass
