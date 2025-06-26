from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import google.generativeai as genai
from fastapi.responses import JSONResponse
import io

app = FastAPI()

# Optional: Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API key setup
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-2.0-flash-lite")

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        prompt = "What is this food? Give the food name only also Give me the calories per 100g with carbs, fiber, protein, also high or low sugar level in json format"

        response = model.generate_content([image, prompt])
        return {"result": response.text.strip()}

    except Exception as e:
        # This will help you debug errors properly in Postman
        return JSONResponse(status_code=500, content={"error": str(e)})
