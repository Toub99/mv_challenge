# from datasets import load_dataset
import argparse
from huggingface_hub import InferenceClient
import spacy
from scispacy.linking import EntityLinker


bearer_token = "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"

prompt = """Please create a short medical report only including sections about Patient
        History, Clinical Findings + Diagnosis and Treatment Options based on this Patient description: {}"""
prompt_with_format = """Please create a short medical report with the following structure {},
        based on the following patient description: {}"""
prompt_with_external = """Use these definitions of medical terms: {} 
        to build a short medical report only including patient history, clinical findings,
        diagnosis and treatment options based on this patient description: {}"""
max_tokens = 700


# Validate file paths
def valid_args():
    """
    Validate command line arguments (e.g. file paths)
    @return: content of read files
    """
    args = parser.parse_args()
    try:
        desc_file = open(args.patient_desc, "r")
        if args.report_format:
            format_file = open(args.report_format, "r")
    except:
        print("Please provide a valid file path")
    else:
        return (desc_file.read(), format_file.read()) if args.report_format else (desc_file.read(), "")


def inference(patient_desc: str, format: str):
    """
    Utilizes huggingface inference API for generating medical reports
    @return: medical report as string
    """
    args = parser.parse_args()
    client = InferenceClient("mistralai/Mistral-Nemo-Instruct-2407", token=bearer_token)
    if args.external_info:
        external_info = str(entity_linking(patient_desc))
        report = client.text_generation(prompt=prompt_with_external.format(external_info, patient_desc), max_new_tokens=max_tokens)
        return report
    if format == "":
        report = client.text_generation(prompt.format(patient_desc), max_new_tokens=max_tokens)
        return report
    else:
        report = client.text_generation(prompt=prompt_with_format.format(format, patient_desc), max_new_tokens=max_tokens)
        return report
        

def entity_linking(patient_desc: str) -> list[tuple]:
    """
    Use scispacy NER and entity linking to get information about medical terms
    @return: list of tuples (entity, definition)
    """
    ents_defs = []
    # Load a pre-trained scispaCy model
    nlp = spacy.load("en_core_sci_sm")
    config = {
        "linker_name": "mesh",
        # "no_definition_threshold": 0.999,
        "filter_for_definitions": True,
        "max_entities_per_mention": 1,
        "threshold": 0.85
    }
    nlp.add_pipe("scispacy_linker", config=config)
    linker = nlp.get_pipe("scispacy_linker")

    # Process the text with the NER model
    doc = nlp(patient_desc)
    
    for ent in list(set(doc.ents)): # eliminate duplicates
        for kb_ent in ent._.kb_ents:
            ent_def = (ent, linker.kb.cui_to_entity[kb_ent[0]].definition) # get definitions from entity linker
            ents_defs.append(ent_def)
            
    return ents_defs
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="mv_challenge", description="CLI for automatically creating medical reports based on patient descriptions")
    parser.add_argument("patient_desc", type=str, help="path to patient description as txt file")
    parser.add_argument("--report_format", type=str, help="path to txt file containing wanted report format")
    parser.add_argument('--external_info', action=argparse.BooleanOptionalAction)    
    try:
        patient_desc, format = valid_args()
    except:
        print("Invalid arguments")
    else:
        report = inference(patient_desc, format)
        print(report)