import os
import json

# Funktion zum Laden der Benutzerdaten aus einer Datei
def lade_benutzerdaten():
    datenbank_dateipfad = "benutzerdaten.json"

    # Überprüfe, ob die Datei bereits existiert
    if os.path.exists(datenbank_dateipfad):
        with open(datenbank_dateipfad, 'r') as datei:
            benutzerdaten = json.load(datei)
    else:
        # Standardbenutzerdaten, wenn die Datei nicht vorhanden ist
        benutzerdaten = {
            'benutzer1': 'passwort1',
            'benutzer2': 'passwort2',
            'benutzer3': 'passwort3',
        }

        # Speichere die Standardbenutzerdaten in der Datei
        with open(datenbank_dateipfad, 'w') as datei:
            json.dump(benutzerdaten, datei)

    return benutzerdaten

# Benutzerdatenbank laden
benutzerdatenbank = lade_benutzerdaten()

def login():
    benutzername = input("Benutzername: ")
    passwort = input("Passwort: ")

    # Überprüfe, ob der Benutzer existiert und das Passwort korrekt ist
    if benutzername in benutzerdatenbank and benutzerdatenbank[benutzername] == passwort:
        print("Login erfolgreich!")
    else:
        print("Falscher Benutzername oder falsches Passwort.")

# Beispielaufruf der Login-Funktion
login()
