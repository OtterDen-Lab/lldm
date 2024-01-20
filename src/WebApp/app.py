# from LLDM.GPT import *
# from LLDM.helpers.JSONControl import *
import os
import random
from flask import Flask, render_template, request, url_for, jsonify

from LLDM.Utility import Routes
from main import get_main_character, main_gen_img, get_img, get_map, handle_input


app = Flask(__name__)
app.secret_key = 'some_secret_key'  # for flash messages

# Select a random image from our static folder
background_image_filename = random.choice(os.listdir(Routes.WEB_APP_IMAGES))
print(f"Background Image: {background_image_filename}")

# Accepted file formats for uploads
ALLOWED_EXTENSIONS = {'pdf'}

# app.config['PATH_UPLOAD_FOLDER'] = PATH_UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Storage of messages to be sent to frontend
messages = [
    {"sender": "bot",
     "text": "I am LLDM, your narrator for this session. \n"
             "Details of this adventure are listed on the right, and will be updated as you progress. \n"
             "Please enter your actions in the field below."}
]


@app.route('/')
def index():
    """Home Page for the Web Application"""
    global background_image_filename
    files = [f for f in os.listdir(Routes.WEB_APP_IMAGES) if f != background_image_filename]
    new_random_file = random.choice(files)
    background_image_filename = new_random_file
    return render_template('home.html', filename=background_image_filename)


@app.route('/chat/', methods=['GET'])
def chat():
    """Main Content Page for the chat interface"""
    global background_image_filename
    return render_template('chat.html', filename="Room 1.png", messages=messages, box1=get_map(),
                           box2=get_main_character())


@app.route('/generate_image', methods=['POST'])
def generate_image():
    """A debug tool test function for image generation. Ex: use when the image generator is offline"""
    test = main_gen_img()
    return jsonify({"image_path": test, "image_name": test})


@app.route('/send_message', methods=['POST'])
def send_message():
    """POST function for user input. Handles updating page content and interfaces with LLDM"""
    message_text = request.form['message']
    messages.append({"sender": "user", "text": message_text})

    bot_responses = handle_input(message_text)
    str_responses = []
    for response in bot_responses:
        messages.append({"sender": "bot", "text": str(response)})
        str_responses.append(str(response))

    if get_img():
        image_name = get_img().removesuffix(".png")
        image_path = url_for('static', filename='images/' + get_img())

        return jsonify({"bot_responses": str_responses, "character_info": get_main_character(), "map_info": get_map(),
                        "image_path": image_path, "image_name": image_name})
    return jsonify({"bot_responses": str_responses, "character_info": get_main_character(), "map_info": get_map()})


if __name__ == '__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)
