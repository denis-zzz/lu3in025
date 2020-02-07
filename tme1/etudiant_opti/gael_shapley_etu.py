'''
Created on 6 fevr. 2020

@author: Denis
'''

from tme1.lecture.lecture_fichier import lecture_fichiers as lecture
from tme1.utile import utile
from copy import deepcopy, copy

def gael_shapley_etu(fichier1, fichier2):
    """
    cette fonction implemente l'algorithme des hopitaux, cote etudiants.
    On utilisera 2 listes FIFO, une file d'attente pour les etudiants et une autre file separee 
    pour leurs demandes.
    elle retourne la liste des tuples parfaits et stables, version etudiant-optimal, sous forme de
    dictionnaire, a la syntaxe {master : [etudiants_acceptes]}
    
    fichier1 : str
    fichier2: str
    dict_resultat: dict(str->list(str))
    """
    
    matrice_etu, matrice_parcours, capacites = lecture(fichier1, fichier2)
    
    #initialisation du dictionnaire qui stockera les tuples resultats
    dict_resultat=dict()
    for i in range(len(matrice_parcours)):
        dict_resultat["{0}".format(matrice_parcours[i][0])]=[]
    
    #copie de matrice_etu qu'on va pouvoir manipuler tranquillement, ca sera la liste des demandeurs
    liste_demandeurs=deepcopy(matrice_etu)
    
    #initialisation du dictionnaire qui stockera les demandes des etudiants
    dict_demandes=dict()
    for i in range(len(matrice_etu)):
        dict_demandes["{0}".format(matrice_etu[i][0])]=[]
    
    while(len(liste_demandeurs)>0): 
    
        #on recupere l'etudiant demandeur (toujours le 1er de la liste)
        etu_demandeur=liste_demandeurs[0][0] 
        #on recupere le master demande    (toujours le 1er de la liste)
        true_master_demande=liste_demandeurs[0][1]
        master_demande=utile.from_androide_to_and(true_master_demande)
        #on ajoute le master demande dans le dictionnaire des demandes (sans transformation)
        dict_demandes[etu_demandeur].append(true_master_demande)
        
        #si le master demande a encore de la place
        if (capacites[master_demande]>0):
            dict_resultat[master_demande].append(etu_demandeur)
            capacites[master_demande]-=1
            #l'etudiant n'est plus libre donc on l'enleve de la liste des demandeurs
            del liste_demandeurs[0]
        #sinon
        else:
            indice_matrice_parcours=utile.get_indice_in_matrice_from_nom(master_demande, matrice_parcours)
            
            numero_etu=utile.from_etu_to_numero(etu_demandeur)
            
            #on recupere les indices de l'etudiant le moins prefere du master demande
            indice_worst_dans_matrice, indice_worst_dans_dict = utile.get_indice_etu_moins_prefere(master_demande, matrice_parcours, dict_resultat)
            
            #si l'etudiant demandeur est prefere a l'etudiant worst du master demande                                                
            if matrice_parcours[indice_matrice_parcours].index(numero_etu) < indice_worst_dans_matrice:
                
                indice_original_du_recale=utile.get_position_originale_etu_recale(matrice_etu, master_demande, dict_resultat, indice_worst_dans_dict)
                #on vire le recale de la liste des acceptes du master demande
                del dict_resultat[master_demande][indice_worst_dans_dict]
                #on y rajoute l'etudiant demandeur
                dict_resultat[master_demande].append(etu_demandeur)
                #l'etudiant n'est plus libre donc on l'enleve de la liste des demandeurs
                del liste_demandeurs[0]
                #on remet l'etudiant rejete dans la liste des demandeurs
                liste_demandeurs.append(copy(matrice_etu[indice_original_du_recale]))
        
                #on enleve par contre les masters pour lesquels le recale a deja fait une demande
                for i in dict_demandes[liste_demandeurs[-1][0]]:    #liste_demandeurs[-1][0] :maniere un peu sale de retrouver le vrai nom du recale
                    try:
                        liste_demandeurs[-1].remove(i)
                    except:
                        print("Erreur : attention aux copy et aux remove/del")
                    
            #sinon, on enleve le master de la liste de l'etudiant demandeur, il fera une demande au suivant
            else:
                liste_demandeurs[0].remove(true_master_demande)
             
    return dict_resultat
                        