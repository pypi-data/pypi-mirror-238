import typing as t

import pandas as pd
from pathlib import Path

p = Path(__file__).with_name('VERSION.rtf')
with p.open('r') as f:
    _version = f.read()
    
from config.config import config
from processing.data_manager import load_model
from processing.validation import validate_inputs

model_file_name = f"{config.app_config.model_save_file}{_version}.pkl"
_titanic_pipe = load_model(file_name=model_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _titanic_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": predictions,
            "version": _version,
            "errors": errors,
        }
        
    return results

'''
# Use if you need to check the function make_prediction
from processing.data_manager import load_dataset
data = load_dataset(file_name=config.app_config.test_data_file)
make_prediction(input_data=data)
'''