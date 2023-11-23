# from LLDM.GPT import *
# from LLDM.helpers.JSONControl import *
import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from LLDM.Utility.path_config import WEB_APP_IMAGES
from main import process_input, get_map, get_character, get_events, get_img

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # for flash messages

# Select a random image from our static folder
background_image_filename = random.choice(os.listdir(WEB_APP_IMAGES))
print(f"Background Image: {background_image_filename}")

# Accepted file formats for uploads
ALLOWED_EXTENSIONS = {'pdf'}


# app.config['PATH_UPLOAD_FOLDER'] = PATH_UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Storage of messages to be sent to frontend
messages = [
    {"sender": "bot", "text": "I am LLDM, your narrator for this session. Type \"exit\" to stop this program."}
]


@app.route('/')
def index():
    global background_image_filename
    files = [f for f in os.listdir(WEB_APP_IMAGES) if f != background_image_filename]
    new_random_file = random.choice(files)
    background_image_filename = new_random_file
    return render_template('home.html', filename=background_image_filename)


@app.route('/chat/', methods=['GET'])
def chat():
    global background_image_filename
    return render_template('chat.html', filename=background_image_filename, messages=messages, box1=get_map(),
                           box2=get_character())


@app.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.form['message']
    messages.append({"sender": "user", "text": message_text})
    process_input(message_text)  # This updates what the getter functions return
    bot_responses = [
        get_events()
    ]
    for response in bot_responses:
        messages.append({"sender": "bot", "text": response})

    image_path = url_for('static', filename='images/' + get_img())

    return jsonify({"bot_responses": bot_responses, "character_info": get_character(), "map_info": get_map(),
                    "image_path": image_path})


if __name__ == '__main__':
    app.run()


def start():
    app.run(host="0.0.0.0", port=5000)
