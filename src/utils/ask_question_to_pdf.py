from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
from docx import Document

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


# goal : be able to read a txt
def read_txt(filename):
    with open(filename, "r") as file:
        data = file.read().replace("\n", "")
    return data


# goal : be able to read a docx
def read_docx(filename):
    doc = Document(filename)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "../../festival.docx")
length_name = len(filename)

if filename[(length_name - 3):] == "pdf":
    document = read_pdf(filename)
    print("pdf")
elif filename[length_name - 3 :] == "txt":
    document = read_txt(filename)
    print("txt")
else:
    document = read_docx(filename)
    print("docx")
chunks = split_text(document)
tx1 = "Réponds aux questions en te basant"
tx2 = "sur le document suivant :"


def gpt3_completion(ppt, doc=document, chatlog=[]):
    print(doc)

    client = openai.OpenAI()
    if (len(chatlog) == 0):
        chatlog.append({"role": "user", "content": tx1+tx2+doc})
    chatlog.append({"role": "user", "content": ppt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chatlog,
    )
    chatlog.append({"role": "assistant",
                    'content': response.choices[0].message.content})
    # messages.append(role, reponse : response.choices[0].message.content)
    # bouton "je vais transmettre un document : modifier message sysyème (doc)
    # en appuyant sur un bouton, on modifie les paramètres du fichier css
    # les boutons sont à déclarer dans html
    print(response)
    return response.choices[0].message.content


def gpt3_question(chatlog=[]):
    client = openai.OpenAI()
    chatlog.append({"role": "system",
                    "content": "Ask a question about the document now"})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chatlog,
    )
    chatlog.append({"role": "assistant",
                    'content': response.choices[0].message.content})
    return response.choices[0].message.content

