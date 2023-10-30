"""
To predict intent tags within your application, run the following:

>> from mathtext.predict_intent import predict_message_intent
>> predict_message_intent('Hello world message from user') # doctest:
{ 
  'type': 'intent',
  'data': ..., 
  'confidence': ...,
  'intents': [
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
  ],
  'predict_probas': ...
}
"""
import joblib
import pandas as pd

from joblib import Memory
from pathlib import Path

from mathtext.constants import DATA_DIR
from mathtext.models.storage import download_model  # , get_file_size, split_bucket_key
from mathtext.constants import (
    CURRENT_MODEL_LINK as MODEL_KEY,
    OBJECT_STORAGE_NAME as MODEL_BUCKET,
)

MODEL_BUCKET = Path(MODEL_BUCKET)
MODEL_KEY = Path(MODEL_KEY)

# MANDATORY imports for joblib to unpickle the model (pipeline)
from mathtext.models.multilabel_intent_recognition import (  # noqa
    BERTEncoder,
    Pipeline,
    OneVsRestClassifier,
    LogisticRegression,
    SentenceTransformer,
    BaseEstimator,
    TransformerMixin,
)


INTENT_RECOGNIZER_MODEL = None

cache_directory = Path(DATA_DIR / "cache")
memory = Memory(cache_directory, verbose=0, backend="local")


def predict_message_intent(message, min_confidence=0.5):
    """Runs the trained model pipeline on a student's message

    >>> result = predict_message_intent('I want to change topics')
    >>> sorted(result.keys())
    ['confidence', 'data', 'intents', 'predict_probas', 'type']
    """
    global INTENT_RECOGNIZER_MODEL
    INTENT_RECOGNIZER_MODEL = INTENT_RECOGNIZER_MODEL or joblib.load(
        download_model(Path(MODEL_BUCKET) / MODEL_KEY)
    )

    pred_probas = INTENT_RECOGNIZER_MODEL.predict_proba([message])[0]

    predicted_labels_and_scores = pd.Series(
        list(pred_probas), index=INTENT_RECOGNIZER_MODEL.label_mapping
    )

    predictions = (
        predicted_labels_and_scores.sort_values(ascending=False)[:3].to_dict().items()
    )

    intents = [
        {"type": "intent", "data": name, "confidence": conf}
        for name, conf in predictions
    ]

    data = intents[0]["data"]
    confidence = intents[0]["confidence"]
    if confidence < min_confidence:
        data = "no_match"
        confidence = 0

    return {
        "type": "intent",
        "data": data,
        "confidence": confidence,
        "intents": intents,
        "predict_probas": [
            {"type": "intent", "data": name, "confidence": conf}
            for name, conf in predicted_labels_and_scores.to_dict().items()
        ],
    }


predict_intent = memory.cache(predict_message_intent)


async def clean_prediction_cache():
    memory.reduce_size(items_limit=500, bytes_limit=1048576)


def predict_intents_list(text, num_intents=None):
    """Return ranked list of (intent_label, confidence) 2-tuple

    Sample Output:
    [('answer', 0.7568096903748207),
     ('numerical_expression', 0.25867391608346874),
     ('support', 0.23595954822965573),
     ('exit', 0.2259397417552966),
     ('negative_ux', 0.22204299015973564),
     ('next_lesson', 0.19376506261045864),
     ...]

    >>> result = predict_intents_list('you are mean forty 2')
    >>> type(result)
    <class 'list'>
    >>> bool(len(result))
    True
    """
    global INTENT_RECOGNIZER_MODEL
    INTENT_RECOGNIZER_MODEL = INTENT_RECOGNIZER_MODEL or joblib.load(
        download_model(Path(MODEL_BUCKET) / MODEL_KEY)
    )

    pred_probas = INTENT_RECOGNIZER_MODEL.predict_proba([text])[0]

    predictions = pd.Series(
        list(pred_probas), index=INTENT_RECOGNIZER_MODEL.label_mapping
    )

    predictions = predictions.sort_values(ascending=False)
    return list(zip(predictions.index.values, predictions.values))
