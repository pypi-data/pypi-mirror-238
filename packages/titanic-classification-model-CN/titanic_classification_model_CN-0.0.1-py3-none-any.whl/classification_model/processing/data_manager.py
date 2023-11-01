'''
Module responsible from
(i) Reading dataset, with or without pre-pipeline cleaning
(ii) Save/Load trained model (output of the sklearn Pipeline)
'''

#--- START OF DECLERATIVE STATEMENTS ---
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

import sys
sys.path.append("..")

from config.config import DATASET_DIR, TRAINED_MODEL_DIR, config

p = Path(__file__).parent.with_name('VERSION.rtf')
with p.open('r') as f:
    _version = f.read()

#--- END OF DECLERATIVE STATEMENTS ---


'''Load the dataset as raw, without any cleaning'''
def load_dataset_raw(*, file_name: str) -> pd.DataFrame:
    df = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    
    return df


'''Preliminary cleaning of the dataset, such as replacing weird values, etc '''
def pre_pipeline_cleaning(*, df: pd.DataFrame) -> pd.DataFrame:
    return df


'''Load the dataset after pre-pipeline-cleaning''' 
def load_dataset(*, file_name: str) -> pd.DataFrame:
    df = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    clean_df = pre_pipeline_cleaning(df=df)

    return clean_df


def save_model(*, model_to_keep: Pipeline) -> None:
    '''
    Saves the model (output of the pipeline) and removes previous models
    By this way, we will be sure there is only 1 model 
    '''   

    save_file_name = f"{config.app_config.model_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name


    remove_old_model(files_to_keep=[save_file_name])
    
    joblib.dump(model_to_keep, save_path)
    

def load_model(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)

    
def remove_old_model(*, files_to_keep: list[str]) -> None:
    """
    To remove old model/s (output of the pipeline).
    To be sure there is one-to-one mapping between package version
    and model version to be used in other parts
    """
    
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in files_to_keep:
            model_file.unlink()