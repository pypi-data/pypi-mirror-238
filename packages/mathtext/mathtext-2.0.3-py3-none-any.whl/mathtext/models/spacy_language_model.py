import spacy  # https://spacy.io

nlp = None

MODEL_NAME = 'en_core_web_sm'
try:
    nlp = spacy.load(MODEL_NAME)
except Exception:
    pass

# Faster pytest approach, relies on en_core_web_sm which is not installable within pypi package
# Allows you to pip install en_core_web_sm
if nlp is None:
    if MODEL_NAME == 'en_core_web_md':
        import en_core_web_md
        nlp = en_core_web_md.load()
    elif MODEL_NAME == 'en_core_web_lg':
        import en_core_web_lg
        nlp = en_core_web_lg.load()
    elif MODEL_NAME.lower()[:2] == 'en':
        import en_core_web_sm
        nlp = en_core_web_sm.load()

if nlp is None:
    try:
        spacy.cli.download(MODEL_NAME)
        nlp = spacy.load(MODEL_NAME)
    except Exception:
        pass


assert nlp is not None
