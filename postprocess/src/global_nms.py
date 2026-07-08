"""中文说明：全局 NMS 入口。

本文件先按原始大图 image_id 分组，再按 category_id 分组，对每组执行
nms_xyxy。它用于把多个 tile 的预测结果合并后去除同图同类重复框。
"""

from collections import defaultdict

from .nms import nms_xyxy


def global_nms(predictions, iou_threshold):
    """Run NMS per original image and category."""
    grouped = defaultdict(list)
    for pred in predictions:
        key = (pred.get("image_id"), pred.get("category_id"))
        grouped[key].append(pred)

    kept = []
    for group_predictions in grouped.values():
        kept.extend(nms_xyxy(group_predictions, iou_threshold))
    return sorted(kept, key=lambda pred: pred.get("score", 0), reverse=True)
