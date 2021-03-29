# Jeu de mathématique [2020.09.29]
import random

NBR_MIN = 1
NBR_MAX = 10
NBR_DE_QUESTIONS = 4

def addition(a,b) :
    return a + b

def soustraction(a,b) :
    return a - b

def multiplication(a,b):
    return a * b

def division(a,b):
    return a / b

def poser_une_question(a,b):
    c = random.randint(1,4)
    resultat = 0.0
    r = False
    try:
        if c == 1 :
            reponse = input(f"Que vaut la sommme : {a} + {b} = ? ")
            resultat = addition(a,b)
            if int(reponse) == resultat:
                r = True
        elif c == 2 :
            reponse = input(f"Que vaut la différence : {a} - {b} = ? ")
            resultat = soustraction(a, b)
            if int(reponse) == resultat:
                r = True
        elif c == 3 :
            reponse = input(f"Que vaut la multiplication : {a} * {b} = ? ")
            resultat = multiplication(a, b)
            if int(reponse) == resultat:
                r = True
        else :
            reponse = input(f"Que vaut la division : {a} / {b} = ? ")
            resultat = division(a, b)
            if float(reponse) == resultat:
                r = True
    except:
        print("Erreur - veuillez introduire un nombre ...")
    else:
        if r :
            print(f"Réponse exacte")
        else :
            print(f"Réponse inexacte. Le résutlat était {resultat}")
    return r

#Main
print(f"Jeu de maths - Nous allons vous poser une série de questions ({NBR_DE_QUESTIONS} au total)")
print(f"Le but est d'obtenir le meilleur score en répondant correctement aux questions...")

score = 0
for q in range(0, NBR_DE_QUESTIONS):
    # Choisir deux nombres entiers au hasard
    premier_nombre = random.randint(NBR_MIN, NBR_MAX)
    second_nombre = random.randint(NBR_MIN, NBR_MAX)
    # Poser une question aléatoire
    print(f"Question n° {str(q+1)} sur {NBR_DE_QUESTIONS}")
    if poser_une_question(premier_nombre, second_nombre):
        score += 1

print(f"Votre note finale est {score}/{NBR_DE_QUESTIONS}")
if score / NBR_DE_QUESTIONS == 1 :
    print("Bravo, 100% !")
elif score / NBR_DE_QUESTIONS >= 75/100 :
    print("Bien >= 75% ")
