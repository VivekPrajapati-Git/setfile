# import joblib
# from pathlib import Path
# import warnings
# from sklearn.exceptions import InconsistentVersionWarning

# warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# def prediction(text):
#     path = Path(__file__).resolve().parent.parent/"model/doc_classifier_svm.pkl"
#     model = joblib.load(path)
#     predict = model.predict([text])
#     return predict

import torch
from ..model.titan import TiTAN_MAG
from ..core.embed_model import load_model
from pathlib import Path

def predict(text):
    mapping = {
        0: "MeetingMinutes", 1: "articles", 2: "blog", 3: "book", 
        4: "code", 5: "email", 6: "invoice", 7: "legal", 
        8: "medicalreport", 9: "research", 10: "resume"
    }

    model = TiTAN_MAG(
        embed_dim=768,
        num_classes=11
    )

    model_path = Path(__file__).resolve().parent.parent/'model/best_titan_mag_model.pth'
    state_dict = torch.load(model_path,map_location=torch.device('cpu') ,weights_only=True) 
    model.load_state_dict(state_dict)

    with torch.no_grad():
        embeddings = load_model(text)
        pred = model(embeddings)
        probabilites = torch.softmax(pred, dim=1)
        prediction = torch.argmax(probabilites,dim=1).item()

    label_name = mapping[prediction]
    return label_name