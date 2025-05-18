import graphviz
import os
from dotenv import load_dotenv

output_path = "./outputs/flowchart"

dot = graphviz.Digraph(format='png')
dot.attr(rankdir='LR', size='10')

dot.node("Transcript", "Raw Clinical Transcript")
dot.node("Pre", "Preprocessing (NER + Sectioning)")
dot.node("QEnc", "Query Encoder\n(DPR or ColBERT)")
dot.node("Index", "Clinical KB Index\n(FAISS/Vector DB)")
dot.node("Patient", "Patient-Specific\nContext Memory")
dot.node("Ctx", "Top-K Retrieved Context")
dot.node("Fusion", "Context Fusion\n(Query + Retrieval)")
dot.node("Gen", "LLM Generator\n(T5 / GPT)")
dot.node("Post", "Postprocessing\n(Regex, HL7, PDF)")
dot.node("Output", "Final EMR Note")

dot.edges([
    ("Transcript", "Pre"),
    ("Pre", "QEnc"),
    ("QEnc", "Index"),
    ("QEnc", "Patient"),
    ("Index", "Ctx"),
    ("Patient", "Ctx"),
    ("Ctx", "Fusion"),
    ("Fusion", "Gen"),
    ("Gen", "Post"),
    ("Post", "Output")
])
dot.attr(dpi='300')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
dot.attr('edge', color='black')
dot.render(output_path, cleanup=True)

