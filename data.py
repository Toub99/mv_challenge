from datasets import load_dataset
import argparse
from huggingface_hub import InferenceClient

# data = load_dataset("ncbi/Open-Patients", split="train")
bearer_token = "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"

prompt = """Please create a short medical report only including sections about Patient
        History, Clinical Findings + Diagnosis and Treatment Options based on this Patient description: """
max_tokens = 700

def valid_args():
    args = parser.parse_args()
    try:
        file = open(args.patient_desc, "r")
    except:
        print("Please provide a valid file path")
    else:
        return file.read()

def inference(patient_desc: str):
    client = InferenceClient("mistralai/Mistral-Nemo-Instruct-2407", token=bearer_token)
    res = client.text_generation(prompt + patient_desc, max_new_tokens=max_tokens)
    print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="mv_challenge", description="CLI for automatically creating medical reports based on patient descriptions")
    parser.add_argument("patient_desc", type=str, help="path to patient description as txt file")
    patient_desc = valid_args()
    inference(patient_desc)