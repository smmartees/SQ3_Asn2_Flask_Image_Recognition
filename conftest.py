

import pytest
from io import BytesIO
from PIL import Image
from app import app  # This imports the Flask app for testing

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_image():
    """Provide a valid JPEG image stored in memory."""
    img_data = BytesIO()

    image = Image.new("RGB", (224, 224), color="white")
    image.save(img_data, format="JPEG")

    img_data.seek(0)

    yield img_data

    img_data.close()
