# Secret Prototype 1 made in ~1 week? (like 3 days, really)
# Requirements: Working Internet Connection
#               Install openai (pip install openai)
#               Install PIL    (pip install Pillow)
# Ray Van Horn
#
# Current Issues:
# 1. GameMaster sometimes asks player for input, which derails Chronicler
# 2. Chronicler SYSTEM prompt probably needs more refinement
# 3. Since SDPrompter takes in a Chronicler summary as input, sometiems junk data ends up in the prompt.
# But visually, this is often invisible.

from datetime import datetime
import os
import openai
import json

from FileControl import *
import StableDiffusion

# openai.api_key = os.getenv("")
# Using Sam Ogden's provided API Key for LLGM
openai.api_key = "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"
MODEL = "gpt-3.5-turbo"

# Global Variables
# -------------------------------------------Paths:------------------------------------------
# Inputs
#   System Messages
#       Game Master (Context)
#       Formatter   (Context)
#       Chronicler  (Context)
#
#   Runtime Injections
#       Game Master (User Input)
#       SDPrompter (Prompt)
#
# Outputs
#   LLGM Narration
#   Stable Diffusion Image
#   
#
# Logs (GPT ChatCompletion Dumps)
#   Game Master Log
#   Formatter   Log
#   Chronicler  Log

# Universal (Hard-Coded Static Config File Locations)
PATH_CONTEXT_GAMEMASTER          = "GPT/System/GameAnalyst.txt"
PATH_CONTEXT_SDPROMTER           = "GPT/System/SDPrompter.txt"
PATH_CONTEXT_CHRONICLER          = "GPT/System/Chronicler.txt"

PATH_SDCONFIG_NEGATIVE           = "StableDiffusion/Input/NegativePrompt.txt"
PATH_SDCONFIG_CONFIG             = "StableDiffusion/Input/Payload.txt"

# Temp/Overwritten
PATH_SDCONFIG_PROMPT             = "StableDiffusion/Input/Prompt.txt"
PATH_INPUT_USER                  = "GPT/Input/User_input.txt"

# Use time of creation as placeholder campaign name
campaign = str(datetime.now().strftime("%m-%d-%Y (%I.%M.%S %p)"))
if not os.path.exists(f"GPT/Campaigns/{campaign}"):
    os.makedirs(f'GPT/Campaigns/{campaign}')


# Instance Logs (Campaign-specific ChatCompletion Dumps)
PATH_OUTPUT_GAMEMASTER           = f"GPT/Campaigns/{campaign}/OUTPUT_GAMEMASTER.txt"
#PATH_OUTPUT_SDPROMPTER           = f"GPT/Campaigns/{campaign}/OUTPUT_SDPROMPTER.txt"
PATH_OUTPUT_CHRONICLER           = f"GPT/Campaigns/{campaign}/OUTPUT_CHRONICLER.txt"
# NOTE: Chronicler output is overwritten (summary-of-summary to preserve tokens)
PATH_OUTPUT_STABLEDIFFUSION      = f"StableDiffusion/Output/{campaign}/"

PATH_LOG_GAMEMASTER              = f"GPT/Campaigns/{campaign}/LOG_GAMEMASTER.txt"
PATH_LOG_SDPROMPTER              = f"GPT/Campaigns/{campaign}/LOG_SDPROMPTER.txt"
PATH_LOG_CHRONICLER              = f"GPT/Campaigns/{campaign}/LOG_CHRONICLER.txt"


# -------------------------------------- Context_Vars: --------------------------------------
# Load contexts from disk
CONTEXT_GAMEMASTER   =   read(PATH_CONTEXT_GAMEMASTER)
CONTEXT_SDPROMTER    =   read(PATH_CONTEXT_SDPROMTER)
CONTEXT_CHRONICLER   =   read(PATH_CONTEXT_CHRONICLER)


# ------------------------------- Initialize Outputs & Logs: --------------------------------


write(PATH_OUTPUT_GAMEMASTER, "")
write(PATH_OUTPUT_CHRONICLER, "")
write(PATH_LOG_GAMEMASTER, "")
write(PATH_LOG_SDPROMPTER, "")
write(PATH_LOG_CHRONICLER, "")


# ================================ Functions: =======================================


def chronicler(gm_entry):
    print("[CHRONICLER]:", end=" ")

    # Send GameChronicler the response, to have it create a new summary.
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": CONTEXT_CHRONICLER},
            {"role": "user", "content": gm_entry}
        ]
    )
    # Dump Log to file
    append(PATH_LOG_CHRONICLER, str(completion))

    # Update the summary
    write(PATH_OUTPUT_CHRONICLER,str(completion.choices[0].message.content))
    #print(str(completion.choices[0].message.content))
    print("...done!")
    return 0


def gamemaster(user_input):
    print("[GAMEMASTER]:", end=" ")
    # Fetch the Chronicled history of this chat to inject into chat
    if not os.path.exists(PATH_OUTPUT_CHRONICLER):
        write(PATH_OUTPUT_CHRONICLER, "")

    summarized_history = read(PATH_OUTPUT_CHRONICLER)

    # Complete the ChatCompletion
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": CONTEXT_GAMEMASTER},
            {"role": "assistant", "content": summarized_history},
            {"role": "user", "content": user_input}
        ]
    )
    # Dump Log into file
    append(PATH_LOG_GAMEMASTER, str(completion))

    # Test GPT-JSON message structure
    # First, convert the message into a string, then trim the newlines.
    gpt_json = json.loads(str(completion.choices[0].message.content).replace("\n", ""))

    # Store natural-language response
    append(PATH_OUTPUT_GAMEMASTER, str(gpt_json["response"]))
    print(str(gpt_json["response"]))

    # Call Chronicler to update history
    chronicler(gpt_json["response"])
    return 0


def sdprompter():
    print("[SDPROMPTER]:", end=" ")

    # Fetch Chronicled Summary (WIP: Use JSON Location when mature)
    summary = read(PATH_OUTPUT_CHRONICLER)

    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": CONTEXT_SDPROMTER},
            {"role": "user", "content": summary}
        ]
    )
    # Dump Log into file
    append(PATH_LOG_SDPROMPTER, str(completion))

    # Currently, PATH_OUTPUT_SDPROMPTER  is commented out because I can't imagine a scenario where it'll be read

    # Forward output to prompt location for StableDiffusion
    write(PATH_SDCONFIG_PROMPT, str(completion.choices[0].message.content))
    print(str(completion.choices[0].message.content))

    # Invoke the local StableDiffusion instance to create an image based on the prompt
    StableDiffusion.generate()
    return 0


# ===================================================================================



# Print Greeting
print("Hello, and welcome to Ray's LLGM Prototype. \n"
      "I will be serving as your DM this session. \n"
      "Type \"Print Environ\" to generate an image \n"
      "Type \"exit\" to stop this program.")


# Main Loop Structure:
# Ask for input
# Evaluate Input
#   Reroute to GAMEMASTER
#   Reroute to SDPROMPTER
#       Load Prompt from disk (OUTPUT_CHRONICLER?


userInput = str(input())

while userInput != "exit":
    match userInput:
        case "Print Environ":
            sdprompter()

        case _:
            gamemaster(userInput)
    userInput = str(input())
print("Goodbye")