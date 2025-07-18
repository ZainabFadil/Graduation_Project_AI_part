# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ccFRY8RRgqeYZdf-AhyaS5F1EAbtjO-D
"""

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# تحميل الموديل، السكيلر، والانكودرز
model = joblib.load("logistic_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# تعريف FastAPI app
app = FastAPI(title="Startup Success Prediction API")

# تعريف شكل البيانات المطلوبة من اليوزر
class StartupData(BaseModel):
    city: str
    industry: str
    has_online_presence: int
    num_founders: int
    num_employees: int
    got_external_funding: int
    startup_stage: str
    market_competition_level: str
    incubator_support: int
    num_direct_competitors: str
    market_need_level: str
    startup_age: int

@app.post("/predict/")
def predict_startup(data: StartupData):
    # تحويل الداتا لـ DataFrame
    input_data = pd.DataFrame([data.dict()])

    # تطبيق Label Encoding
    for col, le in label_encoders.items():
        input_data[col] = le.transform(input_data[col])

    # Scaling
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # تحويل النتيجة لكلام مفهوم
    result = "Successful ✅" if prediction == 1 else "Unsuccessful ❌"
    return {"prediction": int(prediction), "result": result}

#How to use FASTAPI

"""
🧪 تجربة الـ API محليًا:
بعد حفظ الكود في ملف مثلاً main.py، شغّلي:

uvicorn main:app --reload
ثم افتحي المتصفح على:

http://127.0.0.1:8000/docs
هتلاقي واجهة تفاعلية جميلة تقدري تجربي منها الموديل!
"""

