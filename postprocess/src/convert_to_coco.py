"""中文说明：内部预测格式转换为 COCO detection JSON。

本文件把恢复到原图坐标的 bbox_xyxy 转换为 COCO 要求的 [x, y, w, h]。
宽高小于等于 0 的无效框会被跳过，输出坐标保持原始像素坐标，不做归一化。
"""

from .load_predictions import save_json
from .utils_bbox import xyxy_to_xywh


def convert_predictions_to_coco(predictions):
    """Convert internal prediction dicts to COCO detection result format."""
    coco_results = []
    for pred in predictions:
        bbox_xywh = xyxy_to_xywh(pred["bbox_xyxy"])
        if bbox_xywh[2] <= 0 or bbox_xywh[3] <= 0:
            continue
        coco_results.append(
            {
                "image_id": pred["image_id"],
                "category_id": pred["category_id"],
                "bbox": bbox_xywh,
                "score": pred["score"],
            }
        )
    return coco_results


def save_coco_json(predictions, output_path):
    """Save predictions in COCO detection JSON format."""
    coco_results = convert_predictions_to_coco(predictions)
    save_json(coco_results, output_path)
    return coco_results
