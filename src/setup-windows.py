# Script should only be ran on a fresh install -nugget
import os, time, json


###> attempts to change running directory to root if not already there -nugget
if not os.path.exists("src"):
    os.chdir("..")
###! -nugget
###> check if in the right directory, and exit if not -nugget
if not os.path.exists("src"):
    exit(
        "Error: couldn't find src directory, make sure to run setup.py from the root directory"
    )
###! -nugget

# checks for firebase.json
if not os.path.exists("data/firebase.json"):
    exit(
        "firebase.json not found, get it from https://console.firebase.google.com, then run setup.py again"
    )
# gets token
token = input("Please enter your Discord bot token: ")
with open("data/token.json") as f:
    data = json.load(f)
    token = data["token"]


###> check if virtual environment is active or not -nugget
def is_virtualenv():
    return "VIRTUAL_ENV" in os.environ


if not is_virtualenv():
    # if pyvenv.cfg exists, attempt to activate
    if os.path.exists("pyvenv.cfg"):
        print("Trying to activate virtual environment.")
        try:
            os.system("source Scripts/activate")
        except:
            exit(
                "Failed to activate virtual environment.\n Please run setup.py from inside the virtual environment."
            )
    else:
        print("Creating virtual environment.")
        venv = input("Name your venv: ")
        os.system(f"python -m venv {venv}")
        os.system(f"source {venv}/Scripts/activate")
###! -nugget


# installs dependencies
os.system("pip install -r requirements.txt")


# starts the bot
print("Starting bot...\n Run main.py to start the bot again.")
time.wait(5)
os.system("python main.py")
