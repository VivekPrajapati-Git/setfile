import sys
from pathlib import Path
import os

# Set up path to import src
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(src_path))

try:
    from setfile.utils.reader import read_file
    from setfile.core.prediction import prediction
    from setfile.utils.logger import logger as log
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_directory(path):
    folder_path = Path(path)
    if not folder_path.exists():
        print(f"Directory not found: {path}")
        return

    print(f"Scanning directory: {path}")
    print("-" * 50)
    print(f"{'File Name':<40} | {'Prediction':<20} | {'Status'}")
    print("-" * 50)

    files_processed = 0
    predictions = {}
    
    for file in folder_path.iterdir():
        if file.is_file():
            try:
                # Handle filename printing carefully due to potential encoding issues
                try:
                    display_name = file.name
                    # Force string conversion just in case
                    str(display_name)
                    if len(display_name) > 35:
                        display_name = display_name[:32] + "..."
                except:
                    display_name = "[Unprintable Filename]"

                text = read_file(str(file))
                
                # Check if text is empty (unsupported file)
                if not text:
                    status = "Skipped (Empty/Unsupported)"
                    pred_label = "N/A"
                else:
                    predict = prediction(text)
                    pred_label = predict[0]
                    status = "Predicted"
                    predictions[file.name] = pred_label

                print(f"{display_name:<40} | {pred_label:<20} | {status}")
                files_processed += 1
                
            except Exception as e:
                print(f"{file.name:<40} | {'Error':<20} | {str(e)}")

    print("-" * 50)
    print(f"Total files scanned: {files_processed}")
    
    # Generate summary stats
    if predictions:
        print("\nSummary of Predictions:")
        from collections import Counter
        counts = Counter(predictions.values())
        for label, count in counts.items():
            print(f"- {label}: {count}")

if __name__ == "__main__":
    target_dir = r"C:\Users\Abhijeet\Desktop"
    # Allow overriding via arg
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    test_directory(target_dir)
