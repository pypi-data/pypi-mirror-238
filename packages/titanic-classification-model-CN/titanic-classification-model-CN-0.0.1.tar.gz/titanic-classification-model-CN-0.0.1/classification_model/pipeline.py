
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.transformation import LogTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from config.config import config
from processing import custom_preprocess as cp


survival_pipe = Pipeline([
    # -- IMPUTATION --
    (
     'missing_imputation', 
     cp.MissingBinaryTransformer(variables=config.model_config.vars_to_check_existance)
     ),
    (
     'missing_indicator',
     AddMissingIndicator(variables=config.model_config.numerical_vars_with_na)
     ),
    (
     'mean_imputation',
     MeanMedianImputer(imputation_method='mean', variables=config.model_config.numerical_vars_with_na)
     ),

    # -- TRANSFORMATION --
    (
     'gender_binarize',
     cp.GenderBinaryTransformer(variables=config.model_config.vars_to_binarize)
     ),
    (
     'fare_nonzero',
     cp.NonZeroTransformer(variables=config.model_config.vars_to_log_transform)
     ),
    (
     'log',
     LogTransformer(variables=config.model_config.vars_to_log_transform)
     ),

    # -- SCALING AND PREDICTION --
    (
     'scaler',
     MinMaxScaler()
     ),
    (
     'Logit',
     LogisticRegression(penalty=config.model_config.penalty,
                        solver=config.model_config.solver,
                        random_state=config.model_config.random_state)
     ),
])


