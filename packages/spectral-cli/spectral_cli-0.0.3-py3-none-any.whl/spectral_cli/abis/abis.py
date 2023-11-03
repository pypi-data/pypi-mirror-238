import json
import os


def load_abi(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def load_abis():
    d = {}
    # Directory containing all the ABI files (change this to your specific path)
    # dir_path = "./spectral-ai-sdk/spectral_cli/abis"
    dir_path = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".json"):
                full_file_path = os.path.join(root, file)
                abi_dict = load_abi(full_file_path)
                contract_name, _ = os.path.splitext(file)
                d[contract_name] = abi_dict

    return d
