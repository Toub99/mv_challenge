from datasets import load_dataset
import argparse
from huggingface_hub import InferenceClient

# data = load_dataset("ncbi/Open-Patients", split="train")
bearer_token = "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"

prompt = """Please create a short medical report only including sections about Patient
        History, Clinical Findings + Diagnosis and Treatment Options based on this Patient description: {}"""
prompt_with_format = """Please create a short medical report with the following structure {},
        based on the following patient description: {}"""
max_tokens = 700

def valid_args():
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
    client = InferenceClient("mistralai/Mistral-Nemo-Instruct-2407", token=bearer_token)
    if format == "":
        res = client.text_generation(prompt.format(patient_desc), max_new_tokens=max_tokens)
        print(res)
    else:
        res = client.text_generation(prompt=prompt_with_format.format(format, patient_desc), max_new_tokens=max_tokens)
        print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="mv_challenge", description="CLI for automatically creating medical reports based on patient descriptions")
    parser.add_argument("patient_desc", type=str, help="path to patient description as txt file")
    parser.add_argument("--report_format", type=str, help="path to txt file containing wanted report format")
    patient_desc, format = valid_args()
    inference(patient_desc, format)