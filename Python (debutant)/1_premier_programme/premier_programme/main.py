# This is a first sample Python script.
import random

prenom = ""
while not prenom:
    prenom = input("Quel est ton nom? ")
print("Hello, " + prenom)

# !!! une vraie constante n'existe pas en python !!!
NBR_DE_FOIS = 2

# function afficher_info
def afficher_info(nom, age, taille = 0.0):
    print(nom + " as " + str(age) + " ans...")
    print("L'année prochaine, il aura " + str(age + 1) + " ans")

    if 18 <= age < 50 :
        print("Tu es majeur")
    elif 50 <= age <= 65 :    
        print("Tu es vieux")
    elif age < 18 :
        print ("Tu es jeune et mineur")
    else:
        print("Tu es sénior et retraité")

    if not taille == 0:
        print("Ta taille est de " + str(taille) + " m")

# function demander_age
def demander_age(nom):
    age_int = 0
    while age_int <= 0:
        try:
            age_str = input(nom + " , quel est ton âge? ")
            age_int = int(age_str)
        except:
            print("L'âge doit être un nombre > 0. Merci")
    return age_int


# print(type(mon_age))
for i in range(0, NBR_DE_FOIS):
    print(str(i+1) + ") --- ")
    taille = 1.0 + i * random.random()
    age = demander_age(prenom)
    afficher_info(prenom, age, taille)

# print(prenom + " as " + str(age) + " ans...")
# print("L'année prochaine, il aura " + str(age + 1) + " ans")


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
"""def print_hi(mon_prenom):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {mon_prenom}')  # Press Ctrl+F8 to toggle the breakpoint.
"""

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
