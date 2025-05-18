import os
from llm_client import call_llm
from utils import load_transcript, save_output, load_prompt_template

TRANSCRIPTS_DIR = "transcripts"
OUTPUT_DIR = "outputs/soap_notes"
PROMPT_PATH = "prompts/soap_prompt_template.txt"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)      

# Function to generate SOAP notes from transcripts
# using a pre-defined prompt template
# and the OpenAI API
# It loads the transcript from the specified directory,
# formats it with the prompt template,
# and calls the LLM to generate the SOAP note
# The generated note is saved in the specified output directory
# The function iterates over all transcript files in the directory
# and generates a SOAP note for each one
def generate_notes():
    prompt_template = load_prompt_template(PROMPT_PATH)

    for filename in os.listdir(TRANSCRIPTS_DIR):
        if filename.endswith(".txt"):
            input_path = os.path.join(TRANSCRIPTS_DIR, filename)
            transcript = load_transcript(input_path)
            full_prompt = prompt_template.format(transcript=transcript)
            note = call_llm(full_prompt)
            base_name = filename.replace(".txt", "_soap")
            md_path = os.path.join(OUTPUT_DIR, f"{base_name}.md")
            save_output(note, md_path)
            print(f"✅ Generated: {md_path}")

if __name__ == "__main__":
    generate_notes()
