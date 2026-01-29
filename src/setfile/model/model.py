import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score

data = pd.read_csv('final_dataset1.csv')

target_size = 2000

final_data = (
    data
    .groupby("label")
    .apply(lambda x : x.sample(n=min(len(x),target_size), random_state=42))
    .reset_index(drop=True)
)

final_data = final_data.dropna(subset=['text'])
final_data = final_data[final_data['text'].apply(lambda x: isinstance(x, str))]

x = final_data['text']
y = final_data['label']

x_train, x_test, y_train, y_test = train_test_split(x, y ,test_size = 0.2 , random_state=42)

clf = SVC(C=10,kernel='rbf')

pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(max_features=5000)),
    ('classifier',clf)
])

pipeline.fit(x_train, y_train)

pred = pipeline.predict(x_test)

print("The Accuracy score is: ",accuracy_score(y_test, pred))
print("The classification report is: \n",classification_report(y_test, pred))

sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.title('Pipeline Confusion Matrix')
plt.show()

joblib.dump(pipeline, 'doc_classifier_svm.pkl')