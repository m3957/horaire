from rich import print
from tkinter import filedialog
import random

# Dictionnaire de l'horaire
schedule = {}

# Importe l'horaire du fichier texte vers le programme
try:
	# Message d'erreur pour la sélection de fichiers, pas me répéter
	message_erreur_fichier = """[bold red] Veuillez sélectionner le bon fichier. Celui-ci devrait avoir
neuf lignes, chacune commençant par Jour 1, 2, etc. comme ceci:[/bold red]
─ [bold]horaire.txt[/bold] ─────────────────────────────────────
Jour 1: Période 1, Période 2, Période 3, Période 4
Jour 2: Période 1, Période 2, Période 3, Période 4
...
Jour 8: Période 1, Période 2, Période 3, Période 4
Jour 9: Période 1, Période 2, Période 3, Période 4
───────────────────────────────────────────────────"""

	print("""
[bold]Veuillez sélectionner le fichier d'horaire.[/bold]
Appuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.
""", end='')
	input()

	nom_fichier = filedialog.askopenfilename(filetypes=[("Fichiers textes", "*.txt")]) # Ouvre le sélecteur de fichiers Tkinter

	if nom_fichier.endswith('.txt'):
		texte = open(nom_fichier)
		if texte.read(7) == "Jour 1:":
			pass
		else:
			print(message_erreur_fichier)
			exit(0)
	else:
		print(message_erreur_fichier)
		exit(0)
except KeyboardInterrupt:
	exit(0)
except:
	# User clicked cancel in the file dialog or another error occurred
	print("[bold yellow]Sélection de fichier annulée.[/bold yellow]")
	exit(0)

with open("horaire.txt", "r", encoding="utf-8") as f:
	for line in f:
		line = line.strip()
		if not line:
			continue
		# Sépare à la colonne pour séparer le jour et les périodes
		day_part, periods_part = line.split(":", 1)
		# Extrait le chiffre du jour
		day_number = int(day_part.replace("Jour", "").strip())
		# Sépare les périodes et enlève les espaces
		periods = [p.strip() for p in periods_part.split(",")]
		schedule[day_number] = periods

# Variables de compteur
daycount = 0
periodcount = 0

# Avertissement
try:
	print("""[bold red] L'horaire choisi ne vient avec aucune responsabilité. Celui-ci[/bold red]
[bold red]peut contenir des erreurs non présentes dans la version papier.[/bold red]

Appuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.
	""")
	input()
except KeyboardInterrupt:
	exit(0)

# Change la valeur de daycount pour une valeur choisie
while True:
	try:
		print("[bold]Par quel jour d'école voulez-vous commencer (1 - 9)[/bold] ?")
		daycount = int(input("> "))
		if 1 <= daycount <= 9:
			break
		else:
			print("\n[bold red]Réponse invalide. Le nombre doit être entre 1 et 9.[/bold red]\n")
	except ValueError:
		print("\n[bold red]Réponse invalide. Veuillez entrer un nombre.[/bold red]\n")
	except KeyboardInterrupt:
		exit(0)

# Text to speech:
# 1: activé
# 2: désactivé
# 3: aléatoire activé
# 4: aléatoire désactivé
try:
	while True:
		print("\nVoulez-vous [bold]activer la synthèse vocale[/bold] (oui/non) ?")
		text_to_speech_input = input("> ").lower()
		if text_to_speech_input == "oui":
			text_to_speech = 1
			break
		elif text_to_speech_input == "non":
			text_to_speech = 2
			break
		if text_to_speech_input == "peut-être":
			print("\nTu n'es pas sûr? Bon, je continue, alors.")
			text_to_speech = 3
			break
		else:
			print("\n[bold red]Réponse invalide. Veuillez répondre par oui ou non.[/bold red]")
except KeyboardInterrupt:
	exit(0)

if text_to_speech == 1 or text_to_speech == 3:
	from yapper import Yapper, PiperSpeaker, PiperVoiceFrance

	speaker = PiperSpeaker(
		voice=PiperVoiceFrance.TOM  # You can choose any voice listed above
	)

	yapper = Yapper(speaker=speaker)

	if text_to_speech == 3:
		yapper.yap(f"T'es pas sûr? Bon, je continue alors.")

print("\nAppuyez sur [bold]󰘳 Ctrl / Cmd + C[/bold] pour quitter.", end='')
print("\nAppuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.")

try:
	input()
except KeyboardInterrupt:
	print("[bold yellow]Programme quitté.[/bold yellow]")
	exit(0)


# Change les variables et imprime la bonne entrée depuis le dictionnaire

# Méthode de paresseux
print(f"\nJour {daycount} ───────────────────────", end='')
if text_to_speech == 1:
	yapper.yap(f"Jour {daycount}")

try:
	while True:
		if text_to_speech >= 3:
			text_to_speech = random.randint(3, 4)

		input()
		if periodcount >= 4:
			periodcount = 1
			if daycount >= 9:
				daycount = 1
			else:
				daycount += 1
			print(f"\nJour {daycount} ───────────────────────")
			if text_to_speech == 1 or text_to_speech == 3:
				yapper.yap(f"Jour {daycount}")
		else:
			periodcount += 1

		print(f"  Période {periodcount}: {schedule[daycount][periodcount - 1]}", end='')
		if text_to_speech == 1 or text_to_speech == 3:
			yapper.yap(f"{schedule[daycount][periodcount - 1]}")

except KeyboardInterrupt:
	exit(0)
