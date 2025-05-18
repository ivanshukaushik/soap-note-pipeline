# 🩺 Transcript-to-SOAP Note Generation Pipeline

This project implements a reproducible and modular pipeline that converts raw medical transcripts into structured SOAP notes using Large Language Models (LLMs). The output mimics formal clinical documentation standards — suitable for integration with EMRs, internal QA tools, or downstream decision-support systems.

---

## 📋 What It Does

Given a transcript of a medical encounter (e.g., `encounter_1.txt`), this pipeline:
1. Extracts relevant information
2. Segregates it into `Subjective`, `Objective`, `Assessment`, and `Plan` sections
3. Formats the result into a clean Markdown-based SOAP note
4. Optionally converts it to PDF using `pandoc`
5. Strips duplicate headers and preserves LLM output when applicable

---

## 🧠 Design Philosophy

This pipeline emphasizes:
- **Readability** of the generated SOAP notes
- **Determinism**, via prompt engineering and low temperature sampling
- **Composability**, so individual modules (e.g., formatting, extraction, conversion) can be swapped or extended
- **LLM-efficiency**, by using LLMs only for tasks that truly require reasoning
- **Preservation of critical clinical fields**, especially avoiding any unintended modifications to fields like `Diagnosis`

---

## 📦 Folder Structure

```
.
├── transcripts/                 # Raw input transcripts (.txt)
├── prompts/                    # Prompt template for the LLM
├── outputs/
│   └── soap_notes/             # Raw LLM outputs (.md)
│   └── soap_notes_final/       # Cleaned + structured markdown notes
├── llm_client.py               # OpenAI API wrapper
├── soap_generator.py           # Main script: generates SOAP notes
├── format_soap_notes.py        # Polishes and structures raw LLM outputs
├── convert_final_md_to_pdf.sh  # Optional: converts all .md → .pdf via pandoc
└── README.md                   # You are here
```

---

## 🚀 How to Run

### Step 1: Install dependencies

```bash
pip install openai python-dotenv
brew install pandoc  # or use apt/choco if on Linux/Windows
```

### Step 2: Add your API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
```

### Step 3: Run the pipeline

```bash
python soap_generator.py           # Generates base SOAP .md files
python format_soap_notes.py        # Polishes and normalizes structure
bash convert_final_md_to_pdf.sh    # (Optional) Converts all final .md → .pdf
```

---

## ✨ Prompt Engineering Strategy

We use a **single-shot prompt** stored in `prompts/soap_prompt_template.txt`.  
The prompt is structured to:

- Instruct the LLM to output in clinical style
- Mimic real SOAP note language and tone
- Leave placeholders blank if not present in the input
- Avoid unnecessary speculation or hallucination

Temperature is set to `0.3` to encourage consistent, factual outputs.

---

## 🪄 Post-Processing

After generation, we:
- Fill in header fields like name and DOB using regex and LLM fallback
- Preserve fields like `Diagnosis` as-is from LLM output (no overwriting)
- Strip duplicated headers if present in raw LLM output
- Format headings as `### Subjective`, etc.
- Save both `.md` and optionally `.pdf` formats for downstream use

This separation of concerns makes the pipeline modular, maintainable, and safe for sensitive fields.

---

## 🔬 Limitations

- **Model dependency**: The accuracy relies on the quality of the LLM (e.g., GPT-3.5 or GPT-4).
- **Ambiguity**: If transcripts are ambiguous or noisy, outputs may be inconsistent.
- **Edge case formatting**: Markdown/PDF rendering may break if user adds emojis, unusual punctuation, etc.
- **No cross-document memory**: The model doesn't yet learn from multiple transcripts or carry history.
- **Diagnosis field protection** means that missing diagnoses are not auto-filled, even if LLM could infer them.

---

## 💡 Future Improvements

- Fine-tune a clinical model (e.g., BioGPT) on SOAP-style outputs
- Chain-of-thought prompting: generate bullet points → SOAP formatting
- Integrate named entity recognition (NER) to pre-tag symptoms, meds, etc.
- Export to FHIR or HL7-compatible formats
- Add CLI flags or web interface for batch processing

---

## 🤝 Contributing

Pull requests welcome! Let us know if you:
- Want to add a new EMR format
- Have a better clinical prompt

---

## 👨‍⚕️ Authors

Developed by Ivanshu,  


---

## 🧾 License

MIT License. Use freely, modify respectfully.
