# LLDM-Proof-of-Concept
 ### Roll for Initiative!
 Secret Prototype 1 made in ~1 week? *(like 3 days, really)*
## Requirements: Working Internet Connection
    Install openai (pip3 install openai)
    Install PIL    (pip3 install Pillow)

 *It's using Python 3 so need to use pip3*

## How to run:
Run the **GPT.py** script

## Current Issues:
 1. GameMaster sometimes asks player for input, which derails Chronicler
 2. Chronicler SYSTEM prompt probably needs more refinement
 3. Since SDPrompter takes in a Chronicler summary as input, sometimes junk data ends up in the prompt.  
    But visually, this is often invisible.
 5. Remote Hosting URL for StableDiffusion will expire in <72 hours.  
    Instance is fine, running locally on my Desktop in Prom.  
    It's just that the gradio link hosted by the webapp will break.  
