
"""Unit and model-level tests for image preprocessing and prediction."""

import numpy as np
import pytest

from model import preprocess_img, predict_result


def test_preprocess_img():
    """Verify preprocessing produces correctly shaped, normalized data."""

    # ARRANGE
    img_path = "test_images/2/Sign 2 (97).jpeg"

    # ACT
    processed_img = preprocess_img(img_path)

    # ASSERT
    assert processed_img.shape == (1, 224, 224, 3)
    assert np.min(processed_img) >= 0
    assert np.max(processed_img) <= 1


def test_predict_result():
    """Verify that the model returns an integer class index."""

    # ARRANGE
    img_path = "test_images/4/Sign 4 (92).jpeg"
    processed_img = preprocess_img(img_path)

    # ACT
    prediction = predict_result(processed_img)

    # ASSERT
    assert isinstance(prediction, (int, np.integer))
    assert 0 <= prediction <= 9


def test_invalid_image_path():
    """Verify preprocessing rejects a nonexistent image path."""

    # ACT / ASSERT
    with pytest.raises(FileNotFoundError):
        preprocess_img("invalid/path/to/image.jpeg")


def test_model_predictions_consistency():
    """Verify identical inputs produce identical predictions."""

    # ARRANGE
    img_path = "test_images/7/Sign 7 (54).jpeg"
    processed_img = preprocess_img(img_path)

    # ACT
    predictions = [
        predict_result(processed_img)
        for _ in range(3)
    ]

    # ASSERT
    assert all(
        prediction == predictions[0]
        for prediction in predictions
    )
