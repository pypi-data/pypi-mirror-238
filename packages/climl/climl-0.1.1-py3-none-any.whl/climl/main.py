import requests
import typer
import os

app = typer.Typer()

@app.command()
def main():
    
    options = ['Y', 'y', 'N', 'n']
    url = "https://worker-lingering-wildflower-b69e.climl.workers.dev/"
    user_input = ""
    user_email = ""

    script_path = os.path.abspath(__file__)
    print("Current script location:", script_path)

    print("\nWelcome to CLIML. CLIML enables you to rapidly automate the creation of powerful supervised learning models.")
    while user_input not in options :
        user_input = typer.prompt("Have you already signed-up to CLIML? (Y/n)")
    if user_input in ['Y', 'y']:
        user_email = typer.prompt("Enter the email associated with your sign-up")
    else :
        typer.launch("https://google.com")
        raise typer.Exit()

    response = requests.post(url, data=user_email)

    if response.text == "False":
        print("Email not found. Contact john@hotmail.com for help.")
        raise typer.Exit()

    activated_code = """
import typer
import pickle
import pandas as pd
from AutoClean import AutoClean
from flaml import AutoML
import logging
from sklearn.preprocessing import LabelEncoder
from rich import print


app = typer.Typer(help="CLIML: Create Powerful ML Models on Autopilot")


@app.command()
def train(file: str = typer.Argument(default=...,help="The CSV file you want to train a model on.",show_default=False), 
         time: int = typer.Argument(default=..., help="How many seconds to spend on training your model.",show_default=False)) :
    '''
    Train a model on numerical input columns and a final output column.
    
    The output column can contain string categories or numerical data.

    CLIML will detect and train a classification or a regression model respectively.
    '''
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    logging.getLogger('flaml.automl.logger').addHandler(NullHandler())

    print(":file_folder: Loading File")
    df = pd.read_csv(file)
    print(":white_check_mark: File Loaded")
    output = df.columns[-1]
    model = AutoML()
    print(":hourglass_flowing_sand: Training Model for ",time," Seconds")
    if df[output].dtype == 'object' :
        le = LabelEncoder()
        df[output] = le.fit_transform(df[output])
        model.fit(df.iloc[:, :-1],
                  df.iloc[:, -1],
                  mlflow_logging=False,
                  task='classification',
                  time_budget = time)
        df[output] = le.inverse_transform(df[output])  
    else :
        model.fit(df.iloc[:, :-1],
                  df.iloc[:, -1],
                  mlflow_logging=False,
                  task='regression',
                  time_budget = time)
    print(":white_check_mark: Model Trained")

    model_name = file.rsplit('.', 1)[0]
    data_to_pickle = {
    'df': df,
    'model': model
    }

    print(":file_cabinet: Saving Model")
    
    with open(model_name+'.climl', "wb") as f:
        pickle.dump(data_to_pickle, f, pickle.HIGHEST_PROTOCOL)
    print(":white_check_mark: Model Saved")

    print(":information_desk_person: Model Information:")
    print(model_name+".climl is a: ", model.best_estimator)
    print("Hyperparameter Configurations: ", model.best_config)
    print("Model Accuracy: ", round((1-model.best_loss), 2))
    print("Best Training Run Discovered by: ", round(model.time_to_find_best_model, 2),"s")


@app.command()
def inspect(file: str = typer.Argument(default=...,help="The model you want to inspect.",show_default=False)) :
    '''
    Display model type, hyperparameters, accuracy, and training speed to the terminal.
    '''    
    print(":file_folder: Loading Model")

    with open(file, 'rb') as f:
        data_to_pickle = pickle.load(f)
    print(":white_check_mark: Model Loaded")

    print(":magnifying_glass_tilted_left: Inspecting Model")

    model = data_to_pickle['model']
    
    print(":information_desk_person: Model Information:")
    print(file," is a: ", model.best_estimator)
    print("Hyperparameter Configurations: ", model.best_config)
    print("Model Accuracy: ", round((1-model.best_loss), 2))
    print("Best Training Run Discovered by: ", round(model.time_to_find_best_model, 2),"s")


@app.command()
def predict(file: str = typer.Argument(default=...,help="The file containing the inputs you want to predict.",show_default=False), 
         model: str = typer.Argument(default=...,help="The model you've trained on these inputs.",show_default=False)) :
    '''
    Display predictions to the command line and insert them as a new column in the CSV file containing your test dataset.

    HINT: Leave the final column in your test data CSV file completely blank (i.e. don't include a dummy header)
    '''    
    print(":file_folder: Loading Test Data")

    df = pd.read_csv(file)

    print(":white_check_mark: Test Data Loaded")

    print(":file_folder: Loading Model")

    with open(model, 'rb') as f:
        data_to_pickle = pickle.load(f)

    print(":white_check_mark: Model Loaded")

    training_df = data_to_pickle['df']
    autoML_model = data_to_pickle['model']
    output = training_df.columns[-1]

    print(":thinking_face: Generating Predictions")
    if training_df[output].dtype == 'object' :
        le = LabelEncoder()
        training_df[output] = le.fit_transform(training_df[output])
        unique_labels = le.classes_
        dictionary = {encoded: original for encoded, original in enumerate(unique_labels)}
        list = autoML_model.predict(df)
        new_list = [dictionary[item] for item in list]

    else :
        new_list = autoML_model.predict(df)

    df['Predicted Output'] = new_list
    df.to_csv(file, index=False)
    print(":white_question_mark: Model Predictions:")
    print(new_list)

if __name__ == "__main__":
    app()  
    """

# Specify the filename for the new script
    activated_file = script_path

# Write the code to the new script file
    with open(activated_file, "w") as file:
        file.write(activated_code)
    print("CLIML activated")

if __name__ == "__main__":
    app() 
