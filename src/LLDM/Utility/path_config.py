import os
from datetime import datetime

from LLDM.Utility.FileControl import read

# Package Directory  (LLDM < Utility < path_config.py)
LLDM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENUM_DIR = os.path.join(os.path.dirname(LLDM_DIR), "Deprecated", "Data")

print(f"--Path Config:--")
print(f"PATH_CONFIG: {os.path.abspath(__file__)}")
print(f"LLDM_DIR: {LLDM_DIR}")

# External Package Directories (Like 'static' for the WebApp
WEB_APP_TEMPLATES = os.path.join(LLDM_DIR, "WebApp", "templates")
WEB_APP_IMAGES = os.path.join(os.path.dirname(LLDM_DIR), "WebApp", "static", "images")
if not os.path.exists(WEB_APP_IMAGES):
    os.makedirs(WEB_APP_IMAGES)

# Resources Directory (Contains all the GPT/SD inputs)
RESOURCES_DIR = os.path.join(LLDM_DIR, "resources")
PATH_RESOURCE_CHARACTERS = os.path.join(RESOURCES_DIR, "SampleJSON")
PATH_RESOURCE_SAMPLE_CHARACTER = os.path.join(PATH_RESOURCE_CHARACTERS, "Dragon_JSON.txt")

# GPT Subdirectory
RES_GPT_DIR = os.path.join(RESOURCES_DIR, "GPT")
PATH_CONTEXT_SDPROMPTER = os.path.join(RES_GPT_DIR, "SDPrompter.txt")
PATH_CONTEXT_SIMPLE_AGENT = os.path.join(RES_GPT_DIR, "SimpleDungeonAgent.txt")
PATH_CONTEXT_SIMPLE_EVENT = os.path.join(RES_GPT_DIR, "SimpleDungeonEvent.txt")

# GPT Battle Subdirectory 
RES_GPT_BATTLE_DIR = os.path.join(RESOURCES_DIR, "GPT")
PATH_CONTEXT_BATTLE_SDPROMPTER = os.path.join(RES_GPT_BATTLE_DIR, "BattleSDPrompter.txt")
PATH_CONTEXT_BATTLE_SIMPLE_AGENT = os.path.join(RES_GPT_BATTLE_DIR, "BattleSimpleAgent.txt")
PATH_CONTEXT_BATTLE_SIMPLE_EVENT = os.path.join(RES_GPT_BATTLE_DIR, "BattleSimpleEvent.txt")

# SD Subdirectory
RES_SD_DIR = os.path.join(RESOURCES_DIR, "SD")
PATH_SDCONFIG_NEGATIVE = os.path.join(RES_SD_DIR, "NegativePrompt.txt")
PATH_SDCONFIG_CONFIG = os.path.join(RES_SD_DIR, "Payload.txt")

# Temp/Overwritten
PATH_SDCONFIG_PROMPT = os.path.join(RES_SD_DIR, "Prompt.txt")
PATH_INPUT_USER = os.path.join(RESOURCES_DIR, "Input", "User_input.txt")

# Campaign Directory
OUTPUT_DIR = os.path.join(os.path.dirname(LLDM_DIR), "Output")
CAMPAIGNS_DIR = os.path.join(OUTPUT_DIR, "Campaigns")
campaign = str(datetime.now().strftime("%m-%d-%Y (%I.%M.%S %p)"))  # Use time of creation as placeholder campaign name
CURRENT_CAMPAIGN_DIR = os.path.join(CAMPAIGNS_DIR, f"{campaign}")
# Initialize Campaign Instance Directory
if not os.path.exists(CURRENT_CAMPAIGN_DIR):
    os.makedirs(CURRENT_CAMPAIGN_DIR)

# Instance Logs (Campaign-specific ChatCompletion Dumps)
PATH_LOG_SDPROMPTER = os.path.join(CURRENT_CAMPAIGN_DIR, "LOG_SDPROMPTER.txt")
PATH_LOG_EVENTS = os.path.join(CURRENT_CAMPAIGN_DIR, "LOG_EVENTS.txt")
PATH_OUTPUT_STABLEDIFFUSION = os.path.join(CURRENT_CAMPAIGN_DIR, "Images")
if not os.path.exists(PATH_OUTPUT_STABLEDIFFUSION):
    os.makedirs(PATH_OUTPUT_STABLEDIFFUSION)

# Touch Outputs & Logs
LogList = [
    PATH_LOG_SDPROMPTER,
    PATH_LOG_EVENTS
]
for output_path in LogList:
    with open(output_path, 'a'):
        pass

CONTEXT_SDPROMPTER = read(PATH_CONTEXT_SDPROMPTER)
CONTEXT_SIMPLE_AGENT = read(PATH_CONTEXT_SIMPLE_AGENT)
CONTEXT_SIMPLE_EVENT = read(PATH_CONTEXT_SIMPLE_EVENT)
RESOURCE_SAMPLE_CHARACTER = read(PATH_RESOURCE_SAMPLE_CHARACTER)

# Battle variations
BATTLE_CONTEXT_SDPROMPTER = read(PATH_CONTEXT_BATTLE_SDPROMPTER)
BATTLE_CONTEXT_SIMPLE_AGENT = read(PATH_CONTEXT_BATTLE_SIMPLE_AGENT)
BATTLE_CONTEXT_SIMPLE_EVENT = read(PATH_CONTEXT_BATTLE_SIMPLE_EVENT)