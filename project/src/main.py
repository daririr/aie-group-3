import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import ARTIFACTS_DIR
from .model_loader import ModelRegistry
from .predictor import CoolingPredictor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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
    app.state.registry = ModelRegistry()
    app.state.predictor = CoolingPredictor(app.state.registry)
    logger.info("Model loaded successfully. Service ready.")
    yield
    logger.info("Shutting down service...")


app = FastAPI(
    title="Cooling Load Predictor API",
    version="0.1.0",
    lifespan=lifespan,
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
        logger.info("Prediction completed in %s seconds", latency)
        return PredictionResponse(**result)
    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal prediction error")


@app.get("/info")
def get_model_info():
    return {
        "model": app.state.registry.manifest["model_name"],
        "features": app.state.registry.manifest.get("features", {}),
        "artifacts_dir": str(ARTIFACTS_DIR),
    }
