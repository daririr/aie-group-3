import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_input():
    """Типичный вход для предсказания."""
    return {
        "X1": 0.82,
        "X2": 612.5,
        "X3": 318.5,
        "X4": 147.0,
        "X5": 7.0,
        "X6": 2,
        "X7": 0.1,
        "X8": 1,
    }
