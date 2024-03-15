from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from flaskr.demo_model.run_uie_inference import run_uie_inference
from .llm.llm import annotate_text, annotate_bulk
from .demo_model.run_flant5_inference import run_flant5_inference
from .demo_model.format_transfer.sel2record_phee import convert_to_record

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

@app.route("/flant5", methods=["POST"])
def flant5():
    data = request.get_json()
    print(data)

    seq_result = run_flant5_inference(data["text"])
    record_result = convert_to_record(seq_result)
    
    return record_result

@app.route("/uie", methods=["POST"])
def uie():
    data = request.get_json()
    print(data)

    seq_result = run_uie_inference(data["text"])
    record_result = convert_to_record(seq_result)
    
    return record_result

@app.route("/mistral7b", methods=["POST"])
def mistral7b():
    data = request.get_json()
    print(data)

    return annotate_bulk(data["text"])

# @app.route("/chat", methods=["POST"])
# def chat():
#     print(request.get_json())
#     data = request.get_json()
    
#     return chat_with_llm(data["text"])



if __name__ == "__main__":
    app.run()