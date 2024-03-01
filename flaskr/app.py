from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from .llm.llm import annotate_text, chat_with_llm

app = Flask(__name__)
cors = CORS(app)    
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/annotate", methods=["POST"])
def annotate():
    data = request.get_json()
    print(data)

    return annotate_text(data["text"])

@app.route("/chat", methods=["POST"])
def chat():
    print(request.get_json())
    data = request.get_json()
    
    return chat_with_llm(data["text"])


if __name__ == "__main__":
    app.run()