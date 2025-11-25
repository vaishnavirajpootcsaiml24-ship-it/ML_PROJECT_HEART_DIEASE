from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Load trained model and scaler
print("Loading model...")
with open('heart_disease_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

print("✅ Model loaded successfully!")

# Risk recommendations
RECOMMENDATIONS = {
    0: [  # Low Risk
        "Maintain a balanced diet rich in fruits and vegetables",
        "Exercise 3-5 times a week for at least 30 minutes",
        "Keep regular health checkups annually",
        "Maintain healthy weight and BMI",
        "Stay hydrated and get adequate sleep"
    ],
    1: [  # Medium Risk
        "Reduce salt and sugar intake significantly",
        "Start light cardio exercise daily (walking, cycling)",
        "Consult a physician for risk management plan",
        "Monitor blood pressure and cholesterol regularly",
        "Consider stress management techniques (yoga, meditation)",
        "Limit processed foods and saturated fats"
    ],
    2: [  # High Risk
        "Avoid smoking and alcohol completely",
        "Follow a strict low-fat, low-sodium diet",
        "Immediate medical consultation recommended",
        "Take prescribed medications regularly",
        "Monitor vital signs daily",
        "Consider cardiac rehabilitation program",
        "Emergency contact: Keep doctor's number handy"
    ]
}

@app.route('/')
def home():
    return jsonify({
        'message': 'Heart Disease Detection API is running!',
        'endpoints': ['/predict', '/health']
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Extract features (exercise removed)
        age = int(data['age'])
        gender = 1 if data['gender'].lower() == 'male' else 0
        bp = int(data['bp'])
        cholesterol = int(data['cholesterol'])
        heart_rate = int(data['heartRate'])
        smoking = 1 if data['smoking'].lower() == 'yes' else 0
        diabetes = 1 if data['diabetes'].lower() == 'yes' else 0
        bmi = float(data['bmi'])
        
        # Create feature array (exercise removed)
        features = np.array([[age, gender, bp, cholesterol, heart_rate,
                             smoking, diabetes, bmi]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Risk level
        risk_levels = ['Low', 'Medium', 'High']
        risk_level = risk_levels[prediction]
        
        # Confidence score
        confidence = float(prediction_proba[prediction] * 100)
        
        # Recommendations
        recommendations = RECOMMENDATIONS[prediction]
        
        # Calculate risk factors
        risk_factors = []
        if age > 55:
            risk_factors.append(f"Age ({age}) is above 55")
        if bp > 140:
            risk_factors.append(f"Blood Pressure ({bp}) is high")
        if cholesterol > 240:
            risk_factors.append(f"Cholesterol ({cholesterol}) is elevated")
        if smoking == 1:
            risk_factors.append("Smoking increases risk significantly")
        if diabetes == 1:
            risk_factors.append("Diabetes is a major risk factor")
        if bmi > 30:
            risk_factors.append(f"BMI ({bmi}) indicates obesity")
        
        # Response
        response = {
            'success': True,
            'risk_level': risk_level,
            'confidence': round(confidence, 2),
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'probabilities': {
                'Low': round(float(prediction_proba[0]) * 100, 2),
                'Medium': round(float(prediction_proba[1]) * 100, 2),
                'High': round(float(prediction_proba[2]) * 100, 2)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("\n Starting Flask API server...")
    print(" API running on: http://localhost:5000")
    print(" Prediction endpoint: http://localhost:5000/predict")
    app.run(debug=True, port=5000)