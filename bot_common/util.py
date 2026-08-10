import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).parent
COMMON_DATA_DIR = PACKAGE_ROOT / "data"


def _load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json(filename: str):
    """Bot側のJSONを読み込む"""
    return _load_json(Path(filename))


def load_common_json(filename: str):
    """共通パッケージのJSONを読み込む"""
    return _load_json(COMMON_DATA_DIR / filename)