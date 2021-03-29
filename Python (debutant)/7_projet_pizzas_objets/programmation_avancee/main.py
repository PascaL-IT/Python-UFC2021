# Python avancé

class Pizza:
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix


# Création d'une liste d'objet Pizza
pizzas = [Pizza("Calzone", 8.5),
          Pizza("4 Saisons", 11),
          Pizza("Hawai", 12.4)
          ]

# for p in pizzas:
#     print(p)

# Création d'une liste de nom de pizzas avec condition
print("1) Utilisation de la syntaxe 'FOR INLINE' :")
nom_pizzas = [p.nom for p in pizzas if len(p.nom) > 6]
print("Liste des pizzas aux noms longs (>6 chars): ", nom_pizzas)
print()

# Vérification des prix de pizzas avec ANY
print("2) Utilisation de la fonction 'ANY' :")
PRIX = 10
pizza_chere = any([p.prix > PRIX for p in pizzas])
print(f"Y a-t-il une pizza chère? {pizza_chere}")
print()

print("3) Utilisation de la fonction 'SUM' :")
if pizza_chere:
    lst = [p.nom for p in pizzas if p.prix > PRIX]
    print(f"Oui, il existe", sum(1 for l in lst), f"pizza(s) de plus de {PRIX}€ : ", lst)
print()

# Zip & Zip* (unzip)
print("4) Utilisation de la fonction ZIP :")
tuple1 = ('un', 'deux', 'trois')
tuple2 = (1, 2, 3)
tuple3 = (True, False, True)

zipped = zip(tuple1, tuple2, tuple3)
listed = list(zipped)   # attention ce 1er appel videra zipped !!!
listed2 = list(zipped)  # attention 2nd appel à list sur zipped => <vide> ?

print(zipped)
print(listed)
print(zipped)
print(listed2)  # attention <vide> !!!

print(f"Voici le résultat de 'listed': ",)  # attention l'objet ZIP ne s'affiche pas sans usage d'une list()
for (label, nombre, booleen) in listed:
    print(f"{label} {nombre} {booleen}")
print()

print("5) Utilisation de la fonction UNZIP :")
unzipped = zip(*listed)
unlisted = list(unzipped)

print(f"Voici le résultat de 'unlisted' : ",)  # attention l'objet UNZIP ne s'affiche pas sans usage d'une list()
for (label, nombre, booleen) in unlisted:
    print(f"{label} {nombre} {booleen}")
print()

