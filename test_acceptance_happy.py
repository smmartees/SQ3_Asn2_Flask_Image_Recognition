# test_acceptance_happy.py

from io import BytesIO
from PIL import Image
import pytest

def test_acceptance_successful_upload(client, valid_image):
    """Verify that a valid image produces a prediction."""

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (valid_image, "test_image.jpg")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data


def test_acceptance_valid_large_image(client, valid_image):
    """Verify that a valid image produces a prediction."""
    # ARRANGE
    image = Image.open(valid_image)
    large_image = image.resize((1000, 1000))

    large_img_data = BytesIO()
    large_image.save(large_img_data, format="JPEG")
    large_img_data.seek(0)

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (large_img_data, "large_image.jpg")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data
