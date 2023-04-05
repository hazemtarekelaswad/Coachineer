from Common.Imports import *
from Common.Definitions import *
from Health import Health
from DatasetHandler import DatasetHandler
from Recommender import Recommender
from User import User
from Preprocessor import Preprocessor
from Filter import Filter
# * Meal is a pandas Series, not a class
# * all meals are in a dataframe produced from the dataset


def main():
    datasets = {
        Dataset.INGREDIENTS: pd.read_pickle('FoodDataset/ingr_map.pkl'),
        Dataset.INTERACTIONS: pd.read_csv('FoodDataset/interactions_train.csv'),
        Dataset.MEALS: pd.read_csv('FoodDataset/PP_recipes.csv'),
        Dataset.RAW_INTERACTIONS: pd.read_csv('FoodDataset/RAW_interactions.csv'),
        Dataset.RAW_MEALS: pd.read_csv('FoodDataset/RAW_recipes.csv'),
        Dataset.USERS: pd.read_csv('FoodDataset/PP_users.csv')
    }

    preprocessor = Preprocessor(datasets)
    unique_ingredients = preprocessor.get_unique_ingredients()
    # returns
    #   Dataset.MEALS,
    #   Dataset.INTERACTIONS
    pp_datasets, _ = preprocessor.run(feat_mat=False)

    dataset_handler = DatasetHandler(pp_datasets)

    dummy_user = User(
        uid = 0,
        first_name='John',
        last_name='Doe',
        email='john@gmai.com',
        password='password',
        gender=Gender.MALE,
        age=20,
        weight=170,
        height=70,
        goal=Goal.BUILD_MUSCLE,
        activity_level=ActivityLevel.SEDENTARY,
        diet_type=DietType.KETO,
        allergies=[Allergy.GLUTEN]
    )

    # filtered_dataset = Filter(dataset_handler, dummy_user).run()


if __name__ == "__main__":
    main()
