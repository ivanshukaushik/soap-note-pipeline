# This code is part of the Agentic EMR project, which aims to create an
# intelligent EMR system using LLMs and various agents.
# The code below generates a flowchart of the EMR processing pipeline using Graphviz.

import graphviz

# Flowchart
dot = graphviz.Digraph(format='png')
dot.attr(rankdir='TB', size='10')

dot.node("Transcript", "Raw Clinical Transcript")
dot.node("Preprocess", "Preprocessing Agent\n(NER + Sectioning)")
dot.node("Planner", "Planner / Orchestrator\n(Agent Routing + Planning)")
dot.node("RetrieverA", "Retriever A\n(Medical KB)")
dot.node("RetrieverB", "Retriever B\n(Patient History)")
dot.node("Validator", "Validator Agent\n(Fact/Guideline Checking)")
dot.node("Calculator", "Calculator Tool\n(Medical Risk Scores)")
dot.node("Fusion", "Context Fusion Agent\n(Combine Context + Transcript)")
dot.node("Generator", "LLM Generator Agent\n(EMR Draft Creation)")
dot.node("Postprocess", "Postprocessor Agent\n(HL7/FHIR Cleanup)")
dot.node("Output", "Final EMR Note")

dot.edges([
    ("Transcript", "Preprocess"),
    ("Preprocess", "Planner"),
    ("Planner", "RetrieverA"),
    ("Planner", "RetrieverB"),
    ("RetrieverA", "Validator"),
    ("RetrieverB", "Calculator"),
    ("Validator", "Fusion"),
    ("Calculator", "Fusion"),
    ("Planner", "Fusion"),
    ("Fusion", "Generator"),
    ("Generator", "Postprocess"),
    ("Postprocess", "Output")
])

flowchart_path = "outputs/flowchart2"
dot.attr(dpi='300')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
dot.attr('edge', color='black')
dot.attr('graph', fontsize='20')
dot.render(flowchart_path, cleanup=True)
