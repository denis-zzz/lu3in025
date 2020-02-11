'''
Created on 6 fevr. 2020

@author: Denis
'''

from tme1.Lecture.lecture_fichier import lecture_fichiers as lecture
from tme1.Utile import utile
from copy import deepcopy, copy


def gael_shapley_master(fichier1, fichier2):
    """
    cette fonction implemente l'algorithme des hopitaux, côté master.
    On utilisera 2 listes FIFO, une file d'attente pour les masters et une
    autre file séparée pour leurs demandes.
    elle retourne la liste des tuples parfaits et stables, version
    master-optimal, sous forme de dictionnaire, a la syntaxe
    {master : [etudiants_acceptes]}

    fichier1 : str
    fichier2: str
    retourne dict_resultat: dict(str->list(str))
    """

    matrice_etu, matrice_parcours, capacites = lecture(fichier1, fichier2)

    # initialisation du dictionnaire qui stockera les tuples resultats
    dict_resultat = dict()
    for i in range(len(matrice_parcours)):
        dict_resultat["{0}".format(matrice_parcours[i][0])] = []

    # copie de matrice_parcours qu'on va pouvoir manipuler tranquillement, ca sera la liste des demandeurs
    liste_demandeurs = deepcopy(matrice_parcours)

    # initialisation du dictionnaire qui stockera les demandes des masters
    dict_demandes = dict()
    for i in range(len(matrice_parcours)):
        dict_demandes["{0}".format(matrice_parcours[i][0])] = []

    # on a besoin de savoir quels etudiants sont libres à tout instant
    liste_etu_libre = [matrice_etu[i][0] for i in range(len(matrice_etu))]

    while(len(liste_demandeurs) > 0):

        # on recupere le master demandeur (toujours le 1er de la liste)
        true_master_demandeur = liste_demandeurs[0][0]
        master_demandeur = utile.from_and_to_androide(true_master_demandeur) 
        # on recupere l'etudiant demandé    (toujours le 1er de la liste)
        true_etu_demande = liste_demandeurs[0][1]
        etu_demande = utile.from_numero_to_etu(true_etu_demande)
        # on ajoute l'etudiant demandé dans le dictionnaire des demandes (sans transformation)
        dict_demandes[true_master_demandeur].append(true_etu_demande)
        
        # si l'etudiant demandé est libre
        if etu_demande in liste_etu_libre:
            dict_resultat[true_master_demandeur].append(etu_demande)
            capacites[true_master_demandeur] -= 1
            
            # on supprime l'etudiant de la liste du master demandeur pour empecher qu'il fasse
            # des demandes a un etudiant deja accepté
            liste_demandeurs[0].remove(true_etu_demande)
            
            # si le master est plein, on l'enleve de la liste des demandeurs
            if capacites[true_master_demandeur] == 0:
                del liste_demandeurs[0]
            # l'etudiant n'est plus libre donc on l'enleve de la liste des etudiants libres
            liste_etu_libre.remove(etu_demande)
        # sinon
        else:
            indice_matrice_etu = int(true_etu_demande)
            
            true_master_rival = utile.get_master_rival(etu_demande, dict_resultat)
            master_rival = utile.from_and_to_androide(true_master_rival)
            
            # si l'etudiant prefère le master demandeur a celui qu'il a deja                                                
            if matrice_etu[indice_matrice_etu].index(master_demandeur) < matrice_etu[indice_matrice_etu].index(master_rival):
                # on enleve l'etudiant de la liste des acceptés du master rival
                dict_resultat[true_master_rival].remove(etu_demande)
                # on le rajoute dans celui du master demandeur
                dict_resultat[true_master_demandeur].append(etu_demande)
                
                capacites[true_master_demandeur] -= 1
                capacites[true_master_rival] += 1
                
                # on supprime l'etudiant de la liste du master demandeur pour empecher qu'il fasse
                # des demandes a un etudiant deja accepté
                liste_demandeurs[0].remove(true_etu_demande)
                
                # si le master est plein, on l'enleve de la liste des demandeurs
                if capacites[true_master_demandeur] == 0:
                    del liste_demandeurs[0]
                    
                # si le master rival a une place de libre et uniquement une seule,
                # ça veut dire qu'il etait absent de la liste des demandeurs, on le remet donc dedans
                if capacites[true_master_rival] == 1:
                    indice_original_du_recale = utile.get_position_originale_master_recale(matrice_parcours, true_master_rival)
                    liste_demandeurs.append(copy(matrice_parcours[indice_original_du_recale]))
        
                    # on enleve par contre les etudiants pour lesquels le rival a deja fait une demande
                    for i in dict_demandes[liste_demandeurs[-1][0]]:    # liste_demandeurs[-1][0] :maniere un peu sale de retrouver le vrai nom du recalé
                        try:
                            liste_demandeurs[-1].remove(i)
                        except:
                            print("Erreur : attention aux copy et aux remove/del")
                    
            # sinon, on enleve le master de la liste de l'etudiant demandeur, il fera une demande au suivant
            else:
                liste_demandeurs[0].remove(true_etu_demande)
             
    return dict_resultat
