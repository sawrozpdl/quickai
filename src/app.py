import os
from age import detect
from os.path import dirname, join
from profanity_filter import ProfanityFilter
from flask import Flask, request, jsonify, url_for

from flask_cors import CORS, cross_origin

app = Flask(__name__)
pf = ProfanityFilter()

CORS(app, support_credentials=True)

@app.route('/')
@cross_origin(supports_credentials=True)
def greet():
    return jsonify(app="Quick AI", version="1.0.0")


UPLOAD_FOLDER = join(dirname(__file__), "../uploads/")


@app.route('/detect/age', methods=['POST'])
@cross_origin(supports_credentials=True)
def age_detect():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify(status="Fail", message="No image found")
        image = request.files['image']

        path = os.path.join(UPLOAD_FOLDER, request.remote_addr)
        image.save(path)
        detected = detect.age(path)

        build = {
            "status": 'Fail',
            "result": None
        }

        if detected:
            build["status"] = "Success"
            build["result"] = detected

        return jsonify(build)


@app.route('/detect/profanity', methods=['GET'])
@cross_origin(supports_credentials=True)
def profanity_filter():
    string = request.args.get('string')
    return jsonify(status="Success", hasProfanity=not pf.is_clean(string), filtered=pf.censor(string))


if __name__ == "__main__":
    app.run(host=os.environ.get('HOST') or "0.0.0.0",
            port=os.environ.get('PORT') or 5000)
