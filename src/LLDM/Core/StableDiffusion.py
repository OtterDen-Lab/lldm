import requests
import io
import base64
from PIL import Image, PngImagePlugin

from LLDM.Utility.path_config import *


# Use local instance, as gradio links expire after 72 hours
url = "http://127.0.0.1:7860"

# If using remote, Automatic1111's webapp can be hosted on gradio by using the --share init parameter
# url = "https://664176ef9c42434e22.gradio.live"


# On load, set the SD model and lora
option_payload = {
    "sd_model_checkpoint": "aZovyaRPGArtistTools_v3VAE.safetensors [8c4042921a]",
    "sd_lora": "more_details"
}
requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)


def is_url_alive():
    """
    :return: boolean representing image generator service accessibility
    """
    try:
        response = requests.get(url)
        # If the response status code is 200, the URL is alive
        return response.status_code == 200
    except requests.RequestException:
        # If any exception occurs, the URL is probably down or invalid
        return False


def generate(prompt: str, title=None):
    """
    Image Generator using an HTTP call to StableDiffusion
    Saves a png to both Campaign dir & WebApp Static img dir
    :param prompt: prompt for image generation (format for SD)
    :param title: optional title for filename
    :return: file path to static image
    """
    filename = title if title is not None else "output"

    # Read config parameters from file
    negative_prompt = read(Routes.PATH_SDCONFIG_NEGATIVE)

    # These are the config parameters for StableDiffusion. Bare minimum is modified.
    payload = {
        "seed": -1,
        "prompt": "fantasy, dungeons and dragons, " + prompt + " <lora:more_details:1> ",
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

        # Save Image to Campaign Images
        img_path = uniquify(os.path.join(Routes.PATH_OUTPUT_STABLEDIFFUSION, f"{filename}.png"))
        image.save(img_path, pnginfo=pnginfo)

        # Save Image to WebApp Static
        static_img_path = uniquify(os.path.join(Routes.WEB_APP_IMAGES, f"{filename}.png"))
        image.save(static_img_path, pnginfo=pnginfo)

        return os.path.basename(static_img_path)


def uniquify(path):
    """
    Helper function to ensure unique filenames.
    :param path: the filepath
    :return: unique filepath
    """
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path
