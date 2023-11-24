import requests
import io
import base64
from PIL import Image, PngImagePlugin

from LLDM.Utility.path_config import *


# Use local instance, as gradio links expire after 72 hours
url = "http://127.0.0.1:7860"

# If using remote, Automatic1111's webapp can be hosted on gradio by using the --share init parameter
# url = "https://664176ef9c42434e22.gradio.live"


def is_url_alive():
    try:
        response = requests.get(url)
        # If the response status code is 200, the URL is alive
        return response.status_code == 200
    except requests.RequestException:
        # If any exception occurs, the URL is probably down or invalid
        return False


def generate(title=None):
    filename = title if title is not None else "output"

    # Read config parameters from file
    prompt = read(PATH_SDCONFIG_PROMPT)
    negative_prompt = read(PATH_SDCONFIG_NEGATIVE)

    # These are the config parameters for StableDiffusion. Bare minimum is modified.
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

    # POST call to SD service.
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        img_path = uniquify(os.path.join(PATH_OUTPUT_STABLEDIFFUSION, f"{filename}.png"))
        image.save(img_path, pnginfo=pnginfo)
        # image.show()
        static_img_path = uniquify(os.path.join(WEB_APP_IMAGES, f"{filename}.png"))
        image.save(static_img_path, pnginfo=pnginfo)

        # print(f"Image Output Path: {static_img_path}")
        # print(f"Image Filename: {os.path.basename(static_img_path)}")
        return os.path.basename(static_img_path)


# Helper function to ensure unique filenames.
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path
