from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def analyze_ingredients(self, ingredients: list[str], desired_dish: str = None) -> dict:
        """
        Analyze ingredients and return a structured dictionary containing:
        - possibleRecipes (list)
        - ingredientAnalysis (dict with 'available' and 'needToBuy')
        - steps (list)
        """
        pass
