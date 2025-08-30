# Importations
from icalendar import Calendar, Event
from datetime import datetime, timedelta

# TODO: Faire un GUI

# Dictionnaire pour les blocs de temps
time_periods = {
	1: {"start": "9:15", "end": "10:30"},
	2: {"start": "10:50", "end": "12:05"},
	3: {"start": "13:20", "end": "14:35"},
	4: {"start": "14:55", "end": "16:10"}
}

# Dictionnaire pour l'horaire
schedule = {
	1: ["Période", "Période", "Période", "Période"],
	2: ["Période", "Période", "Période", "Période"],
	3: ["Période", "Période", "Période", "Période"],
	4: ["Période", "Période", "Période", "Période"],
	5: ["Période", "Période", "Période", "Période"],
	6: ["Période", "Période", "Période", "Période"],
	7: ["Période", "Période", "Période", "Période"],
	8: ["Période", "Période", "Période", "Période"],
	9: ["Période", "Période", "Période", "Période"]
}

# Informations
print("Le programme va créer un fichier ICS basé sur l'horaire spécifié dans le code.\n")

# Met les variables
scheduledaycount = int(input("À quel jour voulez-vous commencer? (1-9)\n> "))
daycount = datetime.strptime(input("Entre la date de début pour l'horaire (YYYY-MM-DD)\n> "), "%Y-%m-%d").date()

if input("Y a t'il des pédagos/congés dans la semaine? (oui/non)\n> ") == "oui":
	workingdays = [int(x.strip()) for x in input("Quels sont les jours de travail? (ex.: 1,2,3,4,5)\n> ").split(',')]
	# Convertit en integer - enlève les espaces - pour chaque x dans ex.: 1,2,3,4,5 - sépare
	# les valeurs dans une liste, supprime les virgules
else:
	workingdays = [1,2,3,4,5]

# Définit cal - variable sur laquelle on va travailler
cal = Calendar()

for i in range(1, 5+1):
	if i in workingdays:
		for index, eventcounter in enumerate(schedule[scheduledaycount], start=1):
			e = Event() # Définit e
			start_time = datetime.strptime(time_periods[index]["start"], "%H:%M").time() # Note la date de début
			end_time = datetime.strptime(time_periods[index]["end"], "%H:%M").time() # Note la date de fin
			e.add('summary', schedule[scheduledaycount][index-1]) # Ajoute le nom de l'événement
			e.add('dtstart', datetime.combine(daycount, start_time)) # Ajoute la date de début
			e.add('dtend', datetime.combine(daycount, end_time)) # Ajoute la date de fin
			cal.add_component(e) # FIN

		# Compteur de journées d'école
		if scheduledaycount >= 9:
			scheduledaycount = 1
		else:
			scheduledaycount = scheduledaycount + 1

	# Ajoute 1 au compteur de jour réels
	daycount = daycount + timedelta(days=1)

# Écrit le contenu dans un fichier ics
with open('calendar.ics', 'wb') as f:
	f.write(cal.to_ical())


# Informations
print("""
Un fichier ICS a été enregistré. Vous pouvez l'importer
dans votre application de calendrier existante.""")
