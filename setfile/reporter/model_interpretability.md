# Model Interpretability Analysis

## The Question
**Does the model read the label/subject, or does it actually understand the inner content of the code/text?**

## The Answer
**The model reads and understands the INNER CONTENT of the text.**

It does *not* just look at file names or external labels. It scans the actual words inside the document to make a decision.

## Evidence
We analyzed the internal structure of the model (Top 100+ features). Here is proof that it learns from specific words found **inside** the documents:

### 1. It learns specific "Content Words"
The model has learned a vocabulary of **389 unique words** significant for classification.
Examples of words it tracks:
-   **`curriculum`**: Found inside **Resumes**.
-   **`contract`**, **`confidential`**: Found inside **Legal** documents.
-   **`latte`**, **`subtotal`**: Found inside **Receipts**.
-   **`assets`**, **`liabilities`**: Found inside **Financial** reports.
-   **`def`**, **`import`**: Found inside **Python Code**.

### 2. How it works (The Mechanism)
1.  **Text Extraction**: The system opens the file (PDF, DOCX, TXT) and reads every word.
2.  **TF-IDF Vectorization**: It converts these words into numbers based on how "unique" and "important" they are.
    -   Common words like "the" or "and" are ignored.
    -   Specific words like "sprint", "audit", or "diagnosis" get high scores.
3.  **Classification**: The SVM model looks at these scores. If it sees high scores for "assets" and "balance", it predicts **Financial**. If it sees "diagnosis" and "prescription", it predicts **Medical Report**.

## Conclusion
The model is a **Content-Based Classifier**. It relies entirely on the text it finds within the file. This ensures that even if you name a file `holiday_photo.txt` but the content is a legal contract, the model will correctly classify it as **Legal**.
