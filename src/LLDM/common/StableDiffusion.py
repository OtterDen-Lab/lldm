﻿import os

import requests
import io
import base64
from PIL import Image, PngImagePlugin

from helpers.FileControl import *



def generate():
    # Use local instance, the gradio link will expire after 72 hours
    url = "http://127.0.0.1:7860"
    #url = "https://664176ef9c42434e22.gradio.live"
    # Read from file input
    from LLDM.common.GPT import PATH_SDCONFIG_PROMPT, PATH_SDCONFIG_NEGATIVE, PATH_OUTPUT_STABLEDIFFUSION
    prompt = read(PATH_SDCONFIG_PROMPT)
    negativePrompt = read(PATH_SDCONFIG_NEGATIVE)

    payload = {
        "seed": -1,
        "prompt": "fantasy, dungeons and dragons, , " + prompt + " <lora:more_details:1> ",
        "steps": 50,
        "cfg_scale": 7,
        "sampler_name": "DDIM",
        "sampler_index": "DDIM",
        "negative_prompt": negativePrompt,
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

        if not os.path.exists(PATH_OUTPUT_STABLEDIFFUSION):
            os.makedirs(PATH_OUTPUT_STABLEDIFFUSION)

        img_path = uniquify(f'{PATH_OUTPUT_STABLEDIFFUSION}output.png')
        image.save(img_path, pnginfo=pnginfo)
        # image.show()
        static_img_path = uniquify(f'src/LLDM/common/static/images/output.png')
        image.save(static_img_path, pnginfo=pnginfo)

        return static_img_path.replace('src/LLDM/common/static/images/', '')


#
# if __name__ == '__main__':
#     generate()
#


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path