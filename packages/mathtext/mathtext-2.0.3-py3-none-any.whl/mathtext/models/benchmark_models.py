""" This file contains functions to benchmark all previous models on the most recent dataset uploaded to the object storage.

This analysis relies on the specific package versions when the model was created.  Running the benchmark with a different environment may result in an error.

This script must be manually run for now
>> ipython
>> from mathtext.benchmark_models import run_benchmark_analysis_on_models
>> run_benchmark_analysis_on_models()
['Model V1 Accuracy: 0.09542168674698795', 'Model V2 Accuracy: 0.09542168674698795']
"""

import joblib

from mathtext.constants import OBJECT_STORAGE_NAME, OBJECT_STORAGE_CLIENT, DATA_DIR

# These imports aren't used but need to be here to support model loading
from mathtext.models.multilabel_intent_recognition import (
    BERTEncoder,
    Pipeline,
    OneVsRestClassifier,
    LogisticRegression,
    SentenceTransformer,
    BaseEstimator,
    TransformerMixin,
)
from mathtext.models.multilabel_intent_recognition import multilabel_to_unilabel


def map_obj_storage_model_files(object_list):
    """Creates a dictionary of tuples with the model data
    Keys are model version

    Each tuple contains a model file and the training dataset

    Output
    {0: ('v0/multi_intent_recognizer_20230325.joblib', 'v0/rori_labeled_data_20230325.csv'), 1: ('v1/multi_intent_recognizer_20230517.pkl', 'v1/rori_multilabeled_data_20230517.csv'), 2: ('v2/multi_intent_recognizer_20230517.pkl', 'v2/rori_multilabeled_data_20230517.csv'), 3: ('v3/multi_intent_recognizer_20230517.pkl', 'v3/rori_multilabeled_data_20230517.csv')}
    """
    objs = [obj["Key"] for obj in object_list["Contents"]]

    obj_dict = {}
    for obj in objs:
        version = int(obj.split("/")[0].replace("v", ""))

        if ".csv" in obj or ".pkl" in obj or ".joblib" in obj:
            if version in obj_dict:
                obj_dict[version] += (obj,)
            else:
                obj_dict[version] = (obj,)
    return obj_dict


def get_benchmark_dataset(client, model_file_dict):
    """Downloads the most recent labeled dataset from the object storage to your local machine and returns the path

    Output
    [your machine path]\mathtext\mathtext\data\rori_multilabeled_data_20230517.csv
    """
    current_csv_version = max(model_file_dict.keys())
    current_csv_filepath = model_file_dict[current_csv_version][1]
    current_csv_file = current_csv_filepath.replace(f"v{current_csv_version}/", "")

    dataset = client.download_file(
        OBJECT_STORAGE_NAME, current_csv_filepath, str(DATA_DIR / current_csv_file)
    )

    benchmark_dataset = DATA_DIR / current_csv_file
    return benchmark_dataset


def score_each_model_on_benchmark_df(client, model_file_dict, benchmark_df):
    """Iterates through the object of model files to return an accuracy score statement for each model against the most recent labeled dataset

    Output
    ['Model V1 Accuracy: 0.09542168674698795', 'Model V2 Accuracy: 0.09542168674698795', 'Model V3 Accuracy: 0.09542168674698795']
    """
    results = []
    for obj in model_file_dict:
        # NOTE: Skips Logistic Regression model for now
        # Because it's a different model and different file type
        if obj == 0:
            continue

        # Gets the current model to evaluate
        # NOTE: Does not use the model_context (requirements.txt) file yet
        current_model_filepath = model_file_dict[obj][0]
        current_model_name = model_file_dict[obj][0].replace(f"v{obj}/", "")

        # Downloads model to data folder
        try:
            local_model = client.download_file(
                OBJECT_STORAGE_NAME,
                current_model_filepath,
                str(DATA_DIR / current_model_name),
            )

            # Run prediction and score
            model = joblib.load(DATA_DIR / current_model_name)
            predicted_labels = model.predict(benchmark_df["Utterance"])
            true_labels = benchmark_df["Label"]
            score = model.score(true_labels, predicted_labels)

            # Append results
            results.append(f"Model V{obj} Accuracy: {score}")
        except:
            pass
    return results


def run_benchmark_analysis_on_models():
    """Calls the functions to score each model against the most recent labeled dataset

    Output
    ['Model V1 Accuracy: 0.09542168674698795', 'Model V2 Accuracy: 0.09542168674698795']
    """
    client = OBJECT_STORAGE_CLIENT

    try:
        response = client.list_objects_v2(Bucket=OBJECT_STORAGE_NAME)
    except:
        print(f"Bucket '{OBJECT_STORAGE_NAME}' does not exist.")
        return False

    model_file_dict = map_obj_storage_model_files(response)
    benchmark_dataset = get_benchmark_dataset(client, model_file_dict)
    benchmark_df = multilabel_to_unilabel(benchmark_dataset)

    results = score_each_model_on_benchmark_df(client, model_file_dict, benchmark_df)

    for result in results:
        print(result)
    print("---------------------")
    return results
