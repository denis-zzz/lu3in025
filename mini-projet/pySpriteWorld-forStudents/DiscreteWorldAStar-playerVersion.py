# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys

from probleme import distManhattan
import heapq

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----

def astar(pos_initiale, pos_finale, obstacles):
    """
    Implémente l'algorithme A* et retourne le meilleur chemin pour atteindre
    pos_finale à partir de pos_initiale
    IMPORTANT : à utiliser en conjonction avec la fonction reconstruire_chemin qui 
    est codée juste après
    
    Paramètres:
    pos_initiale, pos_finale : (int, int)
    obstacles : list( (int, int) )
    
    Retour:
    dict( (int, int) -> (int, int) )
    """
    
    frontiere = []
    reserve = dict()
    chemin = dict()
    
    # pos_initiale est notre point de départ
    # frontiere sera constituée de tuples de la forme (f, position) avec f le coût total pour atteindre position depuis pos_intiale
    # cela permet à heapq de trier tout seul nos positions en fonction de leur f
    heapq.heappush(frontiere, (0, pos_initiale) )
    
    # reserve sert à la fois de réserve et de dictionnaire permettant
    # de stocker les g, reserve[pos] contiendra donc le g de pos
    # pour pos_initiale, on l'initialise alors à 0
    reserve[pos_initiale] = 0
    
    # on boucle tant que frontiere n'est pas vide
    while len(frontiere) > 0:
        
        g, pos_actuelle = heapq.heappop(frontiere)
        
        # si on a trouvé la pos_finale, on peut sortir de la fonction
        if pos_actuelle == pos_finale:
            return chemin
        
        # sinon, on étend les cases voisines
        voisins = [ (pos_actuelle[0], pos_actuelle[1] + 1), 
                  (pos_actuelle[0] + 1, pos_actuelle[1]), 
                  (pos_actuelle[0] - 1, pos_actuelle[1]), 
                  (pos_actuelle[0], pos_actuelle[1] - 1) ]
        
        # on élimine les cases impossibles, ie les obstacles et celles qui sortent de la fenêtre
        voisins_possibles = [ voisins[i] for i in range(len(voisins)) if voisins[i] not in obstacles 
                            and voisins[i][0] >= 0 and voisins[i][0] <= 20 and voisins[i][1] >= 0 and voisins[i][1] <= 20 ]
           
        for voisin in voisins_possibles:
            
            if voisin not in reserve:
                
                # on calcule f pour voisin
                reserve[voisin] = g + 1   
                h = distManhattan(voisin, pos_finale)
                f = h + reserve[voisin]
                
                # et on l'ajoute dans frontiere
                heapq.heappush(frontiere, (f, voisin) )
                
                # on sauvegarde la case par laquelle voisin est accessible
                # cela permettra de reconstruire le vrai chemin plus tard
                chemin[voisin] = pos_actuelle
    
    return chemin


def reconstruire_chemin(chemin, pos_initiale, pos_finale):
    """
    Permet de reconstruire le vrai chemin calculé par l'algo de A*
    
    Paramètres:
    chemin : dict( (int, int) -> (int, int) )
    pos_initiale, pos_finale : (int, int)
    
    Retour:
    list( (int,int) )
    """
    
    # on part de la fin et on rembobine jusqu'au début
    pos_actuelle = pos_finale
    vrai_chemin = []
    
    while pos_actuelle != pos_initiale:
        
        vrai_chemin.insert(0, pos_actuelle)
        # on va chercher la "position parent" de notre pos_actuelle
        pos_actuelle = chemin[pos_actuelle]
    
    return vrai_chemin

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    
    chemin = astar( initStates[0], goalStates[0], wallStates)
    vrai_chemin = reconstruire_chemin(chemin, initStates[0], goalStates[0])
    
    #-------------------------------
    # Moving along the path
    #-------------------------------
    
    for i in range(iterations):
        
        # on suppose ici que l'objet sera trouvé en moins de "iterations" tours
        next_row = vrai_chemin[i][0]
        next_col = vrai_chemin[i][1]
        
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

            
        
            
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


