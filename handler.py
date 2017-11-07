from flask import Flask, request
import json

from main import createAnswer

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def handel():
        update = request.data.decode("utf-8")
        update = json.loads(update)
        createAnswer(update)
        return ""

if __name__ == '__main__':
        app.run(host='0.0.0.0')