import csv
from user import User


def read_raw_events(filename):
    try: 
        file = open(filename, 'r')
    except:
        print("Impossible d'ouvrir le fichier : " + filename)
        return
    reader = csv.reader(file)
    for row in reader:
        print(row)