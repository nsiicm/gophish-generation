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

def read_results(filename):
    users=[]
    try: 
        file = open(filename, 'r')
    except:
        print("Impossible d'ouvrir le fichier : " + filename)
        return
    reader = csv.reader(file)
    for row in reader:
        users.append(User(row[9], row[10], row[8], row[0], row[1]))
    return users