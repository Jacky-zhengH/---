"""中文说明：预测结果可视化。

本文件使用 OpenCV 在图像上绘制 bbox_xyxy、category_id 和 score。
如果输入图片不存在或 OpenCV 读取失败，会抛出清晰异常，避免静默失败。
"""

from pathlib import Path

import cv2


def draw_predictions(image_path, predictions, output_path):
    """Draw xyxy predictions on an image."""
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Failed to read image with OpenCV: {image_path}")

    for pred in predictions:
        x1, y1, x2, y2 = [int(round(v)) for v in pred["bbox_xyxy"]]
        category_id = pred.get("category_id", "unknown")
        score = pred.get("score", 0)
        label = f"{category_id}: {score:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            label,
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(output_path), image)
    if not ok:
        raise ValueError(f"Failed to write visualization image: {output_path}")
    return str(output_path)
