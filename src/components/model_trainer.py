import os
import sys
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from src.utils import evaluate_model
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_training(self, train_df, test_df):
        try:
            logging.info('Starting model training')
            X_train, y_train, X_test, y_test = (
            train_df.iloc[:, :-1],
            train_df.iloc[:, -1],
            test_df.iloc[:, :-1],
            test_df.iloc[:, -1]

            )

            
            models = {
                'XGBoost': XGBClassifier(n_estimators=295,
                                         max_leaves=810,
                                         min_child_weight=6.150041099125579,
                                         learning_rate=0.06894448972317331,
                                         subsample=0.8618758064542394,
                                         colsample_bylevel=1.0,
                                         colsample_bytree=1.0,
                                         reg_alpha=0.020070123048846998,
                                         reg_lambda=0.49934036422839806,
                                         n_jobs=-1),

                'CatBoost': CatBoostClassifier(early_stopping_rounds=20,
                                               learning_rate=0.1,
                                               n_estimators=350)
            }

            model_report = evaluate_model(X_train, y_train, X_test, y_test, models)
            print('\n================================')
            logging.info(f'Model report: {model_report}')

            # Saving CatBoost as the best model as it is faster to train
            best_model = models['CatBoost']
            save_object(file_path=self.model_trainer_config.trained_model_file_path, object=best_model)

        except Exception as e:
            raise CustomException(e, sys)
