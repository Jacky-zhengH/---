"""中文说明：基础 NMS 与 IoU 实现。

本文件使用 prediction dict 中的 bbox_xyxy 和 score 进行排序与抑制。
nms_xyxy 处理单组框，class_wise_nms 会按 category_id 分组后分别做 NMS，
保证不同类别之间不会互相抑制。
"""

from collections import defaultdict

from .utils_bbox import box_area_xyxy


def box_iou_xyxy(box_a, box_b):
    """Compute IoU between two xyxy boxes."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_area = box_area_xyxy([inter_x1, inter_y1, inter_x2, inter_y2])
    union_area = box_area_xyxy(box_a) + box_area_xyxy(box_b) - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area


def nms_xyxy(predictions, iou_threshold):
    """Run score-sorted NMS on prediction dicts using bbox_xyxy."""
    sorted_predictions = sorted(
        predictions,
        key=lambda pred: pred.get("score", 0),
        reverse=True,
    )

    kept = []
    for pred in sorted_predictions:
        should_keep = True
        for kept_pred in kept:
            if box_iou_xyxy(pred["bbox_xyxy"], kept_pred["bbox_xyxy"]) > iou_threshold:
                should_keep = False
                break
        if should_keep:
            kept.append(pred)
    return kept


def class_wise_nms(predictions, iou_threshold):
    """Run NMS independently for each category_id."""
    grouped = defaultdict(list)
    for pred in predictions:
        grouped[pred.get("category_id")].append(pred)

    kept = []
    for category_predictions in grouped.values():
        kept.extend(nms_xyxy(category_predictions, iou_threshold))
    return sorted(kept, key=lambda pred: pred.get("score", 0), reverse=True)
