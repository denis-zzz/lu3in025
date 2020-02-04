'''
Created on 4 fevr. 2020

@author: Denis
'''

import sys

def lecture_fichiers(fichier1, fichier2):
    """
    cette fonction lit fichier1 et fichier2 et construit les matrices des preferences des etudiants
    et des masters sous la forme [[nom1,...],[nom2,...]...]
    fichier1 doit etre le fichier des etudiants et fichier2 celui des masters.
    
    La fonction retourne dans l'ordre : la matrice des etudiants, la matrice des masters, le dictionnaire des
    capacites de chaque masters de la forme {master: capacite}
    
    fichier1 : str
    fichier2: str
    matrice_etu: list(list(str))
    matrice_parcours: list(list(str))
    capacite: dict(str -> int)
    """
    
    #on commence par les etudiants
    with open(fichier1) as fetudiant:
        fetudiant.readline() #cela nous permet de sauter la 1ere ligne qui nous est inutile
        
        #matrice_etu[i][0] contiendra les noms des etudiants
        matrice_etu=[ligne.split() for ligne in fetudiant]
    
    #on traite les masters
    with open(fichier2) as fparcours:
        fparcours.readline()
        fparcours.readline()    #cela nous permet de sauter les 2eres lignes
        
        #matrice_parcours[i][0] contiendra les noms des masters
        matrice_parcours=[ligne.split() for ligne in fparcours]
        
        fparcours.seek(0)   #on revient au debut du fichier
        fparcours.readline()    #et on resaute la 1ere ligne
        
        #on construit la liste des capacites de chaque master
        liste_capacites=[int(mot.strip()) for ligne in fparcours.readline() for mot in ligne.split()]
        
        #on la stocke dans un dictionnaire
        capacites=dict()
        for i in range(len(matrice_parcours)):
            capacites["{0}".format(matrice_parcours[i][0])]=liste_capacites[i]
    
    return matrice_etu, matrice_parcours, capacites


def gael_shapley_etu(fichier1, fichier2):
    """
    cette fonction implemente l'algorithme des hopitaux, cote etudiants.
    On utilisera 2 listes FIFO, une file d'attente pour les etudiants et une file separee 
    pour leurs demandes.
    elle retourne la liste des tuples parfaits et stables, version etudiant-optimal, sous forme de
    dictionnaire, a la syntaxe {master : [etudiants_acceptes]}
    
    fichier1 : str
    fichier2: str
    dict_resultat: dict(str->list(str))
    """

    matrice_etu, matrice_parcours, capacites = lecture_fichiers(fichier1, fichier2)
    
    #initialisation du dictionnaire qui stockera les tuples resultats
    dict_resultat=dict()
    for i in range(len(matrice_parcours)):
        dict_resultat["{0}".format(matrice_parcours[i][0])]=[]
    
    #copie de matrice_etu qu'on va pouvoir manipuler tranquillement, ca sera la liste des demandeurs
    copie_matrice_etu=matrice_etu.copy()
    
    while(len(copie_matrice_etu)>0):
        
        #on recupere l'etudiant demandeur (toujours le 1er de la liste)
        get_etu=copie_matrice_etu[0][0] 
        #on recupere le master demande    (toujours le 1er de la liste)
        get_master=copie_matrice_etu[0][1] 
        #le nom pour androide est different d'un fichier a l'autre : si on a ANDROIDE, il faut 
        #qu'on prenne AND comme dans matrice_etu et capacites
        if get_master=='ANDROIDE':
            get_master='AND'
        
        #si le master demande a encore de la place
        if (capacites[get_master]>0):
            dict_resultat[get_master].append(get_etu)
            capacites[get_master]-=1
            #l'etudiant n'est plus libre donc on l'enleve de la liste des demandeurs
            copie_matrice_etu.pop(0)
        #sinon
        else:
            
            #on doit pouvoir se reperer dans matrice_parcours, il faut donc un moyen a partir du nom d'un
            #master de retrouver son indice dans matrice_parcours
            get_indice_master=0
            for i in range(len(matrice_parcours)):
                if matrice_parcours[i][0]==get_master:
                    get_indice_master=i
                    break
                
            #on enleve "Etu" pour avoir juste son numero
            numero_etu=get_etu[3:]
            #les numeros sont incoherents entre fichiers, donc il faut palier a ce probleme !!!
            numero_etu=str(int(numero_etu)-1)
            #on doit trouver l'indice de l'etudiant le moins prefere parmis les
            #acceptes du master considere, a la fois dans matrice_parcours ET dans le dictionnaire pour pouvoir l'enlever
            indices_liste=[matrice_parcours[get_indice_master].index(str(int(i[3:])-1)) for i in dict_resultat[get_master]]
            get_indice_matrix_last=max(indices_liste)   #l'indice du moins prefere dans matrice_parcours
            get_indice_dict_last=indices_liste.index(max(indices_liste))    #l'indice du moins prefere dans le dictionnaire resultat
            
            #si l'etudiant demandeur est prefere au dernier etudiant accepte du master                                                
            if matrice_parcours[get_indice_master].index(numero_etu) < get_indice_matrix_last:
                
                #on doit recuperer la place de l'etudiant rejete dans la matrice d'origine,
                #car on va devoir le remettre dans la liste des demandeurs
                get_indice_rejete=0
                for i in range(len(matrice_etu)):
                    if matrice_etu[i][0]==dict_resultat[get_master][get_indice_dict_last]:
                        get_indice_rejete=i
                        break
                    
                dict_resultat[get_master].pop(get_indice_dict_last)
                dict_resultat[get_master].append(get_etu)
                #l'etudiant n'est plus libre donc on l'enleve de la liste des demandeurs
                copie_matrice_etu.pop(0)
                #on remet l'etudiant rejete dans la liste des demandeurs
                copie_matrice_etu.append(matrice_etu[get_indice_rejete])
                #on enleve par contre le master considere, car sinon il fera toujours des demandes au
                #meme master
                copie_matrice_etu[-1].remove(get_master)
            
            #sinon, on enleve le master de la liste de l'etudiant demandeur, il fera une demande au suivant
            else:
                copie_matrice_etu[0].remove(get_master)

        
    return dict_resultat


#a,b,c=lecture_fichiers("FichierPrefEtu.txt", "FichierPrefSpe.txt")
test=gael_shapley_etu(sys.argv[1], sys.argv[2])
print(test)
        