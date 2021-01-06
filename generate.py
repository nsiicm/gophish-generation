import argparse
from user import User
from audit import Audit
from api import *
from report import Report


parser = argparse.ArgumentParser(description='Creation de rapport avec exports Gophish') #Creation du parser d'arguments et ajout description

parser.add_argument("-e","--raw-events", help="Indiquer le fichier d'export Gophish Raw Events", required=False)
parser.add_argument("-r","--results", help="Indiquer le fichier d'export Gophish Resulsts", required=False)
parser.add_argument("-v","--verbose", action="store_true", help="Afficher les details de traitement", required=False)

args = vars(parser.parse_args())

print("Searching for campaigns via API")
audit = Audit("DONNEES")
print(str(audit.len()) + " campaigns found : ")
print(audit.get_names())

rapport = Report(audit)
rapport.render("eee")
