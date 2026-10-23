# test_integration_happy.py

from io import BytesIO
import pytest

def test_successful_prediction(client, valid_image):
    """Verify that a valid image passes through the prediction pipeline."""

    # ARRANGE
    valid_image.seek(0)

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (valid_image, "test.jpg")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data
