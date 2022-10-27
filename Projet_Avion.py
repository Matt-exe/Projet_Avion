##################################################
# groupe 5 L1 MPCI TD 6                                                          
# Matteo Rabache                                 
##################################################


##################################################
#Import des librairies

import tkinter as tk
from tkinter import messagebox
import random, time


##################################################
# Fonctions

def avion():
    """ 
    Fonction qui créer l'avion. Elle met en place les variables utiles à la suite du programme ou à l'utilisation de l'interface graphique.
    """
    for j in range(30):
        for i in range(7):
            canvas.create_rectangle(i * WIDTH // 7, j * HEIGHT // 30, (i + 1) * WIDTH // 7, (j + 1) * HEIGHT // 30, fill="grey")
    for i in range(30):
        canvas.itemconfigure(7*i+4,fill="white")

def genbillet():
    """ 
    Fonction qui génère une liste aléatoire de tous les billets possibles. 
    """
    l = [[i,j,random.randint(0,2)] for i in range(1,31) for j in range(1,8) if j !=4]
    random.shuffle(l)
    return l

def fonction_générale(event):
    """
    fonction générale qui provoque l'arrivée des passagers daans l'avion et stoppe la simulation lorsquils sont tous assis.
    """
    while cpt < 180:
        avancement()
        canvas.update()
        time.sleep(0.05)

def avancement():
    """
    Fonction qui génère l'avancée des passagers dans l'avion.
    """
    global cpt

    # Si des passagers sont déjà entré alors on les fait tous avancer d'une case vers leur place respective
    if len(cherche_sa_place) > 0:
        for i in range(len(cherche_sa_place)):

            #Si le passager est assis
            if billet[i][2] == -1:
                color(cherche_sa_place[i],"green")
                continue        # On passe au passager d'après
            
            # pour faire avancer dans le couloir
            num_couloir = cherche_sa_place[i][0]
            num_siege = cherche_sa_place[i][1]
            if num_couloir < billet[i][0]:
                if couloir[num_couloir] == "white":
                    color(cherche_sa_place[i],"white")
                    cherche_sa_place[i][0] += 1             
                    color(cherche_sa_place[i],"pink")

            # cas où le passager à 1 ou 2 valises
            elif num_couloir == billet[i][0] and billet[i][2] > 0:
                couloir[num_couloir-1] = "red"
                color(cherche_sa_place[i],"red")
                billet[i][2] -= 1

            # else pour avance rangée
            else:
                if plus_dans_le_couloir(i):
                    color(cherche_sa_place[i],"white")
                    couloir[num_couloir-1] = "white"
                else:
                    color(cherche_sa_place[i],"grey")

                if num_siege < billet[i][1]:
                    cherche_sa_place[i][1] += 1
                    color(cherche_sa_place[i],"pink")

                elif num_siege > billet[i][1]:
                    cherche_sa_place[i][1] -= 1
                    color(cherche_sa_place[i],"pink")

                # si le passager est à la bonne place, la case devient verte
                else:
                    color(cherche_sa_place[i],"green")
                    cpt += 1
                    #Lorsqu'un passager est assis son bagage vaut -1 :
                    billet[i][2] = -1

    # Un passager entre
    if len(cherche_sa_place) < 180 and couloir[0] == "white":
        cherche_sa_place.append([1,4])
        color(cherche_sa_place[-1],"yellow")
        

def color(coord:list,couleur:str):
    """
    Colore une case à partir de ses coordonnées [rang,place].
    """
    n = 7*coord[0] - (7-coord[1])
    canvas.itemconfigure(n,fill=couleur)


def plus_dans_le_couloir(i):
    """
    Retourne True si l'ancienne position du passager était dans le couloir, False sinon.
    """
    return cherche_sa_place[i][1] == 4




##################################################
# Variables / Constantes

couloir = ["white" for _ in range(31)]
cpt = 0
cherche_sa_place = []

HEIGHT, WIDTH = 30 * 25, 7 * 25


##################################################
# Fenêtre

racine = tk.Tk()
racine.title("")


##################################################
# Canvas

canvas = tk.Canvas(racine, width=WIDTH, height=HEIGHT)
canvas.grid()
        
avion()
billet = genbillet()

messagebox.showinfo("Indications","- Les cases blanches sont celles du couloir de l'avion. Les cases grises sont celles des sièges de l'avion.\n- Lorsqu'un joueur rentre dans l'avion, la première case du couloir devient jaune.\n- Lorsqu'un joueur avance, la case devient rose.\n- Lorsqu'un joueur est assis, la case devient verte.\n- Lorsqu'un joueur dépose sa valise la case devient rouge (et les passagers du couloir ne peuvent plus avancer).")
messagebox.showinfo("How to run :","Press button 'a'")

racine.bind('<KeyPress-a>', fonction_générale)
racine.mainloop()