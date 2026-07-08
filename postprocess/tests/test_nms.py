import pytest

from src.nms import box_iou_xyxy, class_wise_nms, nms_xyxy


def test_box_iou_xyxy():
    iou = box_iou_xyxy([0, 0, 100, 100], [50, 50, 150, 150])
    assert iou == pytest.approx(2500 / 17500)


def test_nms_keeps_high_score_and_removes_overlap_low_score():
    predictions = [
        {"category_id": 1, "score": 0.90, "bbox_xyxy": [0, 0, 100, 100]},
        {"category_id": 1, "score": 0.60, "bbox_xyxy": [10, 10, 110, 110]},
        {"category_id": 1, "score": 0.80, "bbox_xyxy": [200, 200, 300, 300]},
    ]

    kept = nms_xyxy(predictions, iou_threshold=0.45)

    assert len(kept) == 2
    assert kept[0]["score"] == 0.90
    assert {pred["score"] for pred in kept} == {0.90, 0.80}


def test_class_wise_nms_does_not_suppress_other_categories():
    predictions = [
        {"category_id": 1, "score": 0.90, "bbox_xyxy": [0, 0, 100, 100]},
        {"category_id": 2, "score": 0.60, "bbox_xyxy": [10, 10, 110, 110]},
    ]

    kept = class_wise_nms(predictions, iou_threshold=0.45)

    assert len(kept) == 2
import pytest

from src.nms import box_iou_xyxy, class_wise_nms, nms_xyxy


def test_box_iou_xyxy():
    iou = box_iou_xyxy([0, 0, 100, 100], [50, 50, 150, 150])
    assert iou == pytest.approx(2500 / 17500)


def test_nms_keeps_high_score_and_removes_overlap_low_score():
    predictions = [
        {"category_id": 1, "score": 0.90, "bbox_xyxy": [0, 0, 100, 100]},
        {"category_id": 1, "score": 0.60, "bbox_xyxy": [10, 10, 110, 110]},
        {"category_id": 1, "score": 0.80, "bbox_xyxy": [200, 200, 300, 300]},
    ]

    kept = nms_xyxy(predictions, iou_threshold=0.45)

    assert len(kept) == 2
    assert kept[0]["score"] == 0.90
    assert {pred["score"] for pred in kept} == {0.90, 0.80}


def test_class_wise_nms_does_not_suppress_other_categories():
    predictions = [
        {"category_id": 1, "score": 0.90, "bbox_xyxy": [0, 0, 100, 100]},
        {"category_id": 2, "score": 0.60, "bbox_xyxy": [10, 10, 110, 110]},
    ]

    kept = class_wise_nms(predictions, iou_threshold=0.45)

    assert len(kept) == 2
