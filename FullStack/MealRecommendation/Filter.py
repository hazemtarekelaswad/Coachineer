from User import User
from DatasetHandler import DatasetHandler
import pandas as pd

class Filter:
    def __init__(self, dataset_handler: DatasetHandler, user: User):
        self.dataset_handler = dataset_handler
        self.user = user
    
    def run(self):
        meals = self.dataset_handler.filter_on_allergy(
                    self.dataset_handler.filter_on_diet_type(
                        self.user.diet_type), 
                        self.user.allergy)
        return meals