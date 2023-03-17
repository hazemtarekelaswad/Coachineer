from Common.Definitions import *
from Common.Imports import *
from Health import Health


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
        weight: float, # in kg
        height: float, # in cm
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
        self.weight = weight # in kg
        self.height = height # in cm
        self.goal = goal
        self.activity_level = activity_level

        #!
        self.diet_type = diet_type
        self.allergies = allergies
        
    def get_bmi(self) -> float:
        return Health.calculate_bmi(self.weight, self.height)
    
    def get_daily_calories(self) -> float:
        return Health.calculate_daily_calories(
            bmr = Health.calculate_bmr(self.weight, self.height, self.age, self.gender),
            activity_level = self.activity_level,
            goal = self.goal
        )
    
    def get_body_fat(self) -> Tuple[float, BodyFat]:
        return Health.calculate_body_fat(
            self.age, 
            self.gender, 
            Health.calculate_bmi(self.weight, self.height)
        )
    
    def get_macros(self) -> Tuple[float, float, float]:
        return Health.calculate_macro_calories(self.get_daily_calories())

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
