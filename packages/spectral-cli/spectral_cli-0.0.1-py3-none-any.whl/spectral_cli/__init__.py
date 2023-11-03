from spectral_cli.abis.abis import load_abis
import os
CONFIG_PATH = os.path.expanduser("~/.spectral/config.ini")
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

ALCHEMY_URL = "https://eth-goerli.g.alchemy.com/v2/"
ABIS = load_abis()