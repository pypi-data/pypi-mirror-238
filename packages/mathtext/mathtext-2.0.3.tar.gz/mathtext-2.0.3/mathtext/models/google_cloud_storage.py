from mathtext.constants import (
    OBJECT_STORAGE_CLIENT,
    DATA_DIR,
    OBJECT_STORAGE_NAME,
)
from mathtext.models.object_storage_utils import (
    find_current_max_version,
    print_object_storage_upload_success_message,
    set_model_context_filenames,
)


def get_list_of_blob_names(bucket):
    blobs = bucket.list_blobs()
    blob_names = []
    for blob in blobs:
        print(blob.name)
        blob_names.append(blob.name)
    return blob_names


def upload_to_google_cloud(csv_file, model_requirements_path, model_path):
    dataset_filename, app_reqs_filename, model_filename = set_model_context_filenames()
    bucket = OBJECT_STORAGE_CLIENT.bucket(OBJECT_STORAGE_NAME)
    blob_names = get_list_of_blob_names(bucket)

    current_version, next_version = find_current_max_version(blob_names)

    blob = bucket.blob(f"v{next_version}/{model_filename}")
    blob.upload_from_filename(DATA_DIR / model_filename, timeout=1800)

    blob = bucket.blob(f"v{next_version}/{dataset_filename}")
    blob.upload_from_file(csv_file, content_type="text/csv")

    blob = bucket.blob(f"v{next_version}/{app_reqs_filename}")
    blob.upload_from_filename(DATA_DIR / app_reqs_filename)

    print_object_storage_upload_success_message(
        next_version, model_filename, dataset_filename
    )
