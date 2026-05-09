"""
Credit Card Fraud Detection Model (Beginner Friendly)

This script demonstrates how to build a simple machine learning model
to detect fraudulent credit card transactions using a Random Forest algorithm.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import os

# 1. Load dataset from CSV
# Make sure you have a 'credit_card_data.csv' file in the same directory.
# If you don't have one, run 'python generate_dataset.py' first to create a dummy dataset.
file_path = 'credit_card_data.csv'

if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found.")
    print("Please run 'python generate_dataset.py' to generate a sample dataset.")
    exit()

print("Loading dataset...")
data = pd.read_csv(file_path)

# 2. Handle missing values
# If there are any missing values in our data, we fill them with 0.
# In a real-world scenario, you might use more advanced techniques like filling with the mean/median.
print("Handling missing values...")
data.fillna(0, inplace=True)

# 3. Separate features (X) and target labels (y)
# 'Is_Fraud' is our target column. 1 means Fraud, 0 means Normal.
# The rest of the columns are our features (transaction amount, location, etc.)
X = data.drop('Is_Fraud', axis=1) 
y = data['Is_Fraud']

# 4. Split dataset into training and testing
# We use 80% of the data to train the model, and 20% to test its performance.
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the model
# We are using a Random Forest Classifier.
# It works by creating many decision trees and combining their results.
print("Training the Random Forest model (this might take a few seconds)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Make predictions on the test set
print("Evaluating the model...")
predictions = model.predict(X_test)

# 7. Show accuracy score
# Accuracy is the percentage of correct predictions made by the model.
accuracy = accuracy_score(y_test, predictions)
print(f"\n--- Results ---")
print(f"Accuracy Score: {accuracy * 100:.2f}%")

# 8. Show confusion matrix
# A confusion matrix shows True Positives, True Negatives, False Positives, and False Negatives.
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, predictions)
print(cm)
print("(Top-left: True Negatives | Top-right: False Positives)")
print("(Bottom-left: False Negatives | Bottom-right: True Positives)")

# 9. Save trained model as model.pkl using pickle
# Saving the model allows us to reuse it later without retraining.
print("\nSaving the trained model...")
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully as 'model.pkl'.")
