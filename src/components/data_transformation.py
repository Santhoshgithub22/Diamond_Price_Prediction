import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl") # It will be a folder and file name

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformConfig() # Once we created this class, we should know about above class details so for that this line

    def get_transformation_object(self):
        try:
            logging.info("Data Transformation Initiated")

            # By using this way also we can able to get the numerical and categorical columns, previous method also we can use for this.
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']

            # The categories are the same way which I am given the rank
            cut_categories = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
            color_categories = ["D", "E", "F", "G", "H", "I", "J"]
            clarity_categories = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

            logging.info("Pipeline Initiated")

            ## Numerical Pipeline

            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaling", StandardScaler())
                ]
            )

            ## Categorical Pipeline

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ordinalencoder", OrdinalEncoder(categories=[cut_categories, color_categories,clarity_categories])),
                    # After ordinal encoding we get a values like 1,2,3,4,5 so we should to do scaling.
                    # If we do one hot encoding, then dont do
                    ("scaler", StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_cols),
                ("cat_pipeline", cat_pipeline, categorical_cols)
            ])

            return preprocessor
        
        except Exception as e:
            logging.info("Error occured in Data Transformation")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Read train and test data started")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info(f'Train Dataframe Head: \n{train_df.head().to_string()}')
            logging.info(f"Test Dataframe Head: \n{test_df.head().to_string()}")

            logging.info("obtaining Preprocessing Object")

            preprocessing_obj = self.get_transformation_object()

            target_column_name = "price"
            drop_columns = ["id", target_column_name]

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            ## Transforming using preprocessor object
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.info("Error occured in the initiate data_transformation")
            raise CustomException(e, sys)