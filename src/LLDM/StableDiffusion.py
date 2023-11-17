﻿import os

import requests
import io
import base64
from PIL import Image, PngImagePlugin

from .helpers.path_config_false import *


def generate():
    # Use local instance, the gradio link will expire after 72 hours
    url = "http://127.0.0.1:7860"
    #url = "https://664176ef9c42434e22.gradio.live"
    # Read from file input
    prompt = read(PATH_SDCONFIG_PROMPT)
    negative_prompt = read(PATH_SDCONFIG_NEGATIVE)

    payload = {
        "seed": -1,
        "prompt": "fantasy, dungeons and dragons, , " + prompt + " <lora:more_details:1> ",
        "steps": 50,
        "cfg_scale": 7,
        "sampler_name": "DDIM",
        "sampler_index": "DDIM",
        "negative_prompt": negative_prompt,
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        img_path = uniquify(os.path.join(PATH_OUTPUT_STABLEDIFFUSION, "output.png"))
        image.save(img_path, pnginfo=pnginfo)
        # image.show()
        static_img_path = uniquify(os.path.join(WEB_APP_IMAGES, "output.png"))
        image.save(static_img_path, pnginfo=pnginfo)

        # print(f"Image Output Path: {static_img_path}")
        # print(f"Image Filename: {os.path.basename(static_img_path)}")
        return os.path.basename(static_img_path)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path
