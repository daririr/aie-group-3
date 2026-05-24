import pandas as pd
from .registry import ModelRegistry
from ..config import load_yaml


class CoolingPredictor:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.serving_cfg = load_yaml("serving.yaml")
        self.targets = registry.manifest["targets"]

    def predict(self, input_data: dict) -> dict:
        df_input = pd.DataFrame([input_data])
        predictions = {}
        for target in self.targets:
            predictions[target] = float(self.registry.predict(target, df_input)[0])

        cooling_load = predictions.get("Y2", 0.0)
        risk_level = self._calculate_risk(cooling_load)
        recommendations = self._generate_recommendations(input_data, cooling_load)
        top_factors = self._get_top_factors(input_data)

        return {
            "heating_load": round(predictions.get("Y1", 0.0), 2),
            "cooling_load": round(cooling_load, 2),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "top_factors": top_factors,
        }

    def _calculate_risk(self, cooling_load: float) -> str:
        thresholds = self.serving_cfg["risk_thresholds"]
        if cooling_load < thresholds["low"]:
            return "low"
        elif cooling_load <= thresholds["medium"]:
            return "medium"
        return "high"

    def _generate_recommendations(
        self, input_data: dict, cooling_load: float
    ) -> list[str]:
        recs = []
        if cooling_load > self.serving_cfg["risk_thresholds"]["medium"]:
            recs.append("Upgrade cooling system capacity to handle peak load")
        if input_data.get("X7", 0.0) > 0.30:
            recs.append(
                "High glazing area detected. Use reflective films or external shading"
            )
        if input_data.get("X1", 1.0) < 0.75:
            recs.append(
                "Low building compactness increases heat exchange. Improve insulation"
            )
        if not recs:
            recs.append("Current configuration is within optimal thermal range")
        return recs

    def _get_top_factors(self, input_data: dict) -> list[str]:
        factors = []
        if input_data.get("X2", 0.0) > 650.0:
            factors.append("Surface Area")
        if input_data.get("X5", 0.0) >= 7.0:
            factors.append("Overall Height")
        if input_data.get("X7", 0.0) > 0.25:
            factors.append("Glazing Area")
        default_factors = [
            "Overall Height",
            "Wall Area",
            "Surface Area",
            "Relative Compactness",
            "Glazing Area",
        ]
        for f in default_factors:
            if f not in factors:
                factors.append(f)
            if len(factors) >= 3:
                break
        return factors[:3]
