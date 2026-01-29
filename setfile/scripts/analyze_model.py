import joblib
from pathlib import Path
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import sys

# Define synthetic data for testing - UPDATED with new classes
test_data = [
    # Original Classes
    ("Minutes of the meeting held on 2023-10-27. Attendees: John, Jane. Discussion: Budget approval.", "MeetingMinutes"),
    ("Top 10 travel destinations for 2024. Explore the world with these amazing spots.", "articles"),
    ("Welcome to my personal blog. Today I want to share my thoughts on coding.", "blog"),
    ("Chapter 1: The beginning. It was a dark and stormy night.", "book"),
    ("def hello_world(): print('Hello world')", "code"),
    ("Subject: Project Update. Hi Team, just wanted to let you know the project is on track.", "email"),
    ("INVOICE #1023. Total Amount: $500.00. Due Date: 2023-11-30.", "invoice"),
    ("This agreement is made between Party A and Party B. All rights reserved.", "legal"),
    ("Patient Name: John Doe. Diagnosis: Common Cold. Prescription: Rest and fluids.", "medicalreport"),
    ("Abstract: This paper explores the impact of AI on software engineering.", "research"),
    ("John Doe. Software Engineer. Skills: Python, Java, C++. Experience: 5 years.", "resume"),
    
    # New Classes
    ("Starbucks Receipt. Latte $5.45. Total $5.45. Visa **** 1234.", "receipt"),
    ("Target Store. Subtotal $42.00. Tax $3.00. Total $45.00.", "receipt"),
    
    ("Slide 3: Quarterly Earnings. Revenue up 20% YoY.", "presentation"),
    ("Agenda: 1. Intro 2. Demo 3. Q&A. Thank you for coming.", "presentation"),
    
    ("Q4 Balance Sheet. Assets: $2M. Liabilities: $1.5M. Equity: $0.5M.", "financial"),
    ("Stock Performance Report. VOO +10%. SPY +12%. Portfolio Value.", "financial"),
    
    ("Grocery list: Milk, Bread, Cheese, Eggs. Don't forget.", "notes"),
    ("Idea: A mobile app that tracks water intake. Reminder: Drink more water.", "notes"),
]

def analyze_performance():
    model_path = Path(__file__).resolve().parent.parent / "src/setfile/model/doc_classifier_svm.pkl"
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        
        texts = [item[0] for item in test_data]
        true_labels = [item[1] for item in test_data]
        
        print(f"Running predictions on {len(texts)} test samples...")
        predictions = model.predict(texts)
        
        print("\nClassification Report:")
        print(classification_report(true_labels, predictions, zero_division=0))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(true_labels, predictions))
        
        print("\nDetailed Predictions:")
        for text, true, pred in zip(texts, true_labels, predictions):
            status = "CORRECT" if true == pred else "WRONG"
            print(f"[{status}] Text: '{text[:50]}...' -> True: {true}, Pred: {pred}")

    except Exception as e:
        print(f"Error analyzing model: {e}")

if __name__ == "__main__":
    analyze_performance()
