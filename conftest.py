

import pytest
from io import BytesIO
from PIL import Image
from app import app  # This imports the Flask app for testing

@pytest.fixture
def client():
    original = app.config["WTF_CSRF_ENABLED"]
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as test_client:
        yield test_client

    app.config["WTF_CSRF_ENABLED"] = original


@pytest.fixture
def validClient():
    original = app.config["WTF_CSRF_ENABLED"]
    app.config["WTF_CSRF_ENABLED"] = True

    with app.test_client() as valid_client:
        yield valid_client

    app.config["WTF_CSRF_ENABLED"] = original

@pytest.fixture
def valid_image():
    """Provide a valid JPEG image stored in memory."""
    img_data = BytesIO()

    image = Image.new("RGB", (224, 224), color="white")
    image.save(img_data, format="JPEG")

    img_data.seek(0)

    yield img_data

    img_data.close()
