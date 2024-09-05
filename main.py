from flask import Flask
from flask import render_template
from flask import request
from src.utils import ask_question_to_pdf
import os

app = Flask(__name__)
conversation = []

# @app.route("/")
# def hello_world():
#    return "<p>Hello, World!</p>"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def bot_prompt():
    if request.method == "POST":
        response = ask_question_to_pdf.gpt3_completion(
            request.form["prompt"], ask_question_to_pdf.document, conversation
        )
        return {"answer": response}


@app.route("/question", methods=["GET", "POST"])
def bot_submit():
    if request.method == "GET":
        response = ask_question_to_pdf.gpt3_question(
            ask_question_to_pdf.document, conversation
        )
        return {"answer": response}


@app.route("/answer", methods=["POST"])
def bot_answer():
    if request.method == "POST":
        response = ask_question_to_pdf.gpt3_correct(
            request.form["prompt"], ask_question_to_pdf.document, conversation
        )
        return {"answer": response}


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file-upload"]
        if file and allowed_file(file.filename):
            filename = file.filename

            # Sauvegarder le fichier
            file_path = os.path.join(
                "downloads/" + filename
            )  # ce sera pour quand on en aura plusieurs à la fois lol
            file.save(file_path)
            ask_question_to_pdf.filename = file_path
            ask_question_to_pdf.document = ask_question_to_pdf.read_doc(
                ask_question_to_pdf.filename
            )
            ask_question_to_pdf.chunks = ask_question_to_pdf.split_text(
                ask_question_to_pdf.document
            )

            return "ok"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "pdf",
        "txt",
        "docx",
    }
