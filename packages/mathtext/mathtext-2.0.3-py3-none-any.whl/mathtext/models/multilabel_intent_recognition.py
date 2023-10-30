#!/usr/bin/env python
# coding: utf-8
"""  Create multilabel intent recognition model from a dataset of labeled messages/utterances.

Datasets are stored in mathtext/data/ as CSVs.
To train a model your application, run the following:

from mathtext.models.multilabel_intent_recognition import run_multilabel_model_development_process
run_multilabel_model_development_process()
"""

import io
import joblib
import numpy as np
import pandas as pd
import re
import requests
import subprocess

from collections import Counter
from datetime import datetime
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline

from mathtext.constants import (
    GOOGLE_SHEET_LINK,
    DATA_DIR,
    OBJECT_STORAGE_PROVIDER,
)
from mathtext.models.digital_ocean_storage import upload_to_digital_ocean
from mathtext.models.google_cloud_storage import upload_to_google_cloud


np.random.seed(42)

# Only used if GOOGLE_SHEET_LINK is unavailable
# Requires this file to be on computer
CSV_PATH_MULTILABEL = DATA_DIR / "rori_multilabeled_data_20230515.csv"

REPLACEMENT_LABELS = {
    "menu": "main_menu",
    "example": "hint",
    "examples": "hint",
    "feedback": "help",
    "preamble": "",
    "math": "math_lesson",
    "riddle___joke": "play",
    "affirmation": "yes",
    "preamble": "greeting",
    "numbers": "int_list",
}

# column_number: oversampling_frequency (0=Utterance, 1=Label_1 (Primary), 2=Label_2 (Secondary)...)
OVERSAMPLING_COUNTS = {1: 3, 2: 2, 3: 1}

CURRENT_DATE = datetime.now().strftime("%Y%m%d")


