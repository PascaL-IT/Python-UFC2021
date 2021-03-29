# Projet Pizzas v2 - POO in Section 11 [2020.09.30]

# Pizza object
class Pizza:
    def __init__(self, nom, prix, ingredients, vegetarian=False):
        self.nom = nom                  # str
        self.prix = prix                # €
        self.ingredients = ingredients  # tuple
        self.vegetarian = vegetarian    # pizza vegetarien ou non (bool)

    def s_print(self):
        vgt_str = ""
        if self.vegetarian:
            vgt_str = "- VEGETARIENNE"
        print(f"PIZZA {self.nom} - au prix de {self.prix}€ {vgt_str}")
        print(" composée de " + ", ".join(self.ingredients))
        print()


# PizzaPerso (hérite de Pizza)
class PizzaPerso(Pizza):

    compteur = 0

    def __init__(self):
        super().__init__("Perso", 5.0, []) # !!! LIST pour les ingrédients car mutable
        PizzaPerso.compteur += 1
        self.modifier_nom()
        self.modifier_prix_de_base()
        self.ajouter_ingredients()
        self.prix += len(self.ingredients)

    def modifier_nom(self):
        print(f"Création d'une nouvelle pizza personnalisée {PizzaPerso.compteur}:")
        self.nom = input("Quel nom pour cette pizza personnalisée ? ")

    def modifier_prix_de_base(self):
        mon_prix = input("Quel est votre prix de base en € ? ")
        if mon_prix.strip() == "":
            mon_prix = 0.0
        self.prix = float(mon_prix)

    def ajouter_ingredients(self):
        while True:
            ingredient = input("Ajouter un ingrédient de votre choix (ou appuyer sur ENTER)? ")
            if ingredient.strip() == "" :
                return #sortir de la boucle infinie
            self.ingredients.append(ingredient)
            #affichage des ingrédients de la liste personnalisée
            sep = ', '
            print(f"Vous avez {len(self.ingredients)} ingrédient(s) : {sep.join(self.ingredients)} ")


# Fonction de tri
def tri_prix(e):
    return e.prix


# Main block
ingred_pizza1 = ("fromage mozzarella", "tomate", "jambon italien", "artichaut", "champignons")
pizza1 = Pizza("Capricciosa", 12.5, ingred_pizza1)
pizza1.s_print()

ingred_pizza2 = ("fromage", "tomate", "olives", "capres")
pizza2 = Pizza("Olivia", 9.5, ingred_pizza2, True)
pizza2.s_print()

ingred_pizza3 = ("gorgonzola", "mozzarella", "parmesan", "chèvre", "tomate", "origan")
pizza3 = Pizza("4 fromages", 11.0, ingred_pizza3, False)
# pizza3.s_print()

ingred_pizza4 = ("ananas", "jambon", "crème")
pizza4 = Pizza("Hawai", 8, ingred_pizza4)
# pizza4.s_print()

#pizza5 = PizzaPerso()
# pizza5.s_print()

pizzas = [pizza1, pizza2] #, pizza3, pizza4, pizza5] # , PizzaPerso()]
pizzas.sort(key=tri_prix, reverse=True) # pizzas triées par le prix décroissant

print()
print("Liste des pizzas: ")
print("----------------- ")
for p in pizzas:
#     # if (p.type): # filtre sur végétarienne
#     # if ("tomate" in p.ingredients): # filtre sur avec de la tomate
#     # if p.prix < 10.0 :  # filtre sur un prix
      p.s_print()  # et non print(p.s_print()) !!! sinon None s'affiche...
