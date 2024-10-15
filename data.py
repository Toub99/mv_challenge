# from datasets import load_dataset
import argparse

# data = load_dataset("ncbi/Open-Patients", split="train")

# print(data[0])

def valid_args():
    args = parser.parse_args()
    try:
        file = open(args.patient_desc, "r")
    except:
        print("Please provide a valid file path")
    else:
        return file.read()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="mv_challenge", description="CLI for automatically creating medical reports based on patient descriptions")
    parser.add_argument("patient_desc", type=str, help="path to patient description as txt file")
    valid_args()