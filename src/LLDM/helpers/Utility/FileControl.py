import json
import PyPDF2


def read(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content


def write(path, content):
    file = open(path, "w")
    file.write(content)
    file.close()


def append(path, content):
    file = open(path, "a")
    file.write("\n" + content)
    file.close()


def extract_pdf_fields(pdf_path):

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        fields = reader.get_fields()
        fields_data = {k: v.get('/V', None) for k, v in fields.items()}

    return json.dumps(fields_data, ensure_ascii=False, indent=4)
