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
                "downloads/" + str(ask_question_to_pdf.num_doc) + filename
            )
            ask_question_to_pdf.space_downloads()
            file.save(file_path)
            ask_question_to_pdf.content_downloads = ask_question_to_pdf.maj_downloads()

            ask_question_to_pdf.num_doc = rotation(ask_question_to_pdf.num_doc)
            ask_question_to_pdf.filename = file_path
            ask_question_to_pdf.document = ask_question_to_pdf.read_doc(
                ask_question_to_pdf.filename
            )
            ask_question_to_pdf.chunks = ask_question_to_pdf.split_text(
                ask_question_to_pdf.document
            )

            return {"filename": filename}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "pdf",
        "txt",
        "docx",
    }


def suppr_download(filename):
    # os.chmod("downloads/" + filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    os.remove(os.path.join(os.path.dirname(__file__), "downloads", filename))


@app.route("/charger", methods=["POST"])
def charger():
    data = request.get_json()
    selected_value = data.get("document")
    num_doc = int(selected_value) - 1
    print(num_doc)
    if selected_value != "" and ask_question_to_pdf.content_downloads[num_doc] != "":
        file_path = os.path.join(
            "downloads/" + ask_question_to_pdf.content_downloads[num_doc]
        )
        ask_question_to_pdf.filename = file_path
        ask_question_to_pdf.document = ask_question_to_pdf.read_doc(
            ask_question_to_pdf.filename
        )
        ask_question_to_pdf.chunks = ask_question_to_pdf.split_text(
            ask_question_to_pdf.document
        )

    return "ok"


def rotation(i):
    if i == 5:
        return 1
    else:
        return i + 1


@app.route("/reset", methods=["POST"])
def reset():
    # print("bbbbbbbbbbbbb")
    ask_question_to_pdf.content_downloads = ask_question_to_pdf.vider_downloads()
    ask_question_to_pdf.num_doc = 1
    return "ok"
