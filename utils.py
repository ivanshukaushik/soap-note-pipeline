import os

def load_transcript(file_path):
    with open(file_path, "r") as f:
        return f.read()

def save_output(text, output_path):
    with open(output_path, "w") as f:
        f.write(text)

def load_prompt_template(path):
    with open(path, "r") as f:
        return f.read()
