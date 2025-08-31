from rich import print

# Dictionnaire de l'horaire
schedule = {}
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

print("\nVoulez-vous [bold]activer la synthèse vocale[/bold] (oui/non) ?")
try:
	while True:
		text_to_speech_input = input("> ").lower()
		if text_to_speech_input == "oui":
			text_to_speech = True
			break
		elif text_to_speech_input == "non":
			text_to_speech = False
			break
		else:
			print("\n[bold red]Réponse invalide. Veuillez répondre par oui ou non.[/bold red]\n")
except KeyboardInterrupt:
	exit(0)

if text_to_speech == True:
	from yapper import Yapper, PiperSpeaker, PiperVoiceFrance

	speaker = PiperSpeaker(
		voice=PiperVoiceFrance.TOM  # You can choose any voice listed above
	)

	yapper = Yapper(speaker=speaker)

print("\nAppuyez sur [bold]󰘳 Ctrl / Cmd + C[/bold] pour quitter.", end='')
print("\nAppuyez sur [bold]󰌑 Enter[/ bold] pour continuer.")

# Change les variables et imprime la bonne entrée depuis le dictionnaire
print(f"\nJour {daycount} ───────────────────────", end='') # Méthode de paresseux
try:
	while True:
		input()
		if periodcount >= 4:
			periodcount = 1
			if daycount >= 9:
				daycount = 1
			else:
				daycount += 1
			print(f"\nJour {daycount} ───────────────────────")
			if text_to_speech == True:
				yapper.yap(f"Jour {daycount}")
		else:
			periodcount += 1

		print(f"  Période {periodcount}: {schedule[daycount][periodcount - 1]}", end='')
		if text_to_speech == True:
			yapper.yap(f"{schedule[daycount][periodcount - 1]}")

except KeyboardInterrupt:
	exit(0)
