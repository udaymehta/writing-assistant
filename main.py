import time
from string import Template
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import requests

controller = Controller()


PROMPT_TEMPLATE = Template(
    """"
    Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes. Do not add any new information like "Sure, here is the revised text:" or "The corrected version is:" or anything like that. Just edit the text and make it as clear and correct as possible.
    
    $text
    """
)

MODEL = "gemma:2b-instruct-q5_K_M"

def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "keep_alive": "2m",
            "stream": False,
        },
    )
    response.raise_for_status()
    resp_json = response.json()
    return resp_json.get("response").strip()


def fix_selection():
    with controller.pressed(Key.ctrl):
        controller.tap("c")

    time.sleep(0.1)
    text = pyperclip.paste()

    if not text:
        return
    fixed_text = fix_text(text)
    if not fixed_text:
        return

    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    with controller.pressed(Key.ctrl):
        controller.tap("v")
    print("Text fixed and pasted!")


def on_press_f8(key):
    if key == Key.f8:
        fix_selection()


with keyboard.Listener(on_press=on_press_f8) as listener:
    listener.join()
