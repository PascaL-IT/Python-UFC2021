# Programme sur les Collections (Tableaux, Listes, Tuples) et Dictionnaires

#Tuples
print("** Tuples: ")
famille = ("Pascal", "Octave", "Térence", "Virgile", "Stéphanie")

for p in famille:
     print(p)

for i in range(0, len(famille)):
    print(famille[i] + " - longeur de ce prénom=" + str(len(famille[i])))

#Lists
print()
print("** Lists: ")
amis = ["Benoit", "Alexandre", "Anne-Laure"]
print(amis)
amis.append("Etienne")
print(amis)
amis.remove("Benoit")
print(*amis) #unpack
for a in amis:
     print(a)
     print(*a)
print(*"Pascal")

#Slices
print("Pascal"[1 :6 :2])