class BERTEncoder(BaseEstimator, TransformerMixin):
    """Transforms list of texts (strs) into vectors that represent the meaning of the texts"""

    def __init__(self, name="all-MiniLM-L6-v2", **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.encoder = SentenceTransformer(self.name)
        # super().__init__(**kwargs)

    def transform(self, X, copy=None):
        X = list(X)
        return self.encoder.encode(X)

    def fit(self, X, y=None, sample_weight=None):
        return self


def multilabel_to_unilabel(
    df=CSV_PATH_MULTILABEL, oversampling_counts=OVERSAMPLING_COUNTS
):
    if isinstance(df, (str, Path)):
        df = pd.read_csv(df, usecols=[0, 1, 2, 3])
    else:
        df = pd.DataFrame(df)
    df.index.name = "Utterance"
    if list(df.columns[:2]) == ["Utterance", "Label"]:
        return df
    df.columns = "Utterance Label_1 Label_2 Label_3".split()
    unilabels = np.concatenate(
        oversampling_counts[1] * [df[["Utterance", f"Label_1"]].dropna().values]
    )
    for i in range(2, 4):
        unilabels = np.concatenate(
            [unilabels]
            + oversampling_counts[i] * [df[["Utterance", f"Label_{i}"]].dropna().values]
        )
    df = pd.DataFrame(unilabels, columns="Utterance Label".split())
    df["Label"] = df["Label"].str.strip().str.replace(" ", "_").str.lower()
    df["Label"].replace(REPLACEMENT_LABELS, inplace=True)
    return df


def tags_from_labels(df=CSV_PATH_MULTILABEL):
    """Create a matrix of multihot vectors for each utterance so utterances can each have multiple labels (tags)

    >>> tags_from_labels([['BB', 'b'],
    ...                       ['AA BB', 'a'],
    ...                       ['AA BB', 'b'],
    ...                       ['a b c', 'a'],
    ...                       ['a b c', 'b'],
    ...                       ['a b c', 'c']])
           a  b  c
    AA BB  1  1  0
    BB     0  1  0
    a b c  1  1  1
    """
    if isinstance(df, (str, Path)):
        df = pd.read_csv(df)
    else:
        df = pd.DataFrame(df)
    if "Utterance" not in df.columns or "Label" not in df.columns:
        df = df[list(df.columns)[:2]].copy()
        df.columns = ["Utterance", "Label"]
    df.dropna(subset=["Label"], inplace=True)
    df["Label"] = df["Label"].str.lower().str.strip().str.replace(" ", "_")

    def clean_label(s):
        return re.sub(r"[^\w]+", "_", s)

    df["Label"] = df["Label"].apply(clean_label)

    groups = df.groupby("Utterance")  # 2-tuples (utterance, df_group)
    tags = {}
    for (
        utt,
        g,
    ) in groups:  # groupby made the df.index (utterances) the identifier for the group
        tags[utt] = Counter(g["Label"])

    df_tags = (pd.DataFrame(tags).fillna(0).T >= 1).astype(int)
    return df_tags


def predict_tags(pipe, utterances, label_mapping=None):
    if isinstance(utterances, str):
        utterances = [utterances]
    predicted_tags = pipe.predict(utterances)
    if label_mapping is None:
        label_mapping = pipe.label_mapping

    return {
        utt: [label_mapping[i] for i, is_tag in enumerate(pred) if is_tag]
        for (utt, pred) in zip(utterances, predicted_tags)
    }


def train_and_save(
    df, df_tags, filepath=DATA_DIR / "intent_recognizer.pkl", test_size=0.2
):
    utterances = df_tags.index.values
    label_mapping = df_tags.columns.values

    X_str = pd.Series(utterances)
    y = df_tags >= 1  # make sure counts > 1 are clipped

    pipe = build_pipeline(label_mapping)

    dataset = train_test_split(X_str, y, test_size=test_size)
    X_train, y_train = dataset["X_train"], dataset["y_train"]
    print(
        f"unlabeled intents in the training set:\n{find_unlabeled_intents(y=y_train)}"
    )
    print(f"y_train.shape: {y_train.shape}")
    X_test, y_test = dataset["X_test"], dataset["y_test"]
    print(f"unlabeled intents in the test set:\n{find_unlabeled_intents(y=y_test)}")
    print(f"y_test.shape: {y_test.shape}")
    pipe = pipe.fit(X_train, y_train)
    pipe.fit(X_train, y_train)
    train_acc = pipe.score(X_train, y_train)
    if len(X_test) and len(y_test):
        test_acc = pipe.score(X_test, y_test)
    else:
        test_acc = 0.0
    print(f"Train/Test Accuracy: {train_acc:0.3f}/{test_acc:0.3f}")
    joblib.dump(pipe, filepath)
    return dict(filepath=filepath, pipe=pipe, df_tags=df_tags)


def train_test_split(X, y, test_size=0.2):
    is_test = np.random.rand(len(X)) < test_size  # 20% test set sample
    is_train = ~is_test  # if it's not training set it's testset

    X_train = X[is_train].copy()
    X_test = X[is_test].copy()

    y_train = y[is_train].copy()
    y_test = y[is_test].copy()

    return dict(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)


def find_unlabeled_intents(y):
    num_tests = y.sum()
    return num_tests.index.values[num_tests < 1]


def build_pipeline(label_mapping=None):
    pipe = Pipeline(
        [
            ("encoder", BERTEncoder()),
            (
                "tagger",
                OneVsRestClassifier(
                    LogisticRegression(
                        solver="lbfgs", max_iter=10_000, class_weight="balanced"
                    )
                ),
            ),
        ]
    )
    pipe.label_mapping = label_mapping
    return pipe


# INFO: Not in use
def multilabel_f1_score(model, X, y, label_mapping=None, utterances=None):
    if label_mapping is None:
        label_mapping = model.label_mapping
    utterances = utterances or X.index.values
    y_pred = model.predict(X)
    y_pred = pd.DataFrame(y_pred, index=utterances, columns=label_mapping)

    f1_train_macro = {}
    for i, (truth, pred) in enumerate(zip(y.values.T, y_pred.values.T)):
        tag_name = label_mapping[i]
        assert tag_name == y.columns[i]
        f1_train_macro[tag_name] = f1_score(truth, pred)
    f1_train_macro = pd.Series(f1_train_macro)
    print(f"Train/Test F1 Score: {f1_train_macro.mean():0.3f}")
    return f1_train_macro


def google_sheet_to_csv(google_sheet_link=GOOGLE_SHEET_LINK):
    response = requests.get(google_sheet_link)
    csv_content = response.content
    csv_file = io.BytesIO(csv_content)
    return csv_file


def get_installed_packages():
    """Returns the filepath to a list of packages in the development environment when the model was created

    Output
    [
        'jupyter==1.0.0',
        'jupyter-console==6.4.4',
        'jupyter-events==0.6.3',
        'jupyter_client==8.0.1',
        'jupyter_core==5.1.5',
        ...
    ]
    """
    # Run a python terminal command from within the function
    process = subprocess.Popen(
        ["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Extract result and handle errors
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error occurred: {error}")
        return []

    # Convert output to a local file
    package_list = output.strip().split("\n")
    file_path = "installed_packages.txt"
    with open(DATA_DIR / f"model_context_{CURRENT_DATE}.txt", "w") as file:
        file.write("\n".join(package_list))
    return DATA_DIR / f"model_context_{CURRENT_DATE}.txt"


# TODO: Why did taking out if __name__ == '__main__' make this code work?
# TODO2: Was it because of df_tags being in main and not the other functions?


def run_multilabel_model_development_process():
    df = multilabel_to_unilabel(df=GOOGLE_SHEET_LINK)
    df_tags = tags_from_labels(df).astype(int)

    results = train_and_save(
        df=df,
        df_tags=df_tags,
        filepath=DATA_DIR / f"multi_intent_recognizer_{CURRENT_DATE}.pkl",
        test_size=0.2,
    )
    # retrain it on all the available data for best accuracy
    results = train_and_save(
        df=df,
        df_tags=df_tags,
        filepath=DATA_DIR / f"multi_intent_recognizer_{CURRENT_DATE}.pkl",
        test_size=0,
    )
    results = train_and_save(df=df, df_tags=df_tags, test_size=0)

    csv_file = google_sheet_to_csv(GOOGLE_SHEET_LINK)
    model_requirements_file = get_installed_packages()

    if OBJECT_STORAGE_PROVIDER == "gcs":
        obj_store_results = upload_to_google_cloud(
            csv_file,
            model_requirements_file,
            DATA_DIR / f"multi_intent_recognizer_{CURRENT_DATE}.pkl",
        )
    elif OBJECT_STORAGE_PROVIDER == "s3":
        obj_store_results = upload_to_digital_ocean(
            csv_file,
            model_requirements_file,
            DATA_DIR / f"multi_intent_recognizer_{CURRENT_DATE}.pkl",
        )

    print(results)
    return results
