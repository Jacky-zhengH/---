"""中文说明：tile 坐标还原到原始大图坐标。

本文件根据 tile_info 中的 x_offset/y_offset，把 tile 内 bbox_xyxy 平移到
原图坐标系，同时补充 image_id、origin_image，并裁剪到原图宽高范围内。
"""

from .utils_bbox import clip_box_xyxy


def restore_tile_predictions(predictions, tile_info):
    """Restore tile-coordinate predictions to original image coordinates."""
    restored = []
    for pred in predictions:
        tile_name = pred.get("tile_name")
        if tile_name not in tile_info:
            raise KeyError(f"Missing tile_info for tile_name: {tile_name}")

        info = tile_info[tile_name]
        x_offset = info["x_offset"]
        y_offset = info["y_offset"]
        x1, y1, x2, y2 = pred["bbox_xyxy"]
        restored_box = [
            x1 + x_offset,
            y1 + y_offset,
            x2 + x_offset,
            y2 + y_offset,
        ]
        restored_box = clip_box_xyxy(
            restored_box,
            width=info["origin_width"],
            height=info["origin_height"],
        )

        restored_pred = dict(pred)
        restored_pred["bbox_xyxy"] = restored_box
        restored_pred["image_id"] = info["image_id"]
        restored_pred["origin_image"] = info["origin_image"]
        restored.append(restored_pred)
    return restored
