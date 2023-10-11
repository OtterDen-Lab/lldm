# from LLDM.GPT import *
# from LLDM.helpers.JSONControl import *

import random
from flask import Flask, render_template, request, redirect, url_for, flash

from LLDM.GPT import *
from LLDM.helpers.JSONControl import *
from LLDM.Character import Character

# PATH_BACKGROUND_IMAGES = "src/LLDM/common/static/images"
PATH_UPLOAD_FOLDER = PATH_RESOURCE_CHARACTERS
PATH_PLAYER_CHARACTER = PATH_RESOURCE_CHARACTERS + "/PC"

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # for flash messages

background_image_filename = random.choice(os.listdir(WEB_APP_IMAGES))
print(f"Background Image: {background_image_filename}")

ALLOWED_EXTENSIONS = {'pdf'}

app.config['PATH_UPLOAD_FOLDER'] = PATH_UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/startup/')
def character_creation():
    return render_template('character_creation.html', filename=background_image_filename)


@app.route('/startup/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Here, you can save the file or process it
        filepath = os.path.join(app.config['PATH_UPLOAD_FOLDER'], file.filename)
        stripped_filename = '.'.join(file.filename.split('.')[:-1])
        json_filename = stripped_filename + '.txt'
        file.save(filepath)
        flash('File successfully uploaded')
        print("Writing JSON to " + PATH_PLAYER_CHARACTER+"/"+json_filename)
        write(PATH_PLAYER_CHARACTER +"/" + json_filename, extract_pdf_fields(filepath))
        return redirect(url_for('chat'))

    else:
        flash('Allowed file type is PDF')
        return redirect(request.url)


@app.route('/')
def index():
    global background_image_filename
    files = [f for f in os.listdir(WEB_APP_IMAGES) if f != background_image_filename]
    new_random_file = random.choice(files)
    background_image_filename = new_random_file
    return render_template('home.html', filename=background_image_filename)


# @app.route('/chat/')
# def chat():
#     input_string = request.args.get('input', '')
#     message = GPT.generate_message(input_string)
#     return render_template('chat.html', filename=background_image_filename, message=message)

@app.route('/chat/', methods=['GET', 'POST'])
def chat():
    global background_image_filename
    character = ""
    message = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input == "Print Environ":
            print("Sending request to GPT")
            background_image_filename = print_image()
        else:
            print("Sending request to GPT")
            message = process_input(user_input)
            print(message)
    elif len(os.listdir(PATH_PLAYER_CHARACTER)) > 0:
        # Fix this so file-names are easier to get / the onus of proper file naming is not on this function
        chars = os.listdir(PATH_PLAYER_CHARACTER)
        if len(chars) > 0:
            path_of_character = PATH_PLAYER_CHARACTER + "/" + chars[0]
            character = read(path_of_character)
            print("Sending request to GPT")
            message = place_character(path_of_character)
            print(message)
    else:
        print("Skipped Profile: Unexpected results expected!")
        character = Character(PATH_RESOURCE_SAMPLE_CHARACTER)
        print(f"(APP) Character: {character}")
        message = place_player(character)

    return render_template('chat.html', filename=background_image_filename, character=character, message=message)


if __name__ == '__main__':
    app.run()


def start():
    app.run(host="0.0.0.0", port=5000)
