from src.utils_bbox import (
    aspect_ratio_xyxy,
    box_area_xyxy,
    clip_box_xyxy,
    filter_invalid_predictions,
    xywh_to_xyxy,
    xyxy_to_xywh,
)


def test_xyxy_to_xywh():
    assert xyxy_to_xywh([10, 20, 30, 50]) == [10, 20, 20, 30]


def test_xywh_to_xyxy():
    assert xywh_to_xyxy([10, 20, 20, 30]) == [10, 20, 30, 50]


def test_clip_box_xyxy():
    assert clip_box_xyxy([-10, 5, 120, 80], width=100, height=60) == [0, 5, 100, 60]


def test_box_area_and_aspect_ratio():
    box = [10, 20, 30, 60]
    assert box_area_xyxy(box) == 800
    assert aspect_ratio_xyxy(box) == 0.5


def test_filter_invalid_predictions():
    predictions = [
        {"bbox_xyxy": [0, 0, 10, 10]},
        {"bbox_xyxy": [0, 0, 0, 10]},
        {"bbox_xyxy": [0, 0, 10]},
        {},
    ]
    assert filter_invalid_predictions(predictions) == [{"bbox_xyxy": [0, 0, 10, 10]}]
from src.utils_bbox import (
    aspect_ratio_xyxy,
    box_area_xyxy,
    clip_box_xyxy,
    filter_invalid_predictions,
    xywh_to_xyxy,
    xyxy_to_xywh,
)


def test_xyxy_to_xywh():
    assert xyxy_to_xywh([10, 20, 30, 50]) == [10, 20, 20, 30]


def test_xywh_to_xyxy():
    assert xywh_to_xyxy([10, 20, 20, 30]) == [10, 20, 30, 50]


def test_clip_box_xyxy():
    assert clip_box_xyxy([-10, 5, 120, 80], width=100, height=60) == [0, 5, 100, 60]


def test_box_area_and_aspect_ratio():
    box = [10, 20, 30, 60]
    assert box_area_xyxy(box) == 800
    assert aspect_ratio_xyxy(box) == 0.5


def test_filter_invalid_predictions():
    predictions = [
        {"bbox_xyxy": [0, 0, 10, 10]},
        {"bbox_xyxy": [0, 0, 0, 10]},
        {"bbox_xyxy": [0, 0, 10]},
        {},
    ]
    assert filter_invalid_predictions(predictions) == [{"bbox_xyxy": [0, 0, 10, 10]}]
