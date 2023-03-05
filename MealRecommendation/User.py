from Common.Definitions import *
from typing import List

class User:
    def __init__(
        self,
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
        allergies: List[Allergies],
    ):
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
        self.bmi = None # BMI is calculated based on weight and height

