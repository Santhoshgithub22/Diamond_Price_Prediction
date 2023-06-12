import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

## Initialize the data ingestion configuration

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join("artifacts", "train.csv")
    test_data_path:str = os.path.join("artifacts", "test.csv")
    raw_data_path:str = os.path.join("artifacts", "raw.csv")

## Creating a class for data ingestion

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Method Starts")
        try:
            df=pd.read_csv(os.path.join('notebooks/data','gemstone.csv'))
            logging.info("Dataset read as pandas dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Train and Test Split")

            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            ) # Namma pipeline diagram la raw data kuduthutu idha dhan return pannuvom

        except Exception as e:
            logging.info("Exception Occured at Data Ingestion Stage")
            raise CustomException(e,sys)
        
## Run Data Ingestion

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion() # Its returning train data & and test data 
    # so variable name adha kudukurom
    # raw data no need because namma pipeline diagram la first data ingestion block vandhu
    # raw data va input vangitu train data and test data va dha return pannum

