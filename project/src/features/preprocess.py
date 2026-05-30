from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from ..config import load_yaml


def build_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    cfg = load_yaml("experiment.yaml")
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            (
                "cat",
                OneHotEncoder(
                    handle_unknown=cfg["preprocessing"]["handle_unknown"],
                    sparse_output=False,
                ),
                cat_cols,
            ),
        ]
    )
