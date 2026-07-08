"""中文说明：边界框工具函数。

本文件负责 xyxy/xywh 格式转换、边界裁剪、面积计算、长宽比计算，
以及过滤无效预测框。内部 NMS 和 IoU 均使用 xyxy 格式，导出 COCO
结果时再转换为 xywh。
"""


def xyxy_to_xywh(box):
    """Convert [x1, y1, x2, y2] to [x, y, width, height]."""
    x1, y1, x2, y2 = box
    return [x1, y1, x2 - x1, y2 - y1]


def xywh_to_xyxy(box):
    """Convert [x, y, width, height] to [x1, y1, x2, y2]."""
    x, y, width, height = box
    return [x, y, x + width, y + height]


def clip_box_xyxy(box, width, height):
    """Clip an xyxy box to image bounds."""
    x1, y1, x2, y2 = box
    return [
        max(0, min(x1, width)),
        max(0, min(y1, height)),
        max(0, min(x2, width)),
        max(0, min(y2, height)),
    ]


def box_area_xyxy(box):
    """Return area for an xyxy box. Invalid boxes have area 0."""
    x1, y1, x2, y2 = box
    return max(0, x2 - x1) * max(0, y2 - y1)


def aspect_ratio_xyxy(box):
    """Return width / height for an xyxy box."""
    x1, y1, x2, y2 = box
    box_width = x2 - x1
    box_height = y2 - y1
    if box_height <= 0:
        return 0
    return box_width / box_height


def filter_invalid_predictions(predictions):
    """Drop predictions without a valid positive-area bbox_xyxy."""
    valid_predictions = []
    for pred in predictions:
        box = pred.get("bbox_xyxy")
        if box is None or len(box) != 4:
            continue
        if box_area_xyxy(box) <= 0:
            continue
        valid_predictions.append(pred)
    return valid_predictions
