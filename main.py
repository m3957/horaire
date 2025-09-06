#!/usr/bin/env python

from rich import print
from platform import system
import functions

# Programme de générateur de fichier ICS
def generateur_de_fichier_ics():
	# Dictionnaire pour les blocs de temps
	# TODO: déplacer ça dans un fichier txt
	time_periods = {
		1: {"start": "9:15", "end": "10:30"},
		2: {"start": "10:50", "end": "12:05"},
		3: {"start": "13:20", "end": "14:35"},
		4: {"start": "14:55", "end": "16:10"}
	}

	nom_fichier = functions.selecteur_fichiers()							# Affiche le sélecteur de fichiers
	schedule = functions.convert_txt_file_to_schedule(nom_fichier)			# Convertit le fichier txt sélectionné en dictionnaire

	functions.avertissement_responsabilite()								# Imprime l'avertissement de responsabilité

	scheduledaycount = functions.option_jour_ecole_commencement()			# Option: jour d'école de commencement (1 - 9)
	daycount = functions.option_date_commencement_evenements()				# Option: date de commencement des événements
	workingdays = functions.option_conges_semaine()							# Option: congés/pédagogiques dans la semaine

	functions.information_creation_fichier_ics()							# Informe l'utilisateur que le fichier va être créé

	functions.generate_ics_file(workingdays, schedule, scheduledaycount,	# Génère un fichier ICS
								time_periods, daycount)

	functions.information_fichier_ics_cree()								# Informe l'utilisateur que le fichier a été créé

# Programme papier.py
def papier():
	nom_fichier = functions.selecteur_fichiers()						# Affiche le sélecteur de fichiers
	schedule = functions.convert_txt_file_to_schedule(nom_fichier)		# Convertit le fichier txt sélectionné en dictionnaire
	functions.avertissement_responsabilite()							# Imprime l'avertissement de responsabilité
	daycount = functions.option_jour_ecole_commencement()				# Option: demande pour le jour de commencement

	# TODO: faire que la synthèse vocale fonctionne partout
	if system() == "Linux":
		text_to_speech = functions.option_text_to_speech()				# Option: demande pour la synthèse vocale (Linux seulement)
	else:
		text_to_speech = 2												# Désactive la synthèse vocale si le système n'est pas supporté

	if text_to_speech == 1 or text_to_speech == 3:						# Si la synthèse vocale est activée, l'initaliser
		functions.initialisation_text_to_speech(text_to_speech)

	functions.continuation_progr_av_stage_final()						# Imprime l'information avant de commencer la boucle
	functions.affichage_periodes(schedule, daycount, text_to_speech)	# Affichage des périodes, ex.: Jour 1, Période, etc.

def option_menu_principal():
	while True:
		try:
			print("""[bold]Programme d'horaire scolaire[/bold]
Veuillez sélectionner une option (1 ou 2):

1. Générateur de fichier ICS
     Génère un fichier ICS importable dans une application de
     calendrier avec dedans les périodes scolaires pour la semaine.
2. Copie de périodes dans l'agenda papier
     Affiche la prochaine période à écrire dans l'agenda et l'énonce
     au besoin pour faciliter la copie de celles-ci dans l'agenda.
""")
			selection_utilisateur_menu = int(input("> "))
			if selection_utilisateur_menu == 1:
				generateur_de_fichier_ics()
				exit(0)
			elif selection_utilisateur_menu == 2:
				papier()
				exit(0)
			else:
				print("\n[bold red]Réponse invalide. Veuillez répondre par 1 ou 2.[/bold red]\n")
		except KeyboardInterrupt:
			exit(0)

if __name__ == "__main__":
	option_menu_principal()
