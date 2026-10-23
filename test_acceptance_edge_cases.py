
"""Acceptance tests for image upload edge cases."""

from io import BytesIO

from PIL import Image


def test_edge_case_missing_metadata(client, valid_image):
    """Verify that an image without EXIF metadata can be processed."""

    # ARRANGE
    image = Image.open(valid_image)
    assert not image.getexif()

    # ACT
    valid_image.seek(0)
    response = client.post(
        "/prediction",
        data={"file": (valid_image, "no_metadata.jpg")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data


def test_edge_case_non_standard_image_extension(client, valid_image):
    """Verify that the application can process a WebP image."""

    # ARRANGE
    image = Image.open(valid_image)

    webp_data = BytesIO()
    image.save(webp_data, format="WEBP")
    webp_data.seek(0)

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (webp_data, "test_image.webp")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data


def test_edge_case_sequential_image_uploads(client, valid_image):
    """Verify that consecutive valid uploads are processed independently."""

    # ARRANGE
    image = Image.open(valid_image)

    second_image = BytesIO()
    image.save(second_image, format="JPEG")
    second_image.seek(0)

    # ACT
    valid_image.seek(0)
    response1 = client.post(
        "/prediction",
        data={"file": (valid_image, "first_image.jpg")},
        content_type="multipart/form-data"
    )

    response2 = client.post(
        "/prediction",
        data={"file": (second_image, "second_image.jpg")},
        content_type="multipart/form-data"
    )

    # ASSERT
    assert response1.status_code == 200
    assert response2.status_code == 200

    assert b"File cannot be processed." not in response1.data
    assert b"File cannot be processed." not in response2.data

    assert b"Prediction" in response1.data
    assert b"Prediction" in response2.data


def test_edge_case_unexpected_headers(client, valid_image):
    """Verify that an unexpected HTTP header does not prevent processing."""

    # ACT
    response = client.post(
        "/prediction",
        data={"file": (valid_image, "test_image.jpg")},
        content_type="multipart/form-data",
        headers={"X-Unexpected-Header": "value"}
    )

    # ASSERT
    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert b"Prediction" in response.data
