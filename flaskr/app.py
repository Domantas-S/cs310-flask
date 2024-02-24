from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/annotate", methods=["POST"])
def annotate():
    # Access the request data
    data = request.get_json()

    # Process the data and perform necessary operations
    # ...

    # Return a response
    return "Annotation created successfully"

if __name__ == "__main__":
    app.run()
