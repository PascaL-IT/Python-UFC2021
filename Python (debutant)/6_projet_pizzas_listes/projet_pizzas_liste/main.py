# Projet Pizzas V1

# list_pizzas = ("4 saisons","4 fromages","calzone","capricciosa","margarita") # Tuple
list_pizzas = ["4 saisons","4 fromages","calzone","capricciosa","margarita"] # List

#fonciton ajouter une pizza dans la liste
def ajouter_pizza(list):
    new_pizza = input("Ajouter une nouvelle pizza ? ")
    if new_pizza.lower() in list:
        print("Cette pizza existe déjà ...")
        return
    if len(new_pizza.strip()) != 0:
        list.append(new_pizza.lower())

#fonction de tri spéciale sur base de la longueur de l'element de la collection
def tri_special(e):
    return len(e)

#fonction afficher liste de pizzas
def afficher_pizzas(list, nbr=-1):

    #list.sort()
    #list.sort(reverse=True)
    list.sort(key=tri_special) # liste complete
    new_list = list

    if nbr != -1 :
        new_list = list[0:nbr] # liste tronquée

    size_list = len(new_list)

    if not size_list == 0 :
        print(f"Hello... voici notre liste de {size_list} pizzas: ")
    else:
        print(f"Désolé.. nous n'avons pas de pizzas !")
        return

    i = 0
    for p in new_list :
        i += 1
        print(f"{i}) {p}")

    # #première pizza
    # print(list[0])
    # #dernière pizza
    # print(list[-1])

#Main block
ajouter_pizza(list_pizzas)
# afficher_pizzas(list_pizzas)
afficher_pizzas(list_pizzas, 3)