from User import User
from Common.Imports import *

class Recommender:
    def __init__(self, user: User, meals: pd.DataFrame):
        self.user = user
        self.meals = meals
    

    def recommend(self, meals_cout: int):
        pass