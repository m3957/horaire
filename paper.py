# Importations
from yapper import Yapper, PiperSpeaker, PiperVoiceFrance
from rich import print
import random

def selecteur_fichiers():
	# Ouvre un dialogue de sélection de fichiers avec Tkinter pour que
	# l'utilisateur sélectionne un fichier texte contenant l'horaire voulu.
	#
	# Inclut une détection des erreurs de base qui feraient
	# que le fichier sélectionné serait invalide pour le reste du programme.

	from tkinter import filedialog # Importe filedialog depuis Tkinter

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

		nom_fichier = filedialog.askopenfilename(filetypes=[("Fichiers textes", "*.txt")]) # Ouvre le sélecteur de fichiers

		# Vérifie si le nom du fichier finit avec txt
		if nom_fichier.endswith('.txt'):
			texte = open(nom_fichier)

			# Si oui, vérifie si le fichire commence avec "Jour 1:"
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
		# Indique que la sélection a été annulée, occure si l'utilisateur
		# ferme la boîte de dialogue ou un autre problème mystérieux a été trouvé.
		print("[bold yellow]Sélection de fichier annulée.[/bold yellow]")
		exit(0)

	return nom_fichier # Retourne le nom du fichier, ex.: "horaire.txt"

def convert_txt_file_to_schedule(nom_fichier):
	# Convertit le fichier texte sélectionné avec selecteur_fichiers()
	# en dictionnaire schedule utilisable par le reste des fonctions

	schedule = {} # Initie le dictionnaire schedule

	# Trucs faits par IA, désolé, j'y comprends pas grand chose
	# Moi <- vrai pro de la langue du serpent (HMM)
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

	return schedule # Retourne le dictionnaire schedule

def avertissement_responsabilite():
	# Imprime un avertissement de responsabilité
	try:
		print("""[bold yellow] L'horaire choisi ne vient avec aucune responsabilité. Celui-ci
peut contenir des erreurs non présentes dans la version papier.[/bold yellow]

Appuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.
	""")
		input()
	except KeyboardInterrupt:
		exit(0)

def option_jour_ecole_commencement():
	# Modifie la valeur daycount pour une choisie par l'utilisateur,
	# pour commencer l'impression des jours pas nécessairement par 1

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
	# Modifie la valeur text_to_speech pour une choisie par l'utilisateur,
	# pour avoir ou non de la synthèse vocale dans l'impression des jours
	#
	# Valeurs mises par le programme:
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
				# Easter egg parce que pourquoi pas?
				return 3
			else:
				print("\n[bold red]Réponse invalide. Veuillez répondre par oui ou non.[/bold red]")
	except KeyboardInterrupt:
		exit(0)

def initialisation_text_to_speech(text_to_speech):
	# Initialise les trucs de yapper

	speaker = PiperSpeaker(
		# TODO: Régler l'erreur (même si elle n'affecte rien au runtime)
		voice=PiperVoiceFrance.TOM
	)

	global yapper
	yapper = Yapper(speaker=speaker)

	if text_to_speech == 3:
		# Message drôle se passant
		print("\nTu n'es pas sûr? Bon, je continue, alors.")
		yapper.yap("T'es pas sûr? Bon, je continue alors.")

def continuation_progr_av_stage_final():
	# Petit message informant les utilisateurs comment quitter
	# le programme au besoin, puisqu'il va être dans une boucle infinie

	print("\nAppuyez sur [bold]󰘳 Ctrl / Cmd + C[/bold] pour quitter.", end='')
	print("\nAppuyez sur [bold]󰌑 Entrée[/ bold] pour continuer.")

	try:
		input()
	except KeyboardInterrupt:
		print("[bold yellow]Programme quitté.[/bold yellow]")
		exit(0)

def affichage_periodes(schedule, daycount, text_to_speech):
	periodcount = 0 # Variable de compteur

	# Méthode de paresseux
	print(f"Jour {daycount} ───────────────────────", end='')
	if text_to_speech == 1:
		yapper.yap(f"Jour {daycount}")

	# La grande boucle compliquée, terminant le programme papier
	try:
		while True:
			if text_to_speech >= 3:
				# Aléatoire-ise le text to speech avec l'easter egg "peut-être"
				text_to_speech = random.randint(3, 4)

			# Si périodecount est plus gros que 4, remet à 1
			if periodcount >= 4:
				periodcount = 1

				# Si daycount est plus gros que 9, remet à 1
				if daycount >= 9:
					daycount = 1
				else:
					# Sinon, augmente le compte de la journée
					daycount += 1

				# Imprime la prochaine journée
				print(f"\n\nJour {daycount} ───────────────────────", end='')

				# YAP la prochaine journée au nécessaire
				if text_to_speech == 1 or text_to_speech == 3:
					yapper.yap(f"Jour {daycount}")
			else:
				# Si le compte de période n'est pas >= 4, augmente
				periodcount += 1

			input()

			# Imprime la période qui doit être écrite dans l'agenda
			print(f"  Période {periodcount}: {schedule[daycount][periodcount - 1]}", end='')

			# YAP la période qui doit être écrite dans l'agenda
			if text_to_speech == 1 or text_to_speech == 3:
				yapper.yap(f"{schedule[daycount][periodcount - 1]}")

	except KeyboardInterrupt:
		exit(0)


# Programme papier.py
def main():
	nom_fichier = selecteur_fichiers()						# Affiche le sélecteur de fichiers
	schedule = convert_txt_file_to_schedule(nom_fichier)	# Convertit le fichier txt sélectionné en dictionnaire
	avertissement_responsabilite()							# Imprime l'avertissement de responsabilité
	daycount = option_jour_ecole_commencement()				# Option: demande pour le jour de commencement
	text_to_speech = option_text_to_speech()				# Option: demande pour la synthèse vocale

	if text_to_speech == 1 or text_to_speech == 3:
		# Si la synthèse vocale est activée, l'initaliser
		initialisation_text_to_speech(text_to_speech)

	continuation_progr_av_stage_final()						# Imprime l'information avant de commencer la boucle
	affichage_periodes(schedule, daycount, text_to_speech)	# Affichage des périodes, ex.: Jour 1, Période, etc.

if __name__ == "__main__":
	main()
