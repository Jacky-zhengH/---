"""中文说明：预测结果 JSON 读写入口。

当前第一阶段只支持统一 JSON 格式的 demo predictions，不接入 YOLO、
TensorRT 或真实模型输出。save_json 会自动创建输出目录。
"""

import json
from pathlib import Path


def load_json(path):
    """Load a JSON file."""
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    """Save JSON data, creating parent directories when needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_demo_predictions(path):
    """Load demo predictions from JSON.

    First-stage postprocessing only supports the unified JSON prediction
    format, not YOLO/TensorRT/model-native outputs.
    """
    data = load_json(path)
    if not isinstance(data, list):
        raise ValueError("Demo predictions JSON must be a list of prediction dicts.")
    return data
