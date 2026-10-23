# Importing required libs
"""Flask application for image recognition and prediction."""
from flask import Flask, render_template, request
from PIL import UnidentifiedImageError
from werkzeug.exceptions import BadRequestKeyError

from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    """Render the application's homepage."""
    return render_template("index.html")


# Prediction route
@app.route('/prediction', methods=['POST'])
def predict_image_file():
    """Process an uploaded image and render its prediction."""
    try:
        img = preprocess_img(request.files['file'].stream)
        pred = predict_result(img)
        return render_template("result.html", predictions=str(pred))

    except (BadRequestKeyError, UnidentifiedImageError, OSError, ValueError):
        error = "File cannot be processed."
        return render_template("result.html", err=error)


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
