'''
Created on 6 fevr. 2020

@author: Denis
'''

def lecture_fichiers(fichier1, fichier2):
    """
    cette fonction lit fichier1 et fichier2 et construit les matrices des preferences des etudiants
    et des masters sous la forme [[nom1,...],[nom2,...]...]
    fichier1 doit etre le fichier des etudiants et fichier2 celui des masters.
    
    La fonction retourne dans l'ordre : la matrice des etudiants, la matrice des masters, le dictionnaire des
    capacites de chaque masters de la forme {master: capacite}
    
    fichier1 : str
    fichier2: str
    retourne :  matrice_etu: list(list(str))
                matrice_parcours: list(list(str))
                capacite: dict(str -> int)
    """
    
    # on commence par les etudiants
    with open(fichier1) as fetudiant:
        fetudiant.readline() # cela nous permet de sauter la 1ere ligne qui nous est inutile
        
        # matrice_etu[i][0] contiendra les noms des etudiants
        matrice_etu=[ligne.split() for ligne in fetudiant]
    
    # on traite les masters
    with open(fichier2) as fparcours:
        fparcours.readline()
        fparcours.readline()    # cela nous permet de sauter les 2eres lignes
        
        #matrice_parcours[i][0] contiendra les noms des masters
        matrice_parcours = [ligne.split() for ligne in fparcours]
        
        fparcours.seek(0)   #on revient au debut du fichier
        fparcours.readline()    #et on resaute la 1ere ligne
        
        # on construit la liste des capacités de chaque master
        liste_capacites = [int(mot.strip()) for ligne in fparcours.readline() for mot in ligne.split()]
        
        # on la stocke dans un dictionnaire
        capacites = dict()
        for i in range(len(matrice_parcours)):
            capacites["{0}".format(matrice_parcours[i][0])] = liste_capacites[i]
    
    return matrice_etu, matrice_parcours, capacites
