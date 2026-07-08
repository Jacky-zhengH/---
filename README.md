# Remote Sensing Detection Postprocess

This module is responsible for postprocessing tile-level object detection
predictions into final COCO detection JSON files for submission.

It does not handle model training, TensorRT deployment, or image tiling.

## Stage 1 Goal

The first stage uses demo data to run a minimal closed loop:

1. Load `demo_predictions.json`.
2. Normalize prediction dicts in a simple JSON format.
3. Restore tile coordinates to original image coordinates.
4. Run class-wise global NMS by `image_id` and `category_id`.
5. Convert predictions to COCO detection JSON.
6. Provide visualization utilities.
7. Validate core logic with pytest.

## Input Prediction Format

Predictions are JSON lists. Each item uses tile coordinates in `xyxy` format:

```json
{
  "tile_name": "image001_x0_y0.jpg",
  "category_id": 1,
  "score": 0.9,
  "bbox_xyxy": [100, 100, 200, 200]
}
```

Internal IoU and NMS use `bbox_xyxy`. COCO export converts boxes to `xywh`.

## tile_info.json Format

```json
{
  "image001_x0_y0.jpg": {
    "origin_image": "image001.jpg",
    "image_id": 1,
    "x_offset": 0,
    "y_offset": 0,
    "origin_width": 10000,
    "origin_height": 10000
  }
}
```

`x_offset` and `y_offset` are added to tile-level boxes. Restored boxes are
clipped to `origin_width` and `origin_height`.

## COCO Detection Output

The final output is a JSON list in COCO detection result format:

```json
[
  {
    "image_id": 1,
    "category_id": 1,
    "bbox": [100, 100, 100, 100],
    "score": 0.9
  }
]
```

`bbox` must be `[x, y, width, height]` in original image pixel coordinates.
It must not be normalized, and `width` / `height` must be greater than 0.

## Configuration

Key settings live in `config.yaml`:

- input prediction format: `xyxy`
- coordinate system: `tile`
- confidence threshold: `conf_thres`
- NMS IoU threshold: `nms_iou_thres`
- class-wise NMS switch: `class_wise_nms`
- area filter switch and min/max area
- aspect ratio filter switch and min/max ratio
- COCO output path
- visualization output directory

## Run Tests

```bash
pip install -r requirements.txt
pytest -q
```

Run from the `postprocess` directory.

## Later Extensions

- `evaluate_results.py`: Recall, FP, FN, and false-alarm-rate evaluation.
- `sweep_thresholds.py`: confidence and NMS threshold search.
- `reduce_false_alarm.py`: false alarm reduction strategies.

This module should stay focused on postprocessing and final submission
generation. Do not add training code, TensorRT code, or data download logic.

# 遥感目标检测后处理模块

本模块用于光学遥感卫星陆上目标检测比赛的后处理与最终提交结果生成。
它的输入是模型在 tile 小图上的检测预测结果，输出是可提交的 COCO
detection JSON。

本模块不负责模型训练、不负责 TensorRT 部署、不负责图像切片，也不下载
比赛数据。

## 第一阶段目标

当前阶段先使用模拟数据跑通最小闭环：

1. 读取 `demo_predictions.json`。
2. 统一预测结果格式。
3. 将 tile 坐标还原到原始大图坐标。
4. 按 `image_id + category_id` 做 class-wise global NMS。
5. 转换为 COCO detection JSON。
6. 提供 OpenCV 可视化函数。
7. 使用 pytest 验证核心逻辑。

## 输入预测格式

预测文件是 JSON list，每个预测框使用 tile 坐标系下的 `xyxy` 格式：

```json
{
  "tile_name": "image001_x0_y0.jpg",
  "category_id": 1,
  "score": 0.9,
  "bbox_xyxy": [100, 100, 200, 200]
}
```

内部 IoU 和 NMS 都使用 `bbox_xyxy`。只有在导出 COCO JSON 时，才会把
框转换成 `[x, y, width, height]`。

## tile_info.json 格式

`tile_info.json` 用于说明每个 tile 在原始大图中的偏移量和对应图像信息：

```json
{
  "image001_x0_y0.jpg": {
    "origin_image": "image001.jpg",
    "image_id": 1,
    "x_offset": 0,
    "y_offset": 0,
    "origin_width": 10000,
    "origin_height": 10000
  }
}
```

坐标还原时会对 `bbox_xyxy` 加上 `x_offset` 和 `y_offset`，并裁剪到
`origin_width` / `origin_height` 范围内。

## COCO 输出格式

最终提交结果是 COCO detection result 格式：

```json
[
  {
    "image_id": 1,
    "category_id": 1,
    "bbox": [100, 100, 100, 100],
    "score": 0.9
  }
]
```

注意：

- `bbox` 必须是 `[x, y, width, height]`。
- 坐标必须是原始大图像素坐标。
- 坐标不能是归一化坐标。
- `width` 和 `height` 必须大于 0。

## 核心文件说明

- `utils_bbox.py`：bbox 格式转换、裁剪、面积、长宽比和无效框过滤。
- `nms.py`：IoU、基础 NMS、按类别 NMS。
- `load_predictions.py`：JSON 读取和保存，当前只支持 demo JSON。
- `restore_coords.py`：将 tile 坐标还原为原始大图坐标。
- `global_nms.py`：按 `image_id + category_id` 分组执行全局 NMS。
- `convert_to_coco.py`：转换并保存 COCO detection JSON。
- `visualize_results.py`：使用 OpenCV 绘制检测框、类别和分数。
- `evaluate_results.py`：后续评估逻辑占位。
- `sweep_thresholds.py`：后续阈值搜索逻辑占位。

## 运行测试

请在 `postprocess` 目录下运行：

```bash
pip install -r requirements.txt
pytest -q
```

## 后续扩展

- `evaluate_results.py`：用于 Recall、FP、FN、虚警率评估。
- `sweep_thresholds.py`：用于置信度阈值和 NMS 阈值搜索。
- `reduce_false_alarm.py`：用于后续虚警抑制策略。

本模块应保持职责清晰，只处理预测结果后处理和最终提交 JSON 生成。
