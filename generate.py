import argparse

parser = argparse.ArgumentParser(description='Creation de rapport avec exports Gophish') #Creation du parser d'arguments et ajout description

parser.add_argument("--raw-events", help="Indiquer le fichier d'export Gophish Raw Events")
parser.add_argument("--results", help="Indiquer le fichier d'export Gophish Resulsts")

args = parser.parse_args()