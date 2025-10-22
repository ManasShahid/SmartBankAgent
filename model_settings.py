# model_settings.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define model settings
model_config = {
    "temperature": 1,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 5000,
}

# Load the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=model_config,
)
