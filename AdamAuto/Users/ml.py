import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def train_model():
    # Load the data
    data = pd.read_csv(os.path.join(BASE_DIR, 'car_reviews_with_feedback.csv'))

    # Prepare the features and target
    X = data[['manufacturer', 'model', 'year', 'comfort', 'performance', 'fuel_efficiency', 'safety', 'technology']].copy()
    y = data['description'].copy()  # Use description as the target

    # Encode categorical variables
    le_manufacturer = LabelEncoder()
    le_model = LabelEncoder()
    le_description = LabelEncoder()
    X['manufacturer'] = le_manufacturer.fit_transform(X['manufacturer'])
    X['model'] = le_model.fit_transform(X['model'])
    y = le_description.fit_transform(y)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy}")

    # Save the model and label encoders
    joblib.dump(model, os.path.join(BASE_DIR, 'feedback_model.joblib'))
    joblib.dump(le_manufacturer, os.path.join(BASE_DIR, 'le_manufacturer.joblib'))
    joblib.dump(le_model, os.path.join(BASE_DIR, 'le_model.joblib'))
    joblib.dump(le_description, os.path.join(BASE_DIR, 'le_description.joblib'))

def make_prediction(manufacturer, model, year, comfort, performance, fuel_efficiency, safety, technology):
    # Load the trained model and label encoders
    clf = joblib.load(os.path.join(BASE_DIR, 'feedback_model.joblib'))
    le_manufacturer = joblib.load(os.path.join(BASE_DIR, 'le_manufacturer.joblib'))
    le_model = joblib.load(os.path.join(BASE_DIR, 'le_model.joblib'))
    le_description = joblib.load(os.path.join(BASE_DIR, 'le_description.joblib'))

    # Check if manufacturer and model are in the trained data
    if manufacturer not in le_manufacturer.classes_ or model not in le_model.classes_:
        return "Prediction for this car is not currently available"

    # Prepare the input data
    input_data = pd.DataFrame({
        'manufacturer': [manufacturer],
        'model': [model],
        'year': [year],
        'comfort': [comfort],
        'performance': [performance],
        'fuel_efficiency': [fuel_efficiency],
        'safety': [safety],
        'technology': [technology]
    })

    # Encode categorical variables
    input_data['manufacturer'] = le_manufacturer.transform([manufacturer])
    input_data['model'] = le_model.transform([model])

    # Make prediction
    prediction = clf.predict(input_data)
    description = le_description.inverse_transform(prediction)[0]

    return description

if __name__ == "__main__":
    train_model()
    
    # Sample prediction
    sample_prediction = make_prediction(
        manufacturer="Toyota",
        model="Camry",
        year=2022,
        comfort=8,
        performance=7,
        fuel_efficiency=9,
        safety=8,
        technology=7
    )
    print(f"Sample prediction: {sample_prediction}")
