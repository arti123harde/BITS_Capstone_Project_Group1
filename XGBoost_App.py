import streamlit as st
import pandas as pd
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# ---------------- Custom Transformer ----------------
class YearTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, min_year=1997, max_year=2020):
        self.min_year = min_year
        self.max_year = max_year

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_ = X.copy()
        X_['year'] = (X_['year'].astype(int) - self.min_year) / (self.max_year - self.min_year)
        return X_

        
# ---------------- Load trained XGBoost pipeline ----------------
with open("best_model_XGBoost.pkl", "rb") as f:
    model_pipeline = pickle.load(f)

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 32px; font-weight: 800; color: #15803d; margin-bottom: 20px; }
    .result-box { background-color: #ecfdf5; border: 2px solid #16a34a; color: #065f46;
                  padding: 20px; border-radius: 12px; text-align: center; font-size: 22px;
                  font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 25px; }
    div.stButton > button:first-child { background-color: #16a34a; color: white; border: none;
                                        padding: 10px 24px; border-radius: 8px; font-size: 18px; font-weight: 600; }
    div.stButton > button:hover { background-color: #15803d; transform: scale(1.05); }
    .stSubheader { color: #065f46 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown('<div class="main-title">🌾 Crop Yield Prediction App</div>', unsafe_allow_html=True)
st.write("Enter the real values for your crop and environmental parameters. The pipeline will handle scaling and encoding automatically.")

# ---------------- Dropdown Options ----------------
crop_options = [
    'arecanut', 'arhar/tur', 'castor seed', 'coconut', 'cotton(lint)',
    'dry chillies', 'gram', 'jute', 'linseed', 'maize', 'mesta',
    'niger seed', 'onion', 'other  rabi pulses', 'potato',
    'rapeseed &mustard', 'rice', 'sesamum', 'small millets',
    'sugarcane', 'sweet potato', 'tapioca', 'tobacco', 'turmeric',
    'wheat', 'bajra', 'black pepper', 'cardamom', 'coriander',
    'garlic', 'ginger', 'groundnut', 'horse-gram', 'jowar', 'ragi',
    'cashewnut', 'banana', 'soyabean', 'barley', 'khesari', 'masoor',
    'moong(green gram)', 'other kharif pulses', 'safflower',
    'sannhamp', 'sunflower', 'urad', 'peas & beans (pulses)',
    'other oilseeds', 'other cereals', 'cowpea(lobia)',
    'oilseeds total', 'guar seed', 'other summer pulses', 'moth'
]

state_options = [
    'assam', 'karnataka', 'kerala', 'meghalaya', 'west bengal',
    'puducherry', 'goa', 'andhra pradesh', 'tamil nadu', 'odisha',
    'bihar', 'gujarat', 'madhya pradesh', 'maharashtra', 'mizoram',
    'punjab', 'uttar pradesh', 'haryana', 'himachal pradesh',
    'tripura', 'nagaland', 'chhattisgarh', 'uttarakhand', 'jharkhand',
    'delhi', 'manipur', 'jammu and kashmir', 'telangana',
    'arunachal pradesh', 'sikkim'
]

season_options = ["autumn", "kharif", "rabi", "summer", "whole year", "winter"]

# ---------------- Input Fields ----------------
col1, col2 = st.columns(2)
with col1:
    crop_name = st.selectbox("Crop", sorted(crop_options))
with col2:
    state_name = st.selectbox("State", sorted(state_options))

col1, col2, col3 = st.columns(3)
with col1:
    area = st.number_input("Area (hectares)", min_value=0.0)
with col2:
    fertilizer = st.number_input("Fertilizer (kg/ha)", min_value=0.0)
with col3:
    pesticide = st.number_input("Pesticide (kg/ha)", min_value=0.0)

col1, col2, col3 = st.columns(3)
with col1:
    avg_temp_c = st.number_input("Average Temperature (°C)")
with col2:
    total_rainfall_mm = st.number_input("Total Rainfall (mm)")
with col3:
    avg_humidity_percent = st.number_input("Average Humidity (%)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    n = st.number_input("Nitrogen (N kg/ha)")
with col2:
    p = st.number_input("Phosphorus (P kg/ha)")
with col3:
    k = st.number_input("Potassium (K kg/ha)")
with col4:
    ph = st.number_input("Soil pH")

col1, col2 = st.columns(2)
with col1:
    season = st.selectbox("Season", season_options)
with col2:
    year = st.number_input("Year", min_value=1997, max_value=2025, value=2020, step=1)

# ---------------- Create Input DataFrame ----------------
input_data = pd.DataFrame([{
    'crop': crop_name,
    'state': state_name,
    'season': season,
    'year': year,
    'area': area,
    'fertilizer': fertilizer,
    'pesticide': pesticide,
    'avg_temp_c': avg_temp_c,
    'total_rainfall_mm': total_rainfall_mm,
    'avg_humidity_percent': avg_humidity_percent,
    'n': n,
    'p': p,
    'k': k,
    'ph': ph
}])

# ---------------- Input Data Preview ----------------
st.subheader("📋 Input Data Preview")
st.dataframe(input_data, use_container_width=True)

# ---------------- Prediction ----------------
if st.button("🔍 Predict Crop Yield"):
    try:
        prediction = model_pipeline.predict(input_data)
        st.markdown(f"""
            <div class="result-box">
                🌱 Predicted Crop Yield: <br> <strong>{prediction[0]:.2f} q/ha</strong>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")