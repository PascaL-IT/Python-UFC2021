# Dictionary samples - dictionnaries
personne = { "prenom" : 'Pascal' , "taille" : 1.80 , "age" : 50 }
print(personne)
print("Prénom de cette personne: " + personne['prenom'])


# Ajout d'une <k,V> - un simple str
personne['profession'] = "informaticien"
print(personne)

# Ajout d'une <k,V> - un tuple
personne['hobbies'] = ("VTT","marche","piano")
print(personne)

# Boucle sur les <K,V>
# for k in personne:
#     print(f"<{k},{personne[k]}>")

# A map of dico
enfants = {
    "Térence" : { "prenom" : 'Térence' , "taille" : 1.50 , "age" : 12 , "hobbies" : ("ps4","athlétisme","vtt") } ,
    "Octave"  : { "prenom" : 'Octave'  , "taille" : 1.70 , "age" : 15 , "hobbies" : ("trotinnette","dessin","badminton") } ,
    "Virgile" : { "prenom" : 'Virgile' , "taille" : 1.85 , "age" : 18 , "hobbies" : ("musculation","judo","jogging","vtt") }
}
# print("--- Les enfants : ")
# for k in enfants:
#     print(f"<{k},{enfants[k]}>")

print("--- Les enfants : ")
for key in enfants:
    #if key == 'Térence':
    if enfants.get('Virgile') :
        print(f"prénom: {enfants[key]['prenom']}")
        print(f"taille: {enfants[key]['taille']} m")
        print(f"age: {enfants[key]['age']} ans")
        print(f"hobbies: {enfants[key]['hobbies']}")




