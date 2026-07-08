from src.convert_to_coco import convert_predictions_to_coco


def test_convert_predictions_to_coco_uses_xywh_and_positive_size():
    predictions = [
        {
            "image_id": 1,
            "category_id": 1,
            "score": 0.90,
            "bbox_xyxy": [100, 120, 220, 260],
        },
        {
            "image_id": 1,
            "category_id": 1,
            "score": 0.50,
            "bbox_xyxy": [10, 10, 10, 20],
        },
    ]

    coco = convert_predictions_to_coco(predictions)

    assert coco == [
        {
            "image_id": 1,
            "category_id": 1,
            "bbox": [100, 120, 120, 140],
            "score": 0.90,
        }
    ]
    assert coco[0]["bbox"][2] > 0
    assert coco[0]["bbox"][3] > 0
