import os
from .Common.Imports import *
from .Common.Definitions import *
from .Health import Health
from .Recommender import Recommender
from .User import User
from .Preprocessor import Preprocessor
from .Filter import Filter

# * Meal is a pandas Series, not a class
# * all meals are in a dataframe produced from the dataset

# to switch between database and csv file of interactions
DATASET_INTERACTIONS = True
TRAIN = False

class MealRecommenderService:
    def __init__(self):
        self.user = None
        self.pp_meals = None
        self.pp_interactions = None
        self.feature_matrix = None
    
    def fill_user_interactions(self, pp_interactions):
        self.user.interactions = pp_interactions

    def preprocess(self, path: str):
        datasets = {
            Dataset.INGREDIENTS: pd.read_pickle(os.path.join(path, 'FoodDataset/ingr_map.pkl')),
            Dataset.INTERACTIONS: pd.read_csv(os.path.join(path, 'FoodDataset/interactions_train.csv')),
            Dataset.MEALS: pd.read_csv(os.path.join(path, 'FoodDataset/PP_recipes.csv')),
            Dataset.RAW_INTERACTIONS: pd.read_csv(os.path.join(path, 'FoodDataset/RAW_interactions.csv')),
            Dataset.RAW_MEALS: pd.read_csv(os.path.join(path, 'FoodDataset/RAW_recipes.csv')),
            Dataset.USERS: pd.read_csv(os.path.join(path, 'FoodDataset/PP_users.csv'))
        }

        # run preprocessor and get preprocessed datasets and feature matrix
        preprocessor = Preprocessor(datasets, path)
        pp_meals, feature_matrix = preprocessor.preprocess_meals()

        pp_interactions = None
        user_id = None
        if DATASET_INTERACTIONS:
            # this is function is used only for interactions set in the dataset used for training
            pp_interactions = preprocessor.preprocess_interactions(pp_meals)
            # user_id = pp_interactions['user_id'].value_counts().idxmax()
            user_id = self.user.uid
            pp_interactions = preprocessor.get_one_user_interactions(pp_interactions, user_id)[['recipe_id', 'rating']] 
        else: #! from database in the form of 'recipe_id', 'rating' where recipe_id is the meal index in the pp_meals dataframe
            pass

        self.pp_meals = pp_meals
        self.pp_interactions = pp_interactions
        self.feature_matrix = feature_matrix
    
    def init_user(self, user: User):
        self.user = user
    
    def recommend_meals(self, path: str, n: int = 3):
        filtered_meals = Filter(self.pp_meals, self.user).run()

        recommender = Recommender(filtered_meals, self.feature_matrix, self.user, path)
        rated_meals = recommender.get_rated_meals_2()

        if TRAIN:
            recommender.train(rated_meals)

        unrated_meals, unrated_meals_ids = recommender.get_unrated_meals_2()
        recommended_meals = recommender.recommend(unrated_meals, unrated_meals_ids, n)

        print(f'Calories: {self.user.get_daily_calories()}')
        print(f'Carbs: {self.user.get_macros()[0]}')
        print(f'Fat: {self.user.get_macros()[2]}')
        print(f'Protein: {self.user.get_macros()[1]}')
        print(recommended_meals)
        return recommended_meals



# def main():
#     datasets = {
#         Dataset.INGREDIENTS: pd.read_pickle('FoodDataset/ingr_map.pkl'),
#         Dataset.INTERACTIONS: pd.read_csv('FoodDataset/interactions_train.csv'),
#         Dataset.MEALS: pd.read_csv('FoodDataset/PP_recipes.csv'),
#         Dataset.RAW_INTERACTIONS: pd.read_csv('FoodDataset/RAW_interactions.csv'),
#         Dataset.RAW_MEALS: pd.read_csv('FoodDataset/RAW_recipes.csv'),
#         Dataset.USERS: pd.read_csv('FoodDataset/PP_users.csv')
#     }

#     # run preprocessor and get preprocessed datasets and feature matrix
#     preprocessor = Preprocessor(datasets)
#     pp_meals, feature_matrix = preprocessor.preprocess_meals()

#     pp_interactions = None
#     user_id = None
#     if DATASET_INTERACTIONS:
#         # this is function is used only for interactions set in the dataset used for training
#         pp_interactions = preprocessor.preprocess_interactions(pp_meals)
#         user_id = pp_interactions['user_id'].value_counts().idxmax()
#         # user_id = 275
#         pp_interactions = preprocessor.get_one_user_interactions(pp_interactions, user_id)[['recipe_id', 'rating']] 
#     else: #! from database in the form of 'recipe_id', 'rating' where recipe_id is the meal index in the pp_meals dataframe
#         pass

#     dummy_user = User(
#         uid = user_id,
#         first_name='John',
#         last_name='Doe',
#         email='john@gmai.com',
#         password='password',
#         gender=Gender.MALE,
#         age=20,
#         weight=170,
#         height=70,
#         goal=Goal.BUILD_MUSCLE,
#         activity_level=ActivityLevel.SEDENTARY,
#         diet_type=DietType.KETO,
#         allergies=[Allergy.GLUTEN],
#         interactions=pp_interactions
#     )

#     print(f'User BMI: {dummy_user.get_bmi()}')
#     # print(f'User body fat: {dummy_user.get_body_fat()}')
#     print(f'User daily calories: {dummy_user.get_daily_calories()}')
#     print(f'User macros: {dummy_user.get_macros()}')
#     print()

#     # Todo: implement filter
#     filtered_meals = Filter(pp_meals, dummy_user).run()

#     recommender = Recommender(filtered_meals, feature_matrix, dummy_user)
#     rated_meals = recommender.get_rated_meals_2()

#     if TRAIN:
#         recommender.train(rated_meals)

#     unrated_meals, unrated_meals_ids = recommender.get_unrated_meals_2()
#     recommended_meals = recommender.recommend(unrated_meals, unrated_meals_ids, 10)

#     print(recommended_meals)


# if __name__ == "__main__":
#     main()
