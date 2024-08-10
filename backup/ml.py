import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_json("output.json")

# Convert symptoms to tokenized format
symptoms = df.drop(columns=['prognosis', 'drug'])
symptoms_text = symptoms.apply(lambda x: ' '.join(map(str, x)), axis=1)

# Tokenize symptoms
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(symptoms_text)

# Target variable
y = df['prognosis']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Evaluate model
y_pred = rf_classifier.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Plot confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", xticklabels=rf_classifier.classes_, yticklabels=rf_classifier.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Function to predict prognosis and drug
def predict_prognosis(symptoms_str):
    symptoms_vectorized = vectorizer.transform([symptoms_str])
    prognosis = rf_classifier.predict(symptoms_vectorized)[0]
    drug = df[df['prognosis'] == prognosis]['drug'].iloc[0]
    return prognosis, drug

# Test prediction function
symptoms_str = "hello i am having acidity indigestion headache,what to do?"
prognosis, drug = predict_prognosis(symptoms_str)
print(f"\nSymptoms: {symptoms_str}")
print(f"Predicted Prognosis: {prognosis}")
print(f"Prescribed Drug: {drug}")
