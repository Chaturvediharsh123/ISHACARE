import numpy as np

def predict_ml(data):

    features = np.array([
        data.get("glucose", 0),
        data.get("ldl", 0),
        data.get("hemoglobin", 0)
    ]).reshape(1, -1)

    return "Moderate Risk"