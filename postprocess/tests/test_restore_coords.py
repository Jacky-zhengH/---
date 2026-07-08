from src.restore_coords import restore_tile_predictions


def test_restore_tile_predictions_adds_offsets_and_metadata():
    predictions = [
        {
            "tile_name": "image001_x512_y256.jpg",
            "category_id": 1,
            "score": 0.90,
            "bbox_xyxy": [10, 20, 110, 220],
        }
    ]
    tile_info = {
        "image001_x512_y256.jpg": {
            "origin_image": "image001.jpg",
            "image_id": 1,
            "x_offset": 512,
            "y_offset": 256,
            "origin_width": 10000,
            "origin_height": 10000,
        }
    }

    restored = restore_tile_predictions(predictions, tile_info)

    assert restored[0]["bbox_xyxy"] == [522, 276, 622, 476]
    assert restored[0]["image_id"] == 1
    assert restored[0]["origin_image"] == "image001.jpg"


def test_restore_tile_predictions_clips_to_origin_size():
    predictions = [
        {
            "tile_name": "tile.jpg",
            "category_id": 1,
            "score": 0.90,
            "bbox_xyxy": [90, 90, 200, 200],
        }
    ]
    tile_info = {
        "tile.jpg": {
            "origin_image": "image001.jpg",
            "image_id": 1,
            "x_offset": 0,
            "y_offset": 0,
            "origin_width": 100,
            "origin_height": 120,
        }
    }

    restored = restore_tile_predictions(predictions, tile_info)

    assert restored[0]["bbox_xyxy"] == [90, 90, 100, 120]
from src.restore_coords import restore_tile_predictions


def test_restore_tile_predictions_adds_offsets_and_metadata():
    predictions = [
        {
            "tile_name": "image001_x512_y256.jpg",
            "category_id": 1,
            "score": 0.90,
            "bbox_xyxy": [10, 20, 110, 220],
        }
    ]
    tile_info = {
        "image001_x512_y256.jpg": {
            "origin_image": "image001.jpg",
            "image_id": 1,
            "x_offset": 512,
            "y_offset": 256,
            "origin_width": 10000,
            "origin_height": 10000,
        }
    }

    restored = restore_tile_predictions(predictions, tile_info)

    assert restored[0]["bbox_xyxy"] == [522, 276, 622, 476]
    assert restored[0]["image_id"] == 1
    assert restored[0]["origin_image"] == "image001.jpg"


def test_restore_tile_predictions_clips_to_origin_size():
    predictions = [
        {
            "tile_name": "tile.jpg",
            "category_id": 1,
            "score": 0.90,
            "bbox_xyxy": [90, 90, 200, 200],
        }
    ]
    tile_info = {
        "tile.jpg": {
            "origin_image": "image001.jpg",
            "image_id": 1,
            "x_offset": 0,
            "y_offset": 0,
            "origin_width": 100,
            "origin_height": 120,
        }
    }

    restored = restore_tile_predictions(predictions, tile_info)

    assert restored[0]["bbox_xyxy"] == [90, 90, 100, 120]
