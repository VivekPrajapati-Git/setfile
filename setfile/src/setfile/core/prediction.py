import joblib
from pathlib import Path
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

def prediction(text):
    path = Path(__file__).resolve().parent.parent/"model/doc_classifier_svm.pkl"
    model = joblib.load(path)
    predict = model.predict([text])
    return predict
