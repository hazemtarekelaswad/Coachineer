from Common.Imports import *
from Common.Definitions import *

# Contains utility functions to calculate nutritional values and health metrics
## NOTE
## weight: in kg
## height: in cm
class Health:
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        return weight / ((height / 100) ** 2)
    
    
    @staticmethod
    def calculate_bmr(weight: float, height: float, age: int, gender: Gender) -> float:
        if gender == Gender.MALE:
            return 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
        if gender == Gender.FEMALE:
            return 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age
        raise ValueError("Invalid gender")

    @staticmethod
    def calculate_daily_calories(bmr: float, activity_level: ActivityLevel, goal: Goal) -> float:
        basic_calories = None
        if activity_level == ActivityLevel.SEDENTARY:
            basic_calories = bmr * 1.2
        elif activity_level == ActivityLevel.LIGHTLY_ACTIVE:
            basic_calories = bmr * 1.375
        elif activity_level == ActivityLevel.MODERATELY_ACTIVE:
            basic_calories = bmr * 1.55
        elif activity_level == ActivityLevel.VERY_ACTIVE:
            basic_calories = bmr * 1.725
        elif activity_level == ActivityLevel.EXTRA_ACTIVE:
            basic_calories = bmr * 1.9
        else:
            raise ValueError("Invalid activity level")
        
        if goal == Goal.LOSE_WEIGHT:
            return basic_calories - 500 # from 500 to 1000
        if goal == Goal.MAINTAIN_WEIGHT:
            return basic_calories
        if goal == Goal.BUILD_MUSCLE:
            return basic_calories + 500 # from 250 to 500
        raise ValueError("Invalid goal")
    
    # Returns body fat percentage and body fat category
    @staticmethod
    def calculate_body_fat(age: int, gender: Gender, bmi: float) -> Tuple[float, BodyFat]:
        body_fat = -44.988 \
                + (0.503 * age) \
                + (10.689 * gender.value) \
                + (3.172 * bmi) \
                - (0.026 * bmi ** 2) \
                + (0.181 * bmi * gender.value) \
                - (0.02 * bmi * age) \
                - (0.005 * (bmi ** 2) * gender.value) \
                + (0.00021 * (bmi ** 2) * age)
        
        if gender == Gender.MALE:
            if body_fat <= 20:
                return body_fat, BodyFat.LOW
            if body_fat <= 25:
                return body_fat, BodyFat.MEDIUM
            return body_fat, BodyFat.HIGH
        
        if gender == Gender.FEMALE:
            if body_fat <= 30:
                return body_fat, BodyFat.LOW
            if body_fat <= 35:
                return body_fat, BodyFat.MEDIUM
            return body_fat, BodyFat.HIGH
        
        raise("Invalid gender")

    # NOTE
    # 50% of the calories from carbs
    # 30% of the calories from protein
    # 20% of the calories from fat

    # parameters: daily calories
    # Returns carbs, protein, fat in calories
    @staticmethod
    def calculate_macro_calories(calories: float) -> Tuple[float, float, float]:
        return calories * 0.5, calories * 0.3, calories * 0.2
    
    # parameters: daily calories
    # Returns carbs, protein, fat in grams
    @staticmethod
    def calculate_macro_grams(calories: float) -> Tuple[float, float, float]:
        return calories * 0.5 / 4, calories * 0.3 / 4, calories * 0.2 / 9