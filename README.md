# Project Overview:
LLDM is a Python application that integrates OpenAI and StableDiffusion to produce text adventures and accompanying imagery similar to fantasy tabletop games. It aims to apply a framework to generative tools to capture and integrate tailored responses, expanding the game’s depth and complexity the longer it’s played.
## Technical Stack:
This application primarily uses several external tools and technologies.  
The application is written for Python 3.10, with dependencies such as Flask, Jinja2, openai, Pillow, and PyPDF2. There is a full, pip-frozen list of dependencies included in requirements.txt. 

External services are also called:
- OpenAI API for calls to the GPT (Remote endpoint)
  - gpt-3.5-turbo-1104 (Preferred due to cost)
  - gpt-4-1106-preview (Higher quality, significantly more expensive)  
**Note**: v1104 or v1106 must be used, as this application relies on parallel function calling.
  
- StableDiffusion 1.5 for Image Generation (Locally hosted instance)
  - Automatic1111’s [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
  - AbdBarho’s [stable-diffusion-webui-docker](https://github.com/AbdBarho/stable-diffusion-webui-docker)
  - Zovya’s [“A-Zovya RPG Artist Tools”](https://civitai.com/models/8124?modelVersionId=87886)
  - Lykon’s [“Add More Details - Detail Enhancer / Tweaker (细节调整) LoRA”](https://civitai.com/models/82098/add-more-details-detail-enhancer-tweaker-lora)


# Project-Specific Resources:
For our project, this application is run remotely on Dr. Sam Ogden’s port-forwarded remote server using the AbdBarho’s Docker fork of the stable-diffusion-webui. This application also assumes that the Flask Web Application and the StableDiffusion instance are running on the same server.
## Installation Guide:
**This guide assumes the following**:
- You have access to LLDM’s source code & repository.
- You have access to an OpenAI API key
- You have root access to your machine.
- You have a virtual environment (venv) of Python 3.10 with all dependencies from ‘requirements.txt’ installed.  
This guide is for setting all services up locally. Port forward the Flask WebApp and/or StableDiffusion at your discretion.


### Step 1: Download Stable-Diffusion-Webui
Note: This project uses AbdBarho’s Docker fork of AUTOMATIC1111’s stable-diffusion-webui as the Docker container allows for hassle-free installations on multiple operating systems.  
Both will work for this application, but setup instructions differ between the two, so please read their Setup & Usage pages and follow their directions for installation and building.

### Step 1a: (Optional, recommended) Download Checkpoint & LoRA from Civitai.com
Download the following StableDiffusion 1.5 Checkpoint and LoRA:
- Checkpoint: A-Zovya RPG Artist Tools (V3+VAE) (Full or Pruned)
- LoRA: Add More Details - Detail Enhancer / Tweaker (细节调整) LoRA


Paste each file into the appropriate folder:  
`stable-diffusion-webui/models/Stable-diffusion` for the Checkpoint, and  
`stable-diffusion-webui/models/Lora` for the LoRA.  
**Note**: Docker users, navigate to (`stable-diffusion-webui-docker/data/models`).

### Step 2: Run the StableDiffusion Instance (default port: 7860).
Run the following batch file:	`webui-user.bat`   
For Docker users, execute: 	`docker compose --profile auto up --build`  
**Note**: The Docker command assumes you have already run the download command.

### Step 3: Clone LLDM Project Repo & Setup Virtual Environment
Clone the main branch of the repository to a local directory of your choice.  
Make sure you have a venv with all the external dependencies from ‘requirements.txt’!

### Step 4: Configure venv
Include paths to the LLDM package as part of the activation script of the virtual environment  
Inside `venv/bin/activate`, append the following lines to the bottom of the file:  
`export PYTHONPATH="<absolute-path-to>/lldm/src:$PYTHONPATH"`  
`export GPTAPI="<your-openai-api-key>"`  
Replace the <>’s with your directory structure and OpenAI API key.

### Step 5: Start WebApp
Open a Terminal and navigate to `lldm/src/WebApp`  
Run the app.py script with  
`python3 app.py`
Navigate to your local address 127.0.0.1 on port 5000 (or public IP & port, if port-forwarded).
You should now have access to the webpage!
