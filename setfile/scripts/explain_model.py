import joblib
import pandas as pd
from pathlib import Path
import numpy as np

def explain_model():
    model_path = Path(__file__).resolve().parent.parent / "src/setfile/model/doc_classifier_svm.pkl"
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        
        # Access Pipeline steps
        vectorizer = model.named_steps['vectorizer']
        classifier = model.named_steps['classifier']
        
        feature_names = vectorizer.get_feature_names_out()
        
        print("\n--- Model Interpretability: Top 10 Keywords per Class ---")
        print("This shows the actual 'INNER CONTENT' words the model looks for.\n")
        
        if classifier.kernel == 'linear':
            # For linear kernel, we can directly look at coefficients
            for i, class_label in enumerate(classifier.classes_):
                # Get coefficients for this class
                # (Note: In multiclass SVC, coef_ shape depends on the scheme, usually one-vs-rest)
                # But Scikit-learn SVC with linear kernel stores coef_
                
                # Careful: SVC with multi-class 'ovr' (one-vs-rest) has coef_ of shape (n_classes, n_features)
                # If 'ovo' (one-vs-one), it's (n_classes * (n_classes - 1) / 2, n_features)
                
                # Let's inspect shapes first to be safe, but usually we can find top weighted features
                pass
                
            # If shape matches classes, we can print easily. 
            # If standard SVC (one-vs-one default), interpretation is harder.
            # However, our training script used default SVC. 
            # Let's check coef_ shape dynamically.
            
            if hasattr(classifier, 'coef_'):
               coefs = classifier.coef_
               # Use dense array for sorting
               if hasattr(coefs, 'toarray'):
                   coefs = coefs.toarray()
               
               print(f"Coefficient shape: {coefs.shape}")
               print(f"Classes: {classifier.classes_}")
               
               # If One-vs-One (default for SVC), coefs are interactions between pairs.
               # If we want direct feature importance, LinearSVC or SVC(decision_function_shape='ovr') is better.
               # BUT, we can still try to infer or just print support vectors.
               
               # Actually, let's just re-train a LinearSVC or use the existing ONE and try to interpret.
               # If the model uses 'ovr' (LinearsVC does this), it's easy.
               # If 'ovo' (SVC default), we have row for each pair.
               
               # SIMPLER APPROACH for demonstration if coefficients are complex:
               # We simply print the vectorizer vocabulary to show it tracks thousands of words.
               # AND if possible, print high coefficient words.
               
               # Let's try to map coefficients.
               # If coefs.shape[0] == len(classes), it's OVR.
               # If coefs.shape[0] == n*(n-1)/2, it's OVO.
               
               if coefs.shape[0] == len(classifier.classes_):
                   # One-Vs-Rest mode
                   for idx, label in enumerate(classifier.classes_):
                       top10 = np.argsort(coefs[idx])[-10:]
                       top_words = [feature_names[i] for i in top10]
                       print(f"Class '{label}': {', '.join(top_words)}")
               else:
                   # One-Vs-One mode (likely). 
                   # It's harder to say "Class A relies on Word X" globally.
                   # Just print that it uses {len(feature_names)} distinct words.
                   print(f"Model uses {len(feature_names)} unique words/features from the inner content.")
                   print("Since the model is trained in One-vs-One mode, specific global keywords are complex to extract.")
                   print("However, here is a sample of features it tracks:")
                   print(f"{feature_names[100:120]}")
            else:
                print("Model does not expose linear coefficients.")
                
        else:
            print("Model uses a non-linear kernel. Cannot show simple feature weights.")
            
    except Exception as e:
        print(f"Error explaining model: {e}")

if __name__ == "__main__":
    explain_model()
