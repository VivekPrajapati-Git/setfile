import joblib
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Expanded synthetic dataset for BETTER YIELD and ACCURACY
# Added 'video', 'image', 'audio' classes (19 total)
data = [
    # MeetingMinutes
    ("Minutes of the meeting held on 2023-10-27. Attendees: John, Jane.", "MeetingMinutes"),
    ("Action items: 1. Fix bug in login. 2. Update documentation.", "MeetingMinutes"),
    ("Agenda for the weekly sync. Discuss project roadmap and timelines.", "MeetingMinutes"),
    ("Meeting called to order at 10:00 AM. Quorum present.", "MeetingMinutes"),
    ("Decision log: Feature A approved for next sprint.", "MeetingMinutes"),

    # articles
    ("Top 10 travel destinations for 2024. Explore the world.", "articles"),
    ("Breaking news: Python 4.0 released today with major changes.", "articles"),
    ("The future of AI in healthcare. An in-depth look at trends.", "articles"),
    ("5 tips for better sleep. Improving your daily routine.", "articles"),
    ("Opinion: Why remote work is here to stay. A comprehensive analysis.", "articles"),

    # blog
    ("Welcome to my personal blog. Today I want to share my thoughts.", "blog"),
    ("How to bake a cake. A step-by-step guide for beginners.", "blog"),
    ("My journey learning Rust. It has been a challenging ride.", "blog"),
    ("Review of the latest iPhone. Is it worth the upgrade?", "blog"),
    ("Travel diary: My trip to Japan. The food was amazing.", "blog"),

    # book
    ("Chapter 1: The beginning. It was a dark and stormy night.", "book"),
    ("The Lord of the Rings. Prologue. Concerning Hobbits.", "book"),
    ("Table of Contents. Introduction, Chapter 1, Chapter 2, Index.", "book"),
    ("Copyright 2023 by Author Name. All rights reserved.", "book"),
    ("Epilogue. And they lived happily ever after.", "book"),

    # code
    ("def hello_world(): print('Hello world')", "code"),
    ("import numpy as np; x = np.array([1, 2, 3])", "code"),
    ("class MyClass: def __init__(self): pass", "code"),
    ("SELECT * FROM users WHERE id = 1;", "code"),
    ("<html><body><h1>Hello</h1></body></html>", "code"),
    ("console.log('Hello'); var x = 10;", "code"),
    ("public static void main(String[] args) { }", "code"),
    ("import pandas as pd; df = pd.read_csv('data.csv')", "code"),
    ("for i in range(10): print(i)", "code"),

    # email
    ("Subject: Project Update. Hi Team, just wanted to let you know.", "email"),
    ("Dear Customer, Thank you for your recent purchase. Order shipped.", "email"),
    ("Can we reschedule our call for tomorrow? Let me know.", "email"),
    ("Fwd: Important announcement. Please read carefully.", "email"),
    ("Best regards, John Doe. Sent from my iPhone.", "email"),

    # invoice
    ("INVOICE #1023. Total Amount: $500.00. Due Date: 2023-11-30.", "invoice"),
    ("Bill to: John Doe. Services rendered: Web Development.", "invoice"),
    ("Payment terms: Net 30. Please remit payment to account X.", "invoice"),
    ("Tax Invoice. VAT ID: 123456789. Subtotal: $100. Tax: $10.", "invoice"),
    ("Invoice Date: Jan 1 2024. Please pay by wire transfer.", "invoice"),

    # receipt
    ("Walmart Receipt. Total: $45.20. Thank you for shopping with us.", "receipt"),
    ("Coffee Shop. Latte: $5.00. Muffin: $3.00. Total: $8.00.", "receipt"),
    ("Uber Trip Receipt. Fare: $12.50. Date: 2023-12-01.", "receipt"),
    ("Payment success. Transaction ID: 987654321.", "receipt"),
    ("Amazon Order Confirmation. Total: $29.99.", "receipt"),

    # legal
    ("This agreement is made between Party A and Party B.", "legal"),
    ("Terms and Conditions. By using this service you agree.", "legal"),
    ("Privacy Policy. We value your privacy and data security.", "legal"),
    ("Non-Disclosure Agreement (NDA). Confidential information.", "legal"),
    ("In witness whereof, the parties have signed this contract.", "legal"),

    # medicalreport
    ("Patient Name: John Doe. Diagnosis: Common Cold.", "medicalreport"),
    ("Prescription: Ibuprofen 200mg twice daily.", "medicalreport"),
    ("Clinical trial results shows 95% efficacy.", "medicalreport"),
    ("Medical History: No known allergies. Previous surgeries: None.", "medicalreport"),
    ("Lab Report. Blood pressure: 120/80. Heart rate: 72 bpm.", "medicalreport"),

    # research
    ("Abstract: This paper explores the impact of AI on software.", "research"),
    ("Conclusion: The results demonstrate a significant improvement.", "research"),
    ("Methodology: We conducted a survey of 1000 participants.", "research"),
    ("References: [1] Smith et al., Journal of AI, 2023.", "research"),
    ("Keywords: Machine Learning, Neural Networks, Deep Learning.", "research"),

    # resume
    ("John Doe. Software Engineer. Skills: Python, Java, C++.", "resume"),
    ("Curriculum Vitae. Education: PhD in Computer Science.", "resume"),
    ("Work Experience: Senior Developer at Google. 2018-Present.", "resume"),
    ("Certified Scrum Master. Fluent in English and Spanish.", "resume"),
    ("Objective: To obtain a challenging position in a reputable firm.", "resume"),

    # presentation
    ("Slide 1: Agenda. Introduction, Growth, Q&A.", "presentation"),
    ("Key Takeaways. We need to focus on user retention.", "presentation"),
    ("Q3 Performance Review. Sales up by 15%.", "presentation"),
    ("Thank you. Any questions? Contact: email@example.com.", "presentation"),
    ("Presentation Title: The Future of Cloud Computing.", "presentation"),

    # financial
    ("Balance Sheet as of Dec 31. Assets: $1M. Liabilities: $500k.", "financial"),
    ("Profit and Loss Statement. Revenue: $200k. Expenses: $100k.", "financial"),
    ("Cash Flow Statement. Net cash from operating activities.", "financial"),
    ("Stock Portfolio. AAPL: 100 shares. GOOGL: 50 shares.", "financial"),
    ("Budget vs Actuals. Q1 Variance: -5%.", "financial"),

    # notes
    ("To-Do List: Buy milk, call mom, gym at 6pm.", "notes"),
    ("Idea for new app: A social network for cats.", "notes"),
    ("Reminder: Doctor appointment on Tuesday.", "notes"),
    ("Note to self: Don't forget to backup the database.", "notes"),
    ("Grocery list: Bread, Eggs, Butter, Cheese.", "notes"),

    # report
    ("UIDAI Report. Aadhaar Enrollment Statistics. Government of India.", "report"),
    ("Monthly Status Report. Project X. Progress: 50% complete.", "report"),
    ("Annual Report 2023. Strategic Goals and Achievements.", "report"),
    ("Enrollment Report. Total registered users: 1 Million.", "report"),
    ("Executive Summary. Overview of the findings and recommendations.", "report"),

    # video (Synthetic text from reader.py)
    ("This is a video file format mp4 movie clip recording.", "video"),
    ("This is a video file format avi movie clip recording.", "video"),
    ("This is a video file format mov movie clip recording.", "video"),
    ("This is a video file format mkv movie clip recording.", "video"),
    ("This is a video file format webm movie clip recording.", "video"),

    # image (Synthetic text from reader.py)
    ("This is an image file format jpg photo picture graphic.", "image"),
    ("This is an image file format jpeg photo picture graphic.", "image"),
    ("This is an image file format png photo picture graphic.", "image"),
    ("This is an image file format gif photo picture graphic.", "image"),
    ("This is an image file format bmp photo picture graphic.", "image"),
    ("This is an image file format svg photo picture graphic.", "image"),
    ("This is an image file format webp photo picture graphic.", "image"),

    # audio (Synthetic text from reader.py)
    ("This is an audio file format mp3 sound music recording song.", "audio"),
    ("This is an audio file format wav sound music recording song.", "audio"),
    ("This is an audio file format flac sound music recording song.", "audio"),
    ("This is an audio file format aac sound music recording song.", "audio"),
    ("This is an audio file format ogg sound music recording song.", "audio"),
    ("This is an audio file format m4a sound music recording song.", "audio"),
]

def train_model():
    print(f"Training on {len(data)} examples with {len(set(d[1] for d in data))} classes...")
    df = pd.DataFrame(data, columns=['text', 'label'])
    
    # Split data (though we will train on full set for final model)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.1, random_state=42)
    
    # Create Pipeline
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english')),
        ('classifier', SVC(kernel='linear', probability=True))
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluation on validation set:")
    predictions = pipeline.predict(X_test)
    print(classification_report(y_test, predictions, zero_division=0))
    
    # Retrain on FULL dataset for production
    print("Retraining on full dataset...")
    pipeline.fit(df['text'], df['label'])
    
    # Save
    model_path = Path(__file__).resolve().parent.parent / "src/setfile/model/doc_classifier_svm.pkl"
    print(f"Saving model to {model_path}...")
    joblib.dump(pipeline, model_path)
    print("Model saved successfully.")

if __name__ == "__main__":
    train_model()
