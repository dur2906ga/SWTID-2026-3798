import os
import google.generativeai as genai
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY: genai.configure(api_key=API_KEY)

def generate_nutrition_tip_with_flash(goal):
    if not API_KEY:
        tips = {"weight loss":"Prioritize protein and vegetables, stay hydrated, and choose mostly minimally processed foods.","muscle gain":"Include a protein source in each meal and support training with balanced carbohydrates and adequate hydration.","general wellness":"Build meals around vegetables, protein, whole grains or other high-fiber foods, and stay consistently hydrated.","flexibility":"Support recovery with balanced meals, adequate hydration, and regular nutrient-dense foods."}
        return tips.get(goal.lower(), "Choose balanced meals with protein, vegetables, whole foods, and adequate hydration.")
    return genai.GenerativeModel("gemini-1.5-flash").generate_content(f"Give one concise, practical nutrition or recovery tip for the fitness goal: {goal}. Keep it 2-4 sentences and avoid medical claims.").text
