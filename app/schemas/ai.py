from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    ingredients: List[str]
    desiredDish: Optional[str] = None

class RecipeIngredientAnalysis(BaseModel):
    available: List[str]
    needToBuy: List[str]

class Recipe(BaseModel):
    id: str
    name: str
    description: str
    time: str
    thumbnail: str
    ingredients: RecipeIngredientAnalysis
    steps: List[str]

class AnalyzeResponse(BaseModel):
    recipes: List[Recipe]
