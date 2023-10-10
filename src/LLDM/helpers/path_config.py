import os
from datetime import datetime
from LLDM.helpers.FileControl import *

# Package Directory  (LLDM < helpers < path_config.py)
LLDM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f"--Path Config:--")
print(f"__FILE__: {os.path.abspath(__file__)}")
print(f"LLDM_DIR: {LLDM_DIR}")

# External Package Directories (Like 'static' for the WebApp
WEB_APP_IMAGES = os.path.join(os.path.dirname(LLDM_DIR), "WebApp", "static", "images")

# Resources Directory (Contains all the GPT/SD inputs)
RESOURCES_DIR = os.path.join(LLDM_DIR, "resources")

# TESTING DATA DRAGONBORN SORCERER SAMPLE
PATH_RESOURCE_CHARACTERS         = os.path.join(RESOURCES_DIR, "SampleJSON")
PATH_RESOURCE_SAMPLE_CHARACTER   = os.path.join(PATH_RESOURCE_CHARACTERS, "Dragon_JSON.txt")

# GPT Subdirectory
RES_GPT_DIR = os.path.join(RESOURCES_DIR, "GPT")
PATH_CONTEXT_GAMEMASTER          = os.path.join(RES_GPT_DIR, "GameAnalyst.txt")
PATH_CONTEXT_GAMESETUP           = os.path.join(RES_GPT_DIR, "GameSetup.txt")
PATH_CONTEXT_SDPROMTER           = os.path.join(RES_GPT_DIR, "SDPrompter.txt")
PATH_CONTEXT_CHRONICLER          = os.path.join(RES_GPT_DIR, "Chronicler.txt")

# SD Subdirectory
RES_SD_DIR = os.path.join(RESOURCES_DIR, "SD")
PATH_SDCONFIG_NEGATIVE           = os.path.join(RES_SD_DIR, "NegativePrompt.txt")
PATH_SDCONFIG_CONFIG             = os.path.join(RES_SD_DIR, "Payload.txt")

# Temp/Overwritten
PATH_SDCONFIG_PROMPT             = os.path.join(RES_SD_DIR, "Prompt.txt")
PATH_INPUT_USER                  = os.path.join(RESOURCES_DIR, "Input", "User_input.txt")


# Campaign Directory
OUTPUT_DIR = os.path.join(LLDM_DIR, "Output")
CAMPAIGNS_DIR = os.path.join(OUTPUT_DIR, "Campaigns")
campaign = str(datetime.now().strftime("%m-%d-%Y (%I.%M.%S %p)"))  # Use time of creation as placeholder campaign name
CURRENT_CAMPAIGN_DIR = os.path.join(CAMPAIGNS_DIR, f"{campaign}")
# Initialize Campaign Instance Directory
if not os.path.exists(CURRENT_CAMPAIGN_DIR):
    os.makedirs(CURRENT_CAMPAIGN_DIR)

# Instance Logs (Campaign-specific ChatCompletion Dumps)
PATH_OUTPUT_GAMEMASTER           = os.path.join(CURRENT_CAMPAIGN_DIR, "OUTPUT_GAMEMASTER.txt")
PATH_OUTPUT_CHRONICLER           = os.path.join(CURRENT_CAMPAIGN_DIR, "OUTPUT_CHRONICLER.txt")
# NOTE: Chronicler output is overwritten (summary-of-summary to preserve tokens)

PATH_LOG_GAMEMASTER              = os.path.join(CURRENT_CAMPAIGN_DIR, "LOG_GAMEMASTER.txt")
PATH_LOG_SDPROMPTER              = os.path.join(CURRENT_CAMPAIGN_DIR, "LOG_SDPROMPTER.txt")
PATH_LOG_CHRONICLER              = os.path.join(CURRENT_CAMPAIGN_DIR, "LOG_CHRONICLER.txt")
PATH_OUTPUT_STABLEDIFFUSION      = os.path.join(CURRENT_CAMPAIGN_DIR, "Images")
if not os.path.exists(PATH_OUTPUT_STABLEDIFFUSION):
    os.makedirs(PATH_OUTPUT_STABLEDIFFUSION)

# Touch Outputs & Logs
LogList = [
    PATH_OUTPUT_GAMEMASTER,
    PATH_OUTPUT_CHRONICLER,
    PATH_LOG_GAMEMASTER,
    PATH_LOG_SDPROMPTER,
    PATH_LOG_CHRONICLER
]

for output_path in LogList:
    with open(output_path, 'a'):
        pass

CONTEXT_GAMESETUP    = read(PATH_CONTEXT_GAMESETUP)
CONTEXT_GAMEMASTER   = read(PATH_CONTEXT_GAMEMASTER)
CONTEXT_SDPROMTER    = read(PATH_CONTEXT_SDPROMTER)
CONTEXT_CHRONICLER   = read(PATH_CONTEXT_CHRONICLER)
RESOURCE_SAMPLE_CHARACTER = read(PATH_RESOURCE_SAMPLE_CHARACTER)