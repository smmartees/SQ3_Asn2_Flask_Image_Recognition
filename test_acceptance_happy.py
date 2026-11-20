# test_acceptance_happy.py

from io import BytesIO
from PIL import Image
import pytest
from flask_wtf.csrf import generate_csrf
from html.parser import HTMLParser

class CSRFTokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = None

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            attributes = dict(attrs)
            if attributes.get("name") == "csrf_token":
                self.token = attributes.get("value")

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


def test_acceptance_grayscale_upload(client):
    """Verify that a grayscale image can be uploaded and processed."""

    # ARRANGE
    grayscale_image = Image.new("L", (224, 224), color=128)

    image_data = BytesIO()
    grayscale_image.save(image_data, format="PNG")
    image_data.seek(0)

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (image_data, "grayscale.png")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data

def test_acceptance_good_cookie(validClient):
    """Verify that a valid CSRF token allows image uploads."""

    # ARRANGE
    page = validClient.get("/")

    parser = CSRFTokenParser()
    parser.feed(page.get_data(as_text=True))
    token = parser.token

    assert token is not None

    grayscale_image = Image.new("L", (224, 224), color=128)

    image_data = BytesIO()
    grayscale_image.save(image_data, format="PNG")
    image_data.seek(0)

    # ACT
    response = validClient.post(
        "/prediction",
        data={
            "file": (image_data, "grayscale.png"),
            "csrf_token": token
        },
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data
