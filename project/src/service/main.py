import time
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..config import load_yaml, ARTIFACTS_DIR
from ..utils.logging import setup_logger
from ..models.registry import ModelRegistry
from ..models.predictor import CoolingPredictor

LOG_PATH = ARTIFACTS_DIR / "logs" / "service.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logger = setup_logger(str(LOG_PATH), name="service")


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting model initialization...")
    try:
        app.state.registry = ModelRegistry()
        app.state.predictor = CoolingPredictor(app.state.registry)
        logger.info("Model loaded successfully. Service ready.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    yield
    logger.info("Shutting down service...")


app = FastAPI(
    title="Cooling Load Predictor API",
    version="0.1.0",
    lifespan=lifespan,
    description="API for predicting heating and cooling loads in buildings",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        start_time = time.time()
        result = app.state.predictor.predict(request.model_dump())
        latency = round(time.time() - start_time, 4)
        logger.info(
            f"Prediction completed in {latency}s | Y2={result['cooling_load']} | Risk={result['risk_level']}"
        )
        return PredictionResponse(**result)
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal prediction error")


@app.get("/info")
def get_model_info():
    return {
        "model": app.state.registry.manifest["model_name"],
        "targets": app.state.registry.manifest["targets"],
        "artifacts_dir": str(ARTIFACTS_DIR),
    }
