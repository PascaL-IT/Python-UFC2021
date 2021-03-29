# Le nombre magique (projet - niveau 1) @ 2020.09.28
import random

MIN_NBR_MAGIC = 1
MAX_NBR_MAGIC = 20
NBR_DE_VIES = 4

# Fonction demander un nombre à trouver
def demander_nbr() :
    nombre = MIN_NBR_MAGIC - 1
    while nombre < MIN_NBR_MAGIC or nombre > MAX_NBR_MAGIC :
        try:
            nombre = int(input("Quel est le nombre magique? "))
        except:
            print("Erreur... veuillez introduire un nombre entier entre "+ str(MIN_NBR_MAGIC) + " et " + str(MAX_NBR_MAGIC))

    return int(nombre)

# Génération du nombre magique (aléatoire)
nombre_aleatoire = random.randint(MIN_NBR_MAGIC,MAX_NBR_MAGIC)

nombre_propose = 0
compteur_vie = NBR_DE_VIES

#Introduction
print("Jeu - essayer de découvrir le nombre magique entre " + str(MIN_NBR_MAGIC) + " et " + str(MAX_NBR_MAGIC))

#Boucle
while  nombre_propose != nombre_aleatoire :

    nombre_propose = demander_nbr()

    if nombre_propose < nombre_aleatoire :
        print("Le nombre magique est plus grand ")
        compteur_vie -= 1

    elif nombre_propose > nombre_aleatoire :
        print("Le nombre magique est plus petit")
        compteur_vie -= 1

    else:
        print("Trouvé... Bravo!")
        break

    if compteur_vie == 0 :
        print("Désolé... perdu - le nombre magique était "+ str(nombre_aleatoire))
        break
