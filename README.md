# Horaire
Programme Python avec ces deux fonctions de paresseux:

1. **Générateur de fichier ICS**
	- Génère un fichier ICS importable dans une application de calendrier avec dedans les périodes scolaires pour la semaine.
2. **Copie de périodes dans l'agenda papier**
	- Affiche la prochaine période à écrire dans l'agenda et l'énonce au besoin pour faciliter la copie de celles-ci dans l'agenda.

## Usage
Le programme peut être exécuté à partir du fichier Python ou depuis le fichier .exe fait par Github Actions.

### À partir du fichier
```bash
# Clone le projet
git clone https://github.com/m3957/Horaire

# Installe les dépendances
pip install -r requirements.txt

# Exécute le programme
python3 main.py
```

### À partir de Github Actions
Github Actions compile automatiquement le programme dans un fichier exécutable pour Windows et Linux.
Ceux-ci peuvent être téléchargés depuis la section Releases dans la colonne droite.

## Compilation
```bash
# Installe les dépendances si pas déjà fait
pip install -r requirements.txt

# Installe pyinstaller, compile et exécute le programme
pip install pyinstaller
pyinstaller --onefile main.py

chmod +x dist/main
./dist/main
```
