import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import io

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def process_image_with_vlm(img_path: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """Describe this automotive diagram/image in detail for service manual search. 
    Include technical details, labels, measurements, and context for mechanics."""
    
    img = Image.open(img_path)
    
    response = model.generate_content([prompt, img])
    return response.text