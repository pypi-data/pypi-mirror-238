from sklearn.model_selection import train_test_split

from config.config import config
from pipeline import survival_pipe
from processing.data_manager import load_dataset
from processing.data_manager import save_model

def run_training() -> None:

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    # fit model
    survival_pipe.fit(X_train, y_train)

    # save trained model, overwrite the previous model
    save_model(model_to_keep=survival_pipe)


if __name__ == "__main__":
    run_training()