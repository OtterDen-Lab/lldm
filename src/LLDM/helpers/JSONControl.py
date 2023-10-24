# Implement methods to get specific categories of data from JSON schema (e.g. get equipment, get core stats, etc)
from json import JSONEncoder

import PyPDF2
import json


def extract_pdf_fields(pdf_path):

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        fields = reader.get_fields()
        fields_data = {k: v.get('/V', None) for k, v in fields.items()}

    return json.dumps(fields_data, ensure_ascii=False, indent=4)



