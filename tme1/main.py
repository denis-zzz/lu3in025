'''
Created on 6 fevr. 2020

@author: Denis
'''

from tme1.etudiant_opti.gael_shapley_etu import gael_shapley_etu
from tme1.master_opti.gael_shapley_master import gael_shapley_master
import sys

if __name__ == '__main__':
    
    etu=gael_shapley_etu(sys.argv[1], sys.argv[2])
    master=gael_shapley_master(sys.argv[1], sys.argv[2])
    
    print("etudiant optimal = master optimal ? {0}".format(etu==master))
    #print(etu)
    #print(master)