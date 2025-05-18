import os
import re
import argparse
from datetime import date
from openai import OpenAI
from dotenv import load_dotenv

TRANSCRIPT_DIR = "transcripts"
SOAP_DIR = "outputs/soap_notes"
FINAL_DIR = "outputs/soap_notes_final"

os.makedirs(FINAL_DIR, exist_ok=True)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_fields_with_llm(transcript):
    prompt = f"""Extract the following structured fields from the transcript below.
        Make sure to remember that certain fields might be in conversational format.
      If a field is not present, return an empty string.
      Do not include anything not present in the input.

Fields to extract:
- Client Full Name
- Client Date of Birth
- Exact start time and end time
- Session Location

Return the result as a JSON dictionary.

Transcript:
""{transcript}""
"""


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    import json
    try:
        content = response.choices[0].message.content
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        return {}

def parse_structured_fields(transcript):
    name_match = re.search(r"My name is\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", transcript)
    dob_match = re.search(r"date of birth.*?(?:is\s+)?(\w+\s+\d{1,2},\s+\d{4})", transcript, re.IGNORECASE)
    if not dob_match:
        dob_match = re.search(r"born on\s+(\w+\s+\d{1,2},\s+\d{4})", transcript, re.IGNORECASE)
    if not dob_match:
        dob_match = re.search(r"(?:birthday is|I was born on)\s+(\w+\s+\d{1,2})", transcript, re.IGNORECASE)

    fields = {
        "Client Full Name": name_match.group(1).strip() if name_match else "",
        "Client Date of Birth": dob_match.group(1).strip() if dob_match else "",
        "Date of Service": "",
        "Exact start time and end time": "",
        "Session Location": ""
    }

    if not fields["Client Full Name"] or not fields["Client Date of Birth"]:
        llm_fields = extract_fields_with_llm(transcript)
        for key in fields:
            if not fields[key] and key in llm_fields:
                fields[key] = llm_fields[key]

    return fields

def format_soap_output(transcript, soap_body):
    llm_fields = {}
    for key in [
        "Client Full Name", "Client Date of Birth", "Date of Service",
        "Exact start time and end time", "Session Location"
    ]:
        match = re.search(rf"{re.escape(key)}:\\s*(.*)", soap_body)
        llm_fields[key] = match.group(1).strip() if match else ""

    parsed_fields = parse_structured_fields(transcript)
    merged_fields = {}
    for key in llm_fields:
        merged_fields[key] = llm_fields[key] or parsed_fields[key]

    # Remove any duplicated structured header (before the SOAP sections)
    soap_body = re.sub(
        r"^(Client Full Name:.*?Session Location:\s*.*?)\n(?=\s*(###\s+)?Diagnosis:)",
        "",
        soap_body,
        flags=re.DOTALL | re.IGNORECASE
    )

    soap_body = re.sub(r"\bDiagnosis:\b", "### Diagnosis", soap_body)
    soap_body = re.sub(r"\bSubjective:\b", "### Subjective", soap_body)
    soap_body = re.sub(r"\bObjective:\b", "### Objective", soap_body)
    soap_body = re.sub(r"\bAssessment:\b", "### Assessment", soap_body)
    soap_body = re.sub(r"\bPlan:\b", "### Plan", soap_body)
    soap_body = re.sub(r"Therapist Signature:", "### Therapist Signature\nTherapist Signature:", soap_body)

    header_lines = [
        f"{key}: {merged_fields[key]}" for key in [
            "Client Full Name", "Client Date of Birth", "Date of Service",
            "Exact start time and end time", "Session Location",
        ]
    ] + [""]

    return "\n".join(header_lines) + "\n" + soap_body.strip()

def main(convert_to_pdf=False):
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.startswith("encounter_") and filename.endswith(".txt"):
            base = filename.replace(".txt", "")
            transcript_path = os.path.join(TRANSCRIPT_DIR, filename)
            soap_path = os.path.join(SOAP_DIR, base + "_soap.md")
            final_path = os.path.join(FINAL_DIR, base + "_soap_final.md")

            if os.path.exists(transcript_path) and os.path.exists(soap_path):
                with open(transcript_path, "r") as tf:
                    transcript = tf.read()
                with open(soap_path, "r") as sf:
                    soap = sf.read()

                formatted = format_soap_output(transcript, soap)
                with open(final_path, "w") as out:
                    out.write(formatted)
                print(f"Saved: {final_path}")

    if convert_to_pdf:
        print("📄 Converting to PDF using convert_md_to_pdf.sh...")
        os.system("bash convert_md_to_pdf.sh")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format SOAP notes and optionally convert to PDF.")
    parser.add_argument("--convert", action="store_true", help="Convert final markdown to PDF after formatting (default: off)")
    args = parser.parse_args()

    main(convert_to_pdf=args.convert)
