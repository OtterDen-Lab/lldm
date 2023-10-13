from .helpers.path_config import *
from .StableDiffusion import generate

import openai
import json


# openai.api_key = os.getenv("")
# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = "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"
MODEL = "gpt-3.5-turbo"


# ================================ Functions: =======================================

# ChatCompletion Method (So IDE will stop yelling at me for duplicated code)

def chat_complete(context_file, user_input):
    print("[OPENAI]: REQUEST SENT", end=" ")
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": context_file},
            {"role": "user", "content": user_input}
        ]
    )
    print("| RESPONSE RECEIVED")
    return completion


def chat_complete_assistant(context_file, user_input, assistant_pretext):
    print("[OPENAI] API REQUEST SENT")
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": context_file},
            {"role": "assistant", "content": assistant_pretext},
            {"role": "user", "content": user_input}
        ]
    )
    return completion


def chronicler(gm_entry):
    print("[CHRONICLER]:", end=" ")

    # Send GameChronicler the response, to have it create a new summary.
    completion = chat_complete(CONTEXT_CHRONICLER, gm_entry)

    # Dump Log to file
    append(PATH_LOG_CHRONICLER, str(completion))

    # Update the summary
    write(PATH_OUTPUT_CHRONICLER, str(completion.choices[0].message.content))
    # print(str(completion.choices[0].message.content))
    print(str(completion.choices[0].message.content))
    return str(completion.choices[0].message.content)


def gamemaster(user_input):
    print("[GAMEMASTER]:", end=" ")
    summarized_history = read(PATH_OUTPUT_CHRONICLER)

    # Complete the ChatCompletion
    completion = chat_complete_assistant(CONTEXT_GAMEMASTER, user_input, summarized_history)

    # Dump Log into file
    append(PATH_LOG_GAMEMASTER, str(completion))

    # Test GPT-JSON message structure
    # First, convert the message into a string, then trim the newlines.
    gpt_json = json.loads(str(completion.choices[0].message.content).replace("\n", ""))

    # Store natural-language response
    append(PATH_OUTPUT_GAMEMASTER, str(gpt_json["response"]))
    print (str(gpt_json["response"]))
    return str(gpt_json["response"])


def sdprompter():
    print("[SDPROMPTER]:", end=" ")

    # Fetch Chronicled Summary (WIP: Use JSON Location when mature)
    summary = read(PATH_OUTPUT_CHRONICLER)

    completion = chat_complete(CONTEXT_SDPROMTER, summary)

    # Dump Log into file
    append(PATH_LOG_SDPROMPTER, str(completion))

    # Currently, PATH_OUTPUT_SDPROMPTER  is commented out because I can't imagine a scenario where it'll be read

    # Forward output to prompt location for SD
    write(PATH_SDCONFIG_PROMPT, str(completion.choices[0].message.content))

    # Invoke the local SD instance to create an image based on the prompt
    print(str(completion.choices[0].message.content))
    return generate()


def process_input(user_input):
    match user_input:
        case "exit":
            raise Exception("Exited (using text)!")
        case _:
            return gamemaster(user_input)


def place_character(character_path):
    completion = chat_complete(CONTEXT_GAMESETUP, read(character_path))
    chronicler(completion.choices[0].message.content)
    return completion.choices[0].message.content


def place_player(Character):
    print("[GameSetup]:", end=" ")
    completion = chat_complete(CONTEXT_GAMESETUP, str(Character))
    chronicler(completion.choices[0].message.content)
    return str(completion.choices[0].message.content)


def print_image():
    return sdprompter()
