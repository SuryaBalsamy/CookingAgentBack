import os
from fastapi import APIRouter, Depends, HTTPException, Header
from jose import JWTError, jwt
from app.schemas.ai import AnalyzeRequest, AnalyzeResponse
from app.services.gemini import GeminiService

router = APIRouter(prefix="/analyze", tags=["ai"])

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return email

@router.post("", response_model=AnalyzeResponse)
def analyze_ingredients(request: AnalyzeRequest, email: str = Depends(verify_token)):
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="Ingredients list cannot be empty")
        
    try:
        try:
            # Try Gemini First
            ai_service = GeminiService()
            return ai_service.analyze_ingredients(request.ingredients, request.desiredDish)
        except Exception as e:
            print(f"Gemini failed: {str(e)}. Falling back to Groq...")
            
            # Fallback to Groq
            from app.services.groq_service import GroqService
            fallback_service = GroqService()
            return fallback_service.analyze_ingredients(request.ingredients, request.desiredDish)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
