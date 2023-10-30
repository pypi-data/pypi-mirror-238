"""  This file is run when the model is created in multilabel_intent_recognition.py.  

It automatically uploads as public files the most recent model and dataset to an object storage service (Digital Ocean Spaces).
"""

import boto3
import botocore
import mimetypes
import os
import re
from datetime import datetime

from mathtext.constants import OBJECT_STORAGE_NAME, OBJECT_STORAGE_CLIENT
from mathtext.models.object_storage_utils import (
    find_current_max_version,
    print_object_storage_upload_success_message,
    set_model_context_filenames,
)


def get_object_store_buckets(client, bucket_name):
    """Returns a list of folders in the object storage

    Output
    ['v0/', 'v0/multi_intent_recognizer_20230325.joblib', 'v0/rori_labeled_data_20230325.csv', 'v1/model_context_20230518.txt', 'v1/multi_intent_recognizer_20230518.pkl', 'v1/rori_multilabeled_data_20230518.csv']
    """
    try:
        response = client.list_objects_v2(Bucket=bucket_name)
    except:
        print(f"Bucket '{bucket_name}' does not exist.")

    # Filter through response object for folder names
    objs = [obj["Key"] for obj in response["Contents"]]
    return objs


def upload_file(client, file_path, bucket_name, spaces_path):
    """Uploads a local file to the object storage"""
    client.upload_file(
        file_path, bucket_name, spaces_path, ExtraArgs={"ACL": "public-read"}
    )


def upload_to_digital_ocean(csv_path, model_requirements_path, model_path):
    client = OBJECT_STORAGE_CLIENT
    bucket_name = OBJECT_STORAGE_NAME
    buckets = get_object_store_buckets(client, bucket_name)
    current_version, next_version = find_current_max_version(buckets)

    (
        dataset_file_name,
        model_requirements_name,
        model_file_name,
    ) = set_model_context_filenames()

    # Uploads the CSV - Not a local file
    client.upload_fileobj(
        csv_path,
        bucket_name,
        f"v{next_version}/{dataset_file_name}",
        ExtraArgs={"ACL": "public-read"},
    )

    # Uploads model dev context - Local file
    upload_file(
        client,
        str(model_requirements_path),
        bucket_name,
        f"v{next_version}/{model_requirements_name}",
    )

    # Uploads the model - Local file
    upload_file(
        client, str(model_path), bucket_name, f"v{next_version}/{model_file_name}"
    )

    print_object_storage_upload_success_message(
        next_version, model_file_name, dataset_file_name
    )
