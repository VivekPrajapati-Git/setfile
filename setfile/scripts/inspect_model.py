import joblib
from pathlib import Path
import sys

# Add src to path to allow importing if needed (though we load pkl directly)
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

def inspect_model():
    model_path = Path(__file__).resolve().parent.parent / "src/setfile/model/doc_classifier_svm.pkl"
    try:
        model = joblib.load(model_path)
        print(f"Model Type: {type(model)}")
        
        if hasattr(model, 'classes_'):
            print(f"Classes: {model.classes_}")
        else:
            print("Model does not have 'classes_' attribute.")

        if hasattr(model, 'best_params_'):
            print(f"Best Params: {model.best_params_}")

        # Check if it's a pipeline
        if hasattr(model, 'steps'):
            print("Pipeline Steps:")
            for name, step in model.steps:
                print(f"  - {name}: {type(step)}")
                
    except Exception as e:
        print(f"Error loading model: {e}")

if __name__ == "__main__":
    inspect_model()
