import argparse
from user import User

parser = argparse.ArgumentParser(description='Creation de rapport avec exports Gophish') #Creation du parser d'arguments et ajout description

parser.add_argument("-e","--raw-events", help="Indiquer le fichier d'export Gophish Raw Events", required=False)
parser.add_argument("-r","--results", help="Indiquer le fichier d'export Gophish Resulsts", required=False)
parser.add_argument("-v","--verbose", action="store_true", help="Afficher les details de traitement", required=False)

args = parser.parse_args()


utilisateur = User("SIMON", "Nicolas", "n@a.a", "sdlfkjsqldfj")

print(utilisateur.nom)
