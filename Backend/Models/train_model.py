import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

np.random.seed(42)

n_samples = 1000

data = pd.DataFrame({
    "hemoglobin": np.random.normal(13.5, 2, n_samples),
    "cholesterol": np.random.normal(200, 40, n_samples),
    "glucose": np.random.normal(110, 30, n_samples)
})

# Risk logic
def assign_risk(row):
    if (row["hemoglobin"] < 11 or 
        row["cholesterol"] > 240 or 
        row["glucose"] > 140):
        return 1
    return 0

data["risk"] = data.apply(assign_risk, axis=1)

# Clean values
data["hemoglobin"] = data["hemoglobin"].clip(5, 20)
data["cholesterol"] = data["cholesterol"].clip(100, 400)
data["glucose"] = data["glucose"].clip(60, 300)

X = data[["hemoglobin", "cholesterol", "glucose"]]
y = data["risk"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

os.makedirs("Backend/Models", exist_ok=True)

with open("Backend/Models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained & saved!")