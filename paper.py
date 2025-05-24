import sys

# Dictionnaire de l'horaire
def endofprogram():
    print("\n\n-- Fin du programme --")

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

# Variables de compteur
daycount = None
periodcount = 0

# Change la valeur de daycount pour une valeur choisie
while daycount not in range(1,9):
    try:
        daycount = int(input("Jour d'école pour commencer (1-9) -----\n> "))
    except ValueError:
        print("\nRéponse invalide.\n\n")
    except KeyboardInterrupt:
        endofprogram()
        sys.exit() # Quitte le programme

print("\nAppuie sur 󰌑 Enter pour continuer")

# Change les variables et imprime la bonne
# entrée depuis le dictionnaire
try:
    while True:
        input()
        if periodcount >= 4:
            periodcount = 1
            if daycount >= 9:
                daycount = 1
            else:
                daycount += 1
        else:
            periodcount += 1
        print(f"""
Jour {daycount} -----------------------
Période {periodcount}: {schedule[daycount][periodcount - 1]}
------------------------------
""")
# Code pour le Ctrl/Cmd+C
except KeyboardInterrupt:
    endofprogram()
