import pytest
from pathlib import Path
from src.config import load_yaml, DATA_DIR


def test_config_loads():
    """data.yaml должен загружаться корректно."""
    cfg = load_yaml("data.yaml")
    assert "source_path" in cfg
    assert "columns" in cfg
    assert "separator" in cfg
    assert cfg["separator"] == ";"


def test_data_paths_exist():
    """Папка data должна существовать и содержать CSV."""
    assert DATA_DIR.exists(), f"Папка data не найдена: {DATA_DIR}"
    csv_files = list(DATA_DIR.glob("*.csv"))
    assert len(csv_files) > 0, "CSV файлы в data/ отсутствуют"


def test_data_columns_match_config():
    """Колонки в CSV должны соответствовать конфигу."""
    import pandas as pd

    cfg = load_yaml("data.yaml")
    filename = Path(cfg["source_path"]).name
    data_path = DATA_DIR / filename

    if not data_path.exists():
        pytest.skip(f"Файл {data_path} не найден")

    df = pd.read_csv(data_path, sep=cfg["separator"], decimal=cfg["decimal"])

    all_cols = set(df.columns)
    expected_cols = (
        set(cfg["columns"]["numeric"])
        | set(cfg["columns"]["categorical"])
        | set(cfg["columns"]["targets"])
    )
    assert expected_cols.issubset(
        all_cols
    ), f"Не хватает колонок: {expected_cols - all_cols}"


def test_data_no_missing_values():
    """Данные не должны иметь пропусков (после dropna)."""
    import pandas as pd

    cfg = load_yaml("data.yaml")
    filename = Path(cfg["source_path"]).name
    data_path = DATA_DIR / filename

    if not data_path.exists():
        pytest.skip(f"Файл {data_path} не найден")

    df = pd.read_csv(data_path, sep=cfg["separator"], decimal=cfg["decimal"])
    df_clean = df.dropna(how=cfg["dropna_how"])

    assert len(df_clean) > 0, "Все данные удалены из-за пропусков"
