import os
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from .User import User
from .Common.Imports import *
from scipy.sparse import csr_matrix

MODELS_PATH = 'Models'

class Recommender:
    def __init__(self, meals: pd.DataFrame, feature_matrix: pd.DataFrame, user: User, path: str):
        self.meals = meals
        self.feature_matrix = feature_matrix
        self.user = user
        self.path = path
    
    # returns rated meals
    def _get_rated_meals(self) -> List[np.ndarray]:
        rated_meals = []
        np_user_interactions = self.user.interactions.to_numpy()
        for recipe_id, rating in np_user_interactions:
            rated_meal = self.feature_matrix.iloc[recipe_id].to_numpy() * rating
            rated_meals.append(rated_meal)
        return rated_meals

    # returns unrated meals and their ids
    def _get_unrated_meals(self) -> Tuple[List[np.ndarray], List[int]]:
        unrated_meals = []
        unrated_meals_ids = []

        for i in range(self.feature_matrix.shape[0]):
            if i not in self.user.interactions['recipe_id'].values: #and i not in one_user_interactions_test['recipe_id'].values:
                unrated_meals.append(self.feature_matrix.iloc[i].to_numpy())
                unrated_meals_ids.append(i)

        unrated_meals = np.array(unrated_meals)
        unrated_meals_ids = np.array(unrated_meals_ids)
        return unrated_meals, unrated_meals_ids
    
    def _construct_user_vector(self, rated_meals: List[np.ndarray]) -> np.ndarray:
        user_matrix = np.array(rated_meals)
        user_vector = user_matrix.sum(axis=0)
        user_vector = user_vector / user_vector.sum()
        return user_vector
    
    def run(self, meals_count: int) -> pd.DataFrame:
        rated_meals = self._get_rated_meals()
        unrated_meals, unrated_meals_ids = self._get_unrated_meals()
        user_vector = self._construct_user_vector(rated_meals)
        
        unrated_user_matrix = csr_matrix(unrated_meals).multiply(csr_matrix(user_vector))
        unrated_meals_vector = unrated_user_matrix.sum(axis=1)

        recommended_meals_lst = np.array(unrated_meals_vector).flatten().tolist()
        recommended_meals_lst = [meal for meal in zip(recommended_meals_lst, unrated_meals_ids)]
        recommended_meals_lst = sorted(recommended_meals_lst, key=lambda x: x[0], reverse=True)

        top_meals_ids = [meal[1] for meal in recommended_meals_lst[:meals_count]]
        return self.meals.iloc[top_meals_ids]
    

    def get_rated_meals_2(self) -> pd.DataFrame:
        rated_meals = self.feature_matrix.iloc[self.user.interactions['recipe_id']]
        # convert index to recipe_id in another column
        rated_meals['recipe_id'] = self.feature_matrix.iloc[self.user.interactions['recipe_id']].index
        rated_meals = rated_meals.reset_index(drop=True)
        # add rating column
        rated_meals['rating'] = self.user.interactions['rating']
        return rated_meals

    def get_unrated_meals_2(self) -> Tuple[pd.DataFrame, List[int]]:
        unrated_meals = self.feature_matrix.iloc[~self.feature_matrix.index.isin(self.user.interactions['recipe_id'])]
        unrated_meals_ids = unrated_meals.index
        return unrated_meals, unrated_meals_ids


    def train(self, rated_meals: pd.DataFrame):
        # split rated meals into train and test
        train, validation = train_test_split(rated_meals, train_size=0.7, test_size=0.3, random_state=42)
        # extract x_train, y_train, x_validation, y_validation by dropping recipe_id and rating columns
        x_train = train.drop(['recipe_id', 'rating'], axis=1)
        y_train = train['rating']
        x_validation = validation.drop(['recipe_id', 'rating'], axis=1)
        y_validation = validation['rating']

        # train linear regression model
        model = GradientBoostingRegressor(
            n_estimators = 4780, 
            learning_rate = 0.01,
            max_depth = 10, 
            max_features = 'sqrt',
            min_samples_leaf = 1, 
            min_samples_split = 250, 
            loss = 'squared_error', 
            random_state = 6
        )
        model.fit(x_train, y_train)

        y_pred = model.predict(x_validation)

        rmse = mean_squared_error(y_validation, y_pred, squared=False)
        r2 = r2_score(y_validation, y_pred)
        explained_variance = explained_variance_score(y_validation, y_pred)

        # misclassified examples after rounding the predictions
        misclassified = (y_validation.to_numpy().astype(np.float64) != np.round(y_pred)).sum()
        accuracy = 1 - (misclassified / len(y_validation))

        print('RMSE: ', rmse)
        print('R2: ', r2)
        print('Explained Variance: ', explained_variance)
        print('Misclassified: ', misclassified)
        print('Accuracy: ', accuracy)

        # save model as pickle file
        pickle.dump(model, open(os.path.join(self.path, f'{MODELS_PATH}/{self.user.uid}_content_based_model.pkl'), 'wb'))
        
    def recommend(self, unrated_meals: pd.DataFrame, unrated_meals_ids: List[int], meals_count: int) -> pd.DataFrame:
        model = pickle.load(open(os.path.join(self.path, f'{MODELS_PATH}/{self.user.uid}_content_based_model.pkl'), 'rb'))
        x_test = unrated_meals
        y_pred_test = model.predict(x_test)
        
        # convert y_pred to be a tuple of y_pred and of recipe_id
        unrated_lst = list(zip(y_pred_test, unrated_meals_ids))
        unrated_lst.sort(key=lambda x: x[0], reverse=True)
        top_K_recommendations = self.meals.iloc[[x[1] for x in unrated_lst[:meals_count]]]
        top_K_recommendations = top_K_recommendations.drop('id', axis=1)
        return top_K_recommendations
