from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schemas import RecommendationResponse
from app.model import FashionRecommender

app = FastAPI(
    title="Fashion Recommendation API",
    description="MLOps Demo for Fashion Recommendations",
    version="1.0.0"
)

# Initialize the mock ML model logic
recommender = FashionRecommender()

@app.get("/")
def read_root():
    return {"message": "Fashion Recommendation API is running. Check /docs for interactive testing."}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(file: UploadFile = File(...)):
    """
    Upload an image of clothing, and receive fashion recommendations.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
    
    # Read the file contents. In production, consider limits on file size.
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        recommendations = recommender.predict(contents)
    except ValueError as val_e:
         raise HTTPException(status_code=400, detail=str(val_e))
        
    return RecommendationResponse(
        items=recommendations,
        message="Recommendations generated successfully!"
    )
