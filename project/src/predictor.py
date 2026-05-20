import pandas as pd
import logging
from .model_loader import ModelRegistry

logger = logging.getLogger(__name__)


class CoolingPredictor:
    """Обёртка над моделями для предсказания, оценки риска и генерации рекомендаций."""

    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.targets = registry.manifest["targets"]

    def predict(self, input_data: dict) -> dict:
        df_input = pd.DataFrame([input_data])
        predictions = {}
        for target in self.targets:
            model = self.registry.get_model(target)
            predictions[target] = float(model.predict(df_input)[0])

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

    @staticmethod
    def _calculate_risk(cooling_load: float) -> str:
        # Границы определены на основе распределения Y2 в датасете
        if cooling_load < 20.0:
            return "low"
        elif cooling_load <= 35.0:
            return "medium"
        return "high"

    @staticmethod
    def _generate_recommendations(input_data: dict, cooling_load: float) -> list[str]:
        recs = []
        if cooling_load > 35.0:
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

    @staticmethod
    def _get_top_factors(input_data: dict) -> list[str]:
        """
        Возвращает топ-3 фактора, влияющих на прогноз.
        Использует простые эвристики на основе EDA + дефолтные значения для заполнения.
        """
        factors = []

        # Эвристики на основе корреляций из EDA
        if input_data.get("X2", 0.0) > 650.0:  # Surface Area
            factors.append("Surface Area")
        if input_data.get("X5", 0.0) >= 7.0:  # Overall Height
            factors.append("Overall Height")
        if input_data.get("X7", 0.0) > 0.25:  # Glazing Area
            factors.append("Glazing Area")
        if (
            input_data.get("X1", 1.0) < 0.75
        ):  # Relative Compactness (низкая → выше нагрузка)
            factors.append("Relative Compactness")
        if input_data.get("X3", 0.0) > 350.0:  # Wall Area
            factors.append("Wall Area")

        # Дефолтный список признаков, упорядоченный по убыванию средней важности из EDA
        default_factors = [
            "Overall Height",
            "Wall Area",
            "Surface Area",
            "Relative Compactness",
            "Glazing Area",
            "Roof Area",
        ]

        # Добавляем дефолтные факторы, которых ещё нет в списке
        for factor in default_factors:
            if factor not in factors:
                factors.append(factor)
            if len(factors) >= 3:
                break

        return factors[:3]
