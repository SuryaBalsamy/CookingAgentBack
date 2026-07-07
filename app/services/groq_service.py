import os
import json
from groq import Groq
from app.services.ai_service import AIService
from dotenv import load_dotenv

load_dotenv()

class GroqService(AIService):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def analyze_ingredients(self, ingredients: list[str], desired_dish: str = None) -> dict:
        ingredients_str = ", ".join(ingredients)
        
        system_prompt = """You are a master chef AI. Return your response ONLY as a valid JSON object. Do not include markdown formatting like ```json.
Expected JSON format:
{
  "recipes": [
    {
      "id": "unique-slug-name",
      "name": "Recipe Name",
      "description": "Short appetizing description (2-4 words)",
      "time": "e.g. 20 mins",
      "thumbnail": "emojis representing the dish",
      "ingredients": {
        "available": ["Available item 1", "Available item 2"],
        "needToBuy": ["Missing item 1", "Missing item 2"]
      },
      "steps": ["Step 1", "Step 2", "Step 3"]
    }
  ]
}
"""
        
        if desired_dish:
            user_prompt = f"""
Available Ingredients: {ingredients_str}
Desired Dish: {desired_dish}

Return the requested dish as a detailed recipe object in the array. You can also provide 1 or 2 alternative similar recipes if appropriate.
Compare the available ingredients with the requested recipe.
Return the available ingredients and what needs to be bought.
Provide concise cooking steps.
"""
        else:
            user_prompt = f"""
Available Ingredients: {ingredients_str}

Suggest 3 completely different and delicious recipes that can be made STRICTLY USING ONLY the available ingredients provided above.
DO NOT suggest any recipe that requires ingredients not listed in the available ingredients. 
The "needToBuy" array for every single suggested recipe MUST BE EMPTY ([]). You are only allowed to use ingredients the user already has.
Provide concise cooking steps.
"""

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )
        
        text_response = response.choices[0].message.content.strip()
        
        # Clean up potential markdown formatting from LLM
        if text_response.startswith("```"):
            first_newline = text_response.find("\n")
            if first_newline != -1:
                text_response = text_response[first_newline:].strip()
            else:
                text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        if text_response.endswith("```"):
            text_response = text_response[:-3].strip()
            
        try:
            return json.loads(text_response)
        except json.JSONDecodeError:
            print(f"FAILED TO PARSE JSON. RAW RESPONSE: {response.choices[0].message.content}")
            raise Exception("Failed to parse AI response into JSON")
