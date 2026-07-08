# Project Instructions for Codex

This repository contains the post-processing module for an optical remote sensing object detection competition.

The goal of this module is to convert model predictions on image tiles into final submission-ready COCO JSON results.

Core workflow:
1. Load raw model predictions.
2. Standardize bbox format to xyxy.
3. Restore tile-local coordinates to original large-image coordinates.
4. Apply class-wise global NMS.
5. Reduce false alarms with configurable thresholds and filters.
6. Convert final predictions to COCO detection JSON.
7. Generate visualization images for checking and reporting.
8. Provide simple evaluation utilities for Recall, FP, FN, and false alarm rate.

Coding rules:
- Use Python 3.
- Keep code simple, readable, and modular.
- Avoid over-engineering.
- Do not depend on a real model or real dataset yet.
- Use demo data and unit tests to verify the pipeline.
- All bbox operations should clearly state whether the format is xyxy or xywh.
- COCO output bbox must be [x, y, width, height] in original image pixel coordinates.
- Keep parameters in config.yaml instead of hardcoding thresholds.
- Add comments for non-trivial coordinate transformations.
- Provide tests for bbox conversion, IoU/NMS, coordinate restoration, and COCO output.