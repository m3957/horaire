from yapper import Yapper, PiperSpeaker, PiperVoiceFrance
from rich import print
import random

# TODO: Ajouter des commentaires un peu partout

def selecteur_fichiers():
	# Ouvre un dialogue de sélection de fichiers avec Tkinter pour que
	# l'utilisateur sélectionne un fichier texte contenant l'horaire voulu.
	#
	# Inclut une détection des erreurs de base qui feraient
	# que le fichier sélectionné serait invalide pour le reste du programme.

	from tkinter import filedialog

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

	return nom_fichier

def convert_txt_file_to_schedule(nom_fichier):
	schedule = {} # Initie le dictionnaire schedule

	with open(nom_fichier or "", "r", encoding="utf-8") as f:
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

	return schedule

# Avertissement
def avertissement_responsabilite():
	try:
		print("""[bold red] L'horaire choisi ne vient avec aucune responsabilité. Celui-ci[/bold red]
[bold red]peut contenir des erreurs non présentes dans la version papier.[/bold red]

Appuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.
	""")
		input()
	except KeyboardInterrupt:
		exit(0)

# Change la valeur de daycount pour une valeur choisie
def option_jour_ecole_commencement():
	while True:
		try:
			print("[bold]Par quel jour d'école voulez-vous commencer (1 - 9)[/bold] ?")
			daycount = int(input("> "))
			if 1 <= daycount <= 9:
				return daycount
				break
			else:
				print("\n[bold red]Réponse invalide. Le nombre doit être entre 1 et 9.[/bold red]\n")
		except ValueError:
			print("\n[bold red]Réponse invalide. Veuillez entrer un nombre.[/bold red]\n")
		except KeyboardInterrupt:
			exit(0)

def option_text_to_speech():
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
				return 1
			elif text_to_speech_input == "non":
				return 2
			elif text_to_speech_input == "peut-être":
				print("\nTu n'es pas sûr? Bon, je continue, alors.")
				return 3
			else:
				print("\n[bold red]Réponse invalide. Veuillez répondre par oui ou non.[/bold red]")
	except KeyboardInterrupt:
		exit(0)

def initialisation_text_to_speech():
	# TODO: Régler l'erreur (même si elle n'affecte rien au runtime)
	speaker = PiperSpeaker(
		voice=PiperVoiceFrance.TOM
	)

	global yapper
	yapper = Yapper(speaker=speaker)

	if text_to_speech == 3:
		yapper.yap("T'es pas sûr? Bon, je continue alors.")

def continuation_progr_av_stage_final():
	print("\nAppuyez sur [bold]󰘳 Ctrl / Cmd + C[/bold] pour quitter.", end='')
	print("\nAppuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.")

	try:
		input()
	except KeyboardInterrupt:
		print("[bold yellow]Programme quitté.[/bold yellow]")
		exit(0)

# Méthode de paresseux
def affichage_periodes(daycount, text_to_speech):
	# Variables de compteur
	periodcount = 0

	print(f"\nJour {daycount} ───────────────────────", end='')
	if text_to_speech == 1:
		yapper.yap(f"Jour {daycount}")

	try:
		while True:
			if text_to_speech >= 3:
				text_to_speech = random.randint(3, 4)

			#input()
			if periodcount >= 4:
				periodcount = 1
				if daycount >= 9:
					daycount = 1
				else:
					daycount += 1
				print(f"\n\nJour {daycount} ───────────────────────", end='')
				if text_to_speech == 1 or text_to_speech == 3:
					yapper.yap(f"Jour {daycount}")
			else:
				periodcount += 1

			input()

			print(f"  Période {periodcount}: {schedule[daycount][periodcount - 1]}", end='')
			if text_to_speech == 1 or text_to_speech == 3:
				yapper.yap(f"{schedule[daycount][periodcount - 1]}")

	except KeyboardInterrupt:
		exit(0)

nom_fichier = selecteur_fichiers()
schedule = convert_txt_file_to_schedule(nom_fichier)
avertissement_responsabilite()
daycount = option_jour_ecole_commencement()
text_to_speech = option_text_to_speech()

if text_to_speech == 1 or text_to_speech == 3:
	initialisation_text_to_speech()

continuation_progr_av_stage_final()
affichage_periodes(daycount, text_to_speech)
