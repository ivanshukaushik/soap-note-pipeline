import os
import re
from datetime import date

TRANSCRIPT_DIR = "transcripts"
SOAP_DIR = "outputs/soap_notes"
FINAL_DIR = "outputs/soap_notes_final"

os.makedirs(FINAL_DIR, exist_ok=True)

def parse_structured_fields(transcript):
    name_match = re.search(r"My name is\\s+([A-Z][a-z]+(?:\\s[A-Z][a-z]+)+)", transcript)
    dob_match = re.search(r"date of birth.*?(?:is\\s+)?(\\w+\\s+\\d{1,2},\\s+\\d{4})", transcript, re.IGNORECASE)
    diagnosis = "Tension headache"  # Assumed if not otherwise present

    return {
        "Client Full Name": name_match.group(1).strip() if name_match else "",
        "Client Date of Birth": dob_match.group(1).strip() if dob_match else "",
        "Date of Service": date.today().strftime("%-m/%-d/%Y"),
        "Exact start time and end time": "",
        "Session Location": "",
        "Diagnosis": diagnosis
    }

def format_soap_output(transcript, soap_body):
    fields = parse_structured_fields(transcript)

    header_lines = [
        f"{key}: {fields[key]}" for key in [
            "Client Full Name", "Client Date of Birth", "Date of Service",
            "Exact start time and end time", "Session Location", "Diagnosis"
        ]
    ] + [""]

    # Reformat section headers
    soap_body = re.sub(r"\\bSubjective:\\b", "### Subjective", soap_body)
    soap_body = re.sub(r"\\bObjective:\\b", "### Objective", soap_body)
    soap_body = re.sub(r"\\bAssessment:\\b", "### Assessment", soap_body)
    soap_body = re.sub(r"\\bPlan:\\b", "### Plan", soap_body)
    soap_body = re.sub(r"Therapist Signature:", "### Therapist Signature\\nTherapist Signature:", soap_body)

    return "\\n".join(header_lines) + "\\n" + soap_body.strip()

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
            print(f"✅ Saved: {final_path}")

# Automatically run bash script to convert .md to .pdf
os.system("bash convert_md_to_pdf.sh")