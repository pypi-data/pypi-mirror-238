import re
from datetime import datetime


def set_model_context_filenames():
    current_date = datetime.now().strftime("%Y%m%d")

    dataset_filename = f"rori_multilabeled_data_{current_date}.csv"
    app_reqs_filename = f"model_context_{current_date}.txt"
    model_filename = f"multi_intent_recognizer_{current_date}.pkl"

    return dataset_filename, app_reqs_filename, model_filename


def find_current_max_version(buckets):
    """Searches through the object storage folders to find the most recent model version and set the next version

    >>> find_current_max_version(['v0/', 'v0/multi_intent_recognizer_20230325.joblib', 'v0/rori_labeled_data_20230325.csv', 'v1/model_context_20230518.txt', 'v1/multi_intent_recognizer_20230518.pkl', 'v1/rori_multilabeled_data_20230518.csv'])
    (1, 2)
    """
    current_version = -1

    for obj in buckets:
        try:
            result = re.search(r"v(\d+)", obj)
            match = int(result.group(1))
        except:
            continue

        if match > current_version:
            current_version = match
    next_version = current_version + 1
    return current_version, next_version


def print_object_storage_upload_success_message(
    next_version, model_file_name, dataset_file_name
):
    print(
        f"""
    Upload to Object Storage Successful!

    Remember to update the .env variables with the most current model in the production and staging servers.

    CURRENT_MODEL_LINK='v{next_version}/{model_file_name}'
    CURRENT_MODEL_FILENAME='{model_file_name}'
    """
    )
    return {
        "model_version": next_version,
        "model": model_file_name,
        "dataset": dataset_file_name,
    }
