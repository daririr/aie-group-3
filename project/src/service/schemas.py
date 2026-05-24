from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    X1: float = Field(..., description="Relative Compactness")
    X2: float = Field(..., description="Surface Area")
    X3: float = Field(..., description="Wall Area")
    X4: float = Field(..., description="Roof Area")
    X5: float = Field(..., description="Overall Height")
    X6: int = Field(..., description="Orientation (2, 3, 4, 5)")
    X7: float = Field(..., description="Glazing Area")
    X8: int = Field(..., description="Glazing Area Distribution (1-5)")


class PredictionResponse(BaseModel):
    heating_load: float
    cooling_load: float
    risk_level: str
    recommendations: list[str]
    top_factors: list[str]
