'''
Created on 6 fevr. 2020

@author: Denis
'''

def from_androide_to_and(string):
    """transforme la chaine de caractere ANDROIDE en AND si necessaire"""
    
    if string=="ANDROIDE":
        return "AND"
    else:
        return string

def from_and_to_androide(string):
    """transforme la chaine de caractere AND en ANDROIDE si necessaire"""
    
    if string=="AND":
        return "ANDROIDE"
    else:
        return string
    
def get_indice_in_matrice_from_nom(nom, matrice):
    """retourne l'indice de l'element dans la matrice correspondant au nom donne en parametre"""
    
    for i in range(len(matrice)):
        if matrice[i][0]==nom:
            return i

def from_numero_to_etu(numero):
    """retourne a partir du numero 0..31 le bon nom Etu"""
    
    return "Etu"+str(int(numero)+1)

def from_etu_to_numero(string):
    """retourne a partir du nom Etu le bon numero"""
    
    return str(int(string[3:])-1)

def get_indice_etu_moins_prefere(master, matrice, dictionnaire):
    """retourne l'indice de l'etudiant accepte le moins prefere pour un master donne en parametre, a la fois
    dans matrice ET dans le dictionnaire resultat
    """
    
    indice_from_nom=get_indice_in_matrice_from_nom(master, matrice)
    #i de la forme "EtuXX"
    indices_matrice=[matrice[indice_from_nom].index(str(int(i[3:])-1)) for i in dictionnaire[master]]
    
    return max(indices_matrice), indices_matrice.index(max(indices_matrice))

def get_position_originale_etu_recale(matrice, master, dictionnaire, indice_dict):
    """retourne l'indice de l'etudiant recale dans la matrice d'origine"""
    
    for i in range(len(matrice)):
        if matrice[i][0]==dictionnaire[master][indice_dict]:
            return i

        
#-----------------------------------------------------------------------------------------------#


def get_master_rival(etu, dictionnaire):
    """retourne le master qui a deja accepte l'etudiant donne en parametre"""
    
    for master, liste_accepte in dictionnaire.items():
        if etu in liste_accepte:
            return master

def get_position_originale_master_recale(matrice, master):
    """retourne l'indice du master recale dans la matrice d'origine"""
    
    for i in range(len(matrice)):
        if matrice[i][0]==master:
            return i
                