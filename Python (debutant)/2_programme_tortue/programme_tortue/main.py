# 2nd program - Turtle [2020.09.28]
import turtle
t = turtle.Turtle()

NBR_DE_MARCHE = 5
NBR_DE_PIXELS = 10

# fonction escalier(taille en pixel, nbr. de marches)
def escalier(taille_pxl, nbr_marhces) :
    for i in range (0, NBR_DE_MARCHE):
        t.forward(taille_pxl)
        t.left(90)
        t.forward(taille_pxl)
        t.right(90)
        taille_pxl += taille_pxl / 2
        # taille_pxl -= taille_pxl / 2
    t.forward(taille_pxl)

# fonction carre(taille d'un cote en pixel)
def carre(taille_pxl_cote) :
    for i in range (0, 4):
        t.forward(taille_pxl_cote)
        t.left(90)

# fonction carres(nbr. de carrés)
def carres(nbr_carres, taille_depart):
    for c in range(0, nbr_carres) :
        carre(taille_depart * (c+1))

escalier(NBR_DE_PIXELS, NBR_DE_MARCHE)
t.clear()
t.backward(100)
carres(5, 10)

turtle.done()

