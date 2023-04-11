from itertools import combinations
from math import factorial

#import OS
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def gen_cartones(nfichas,tabs, metodo):# método = "aleatorio","unico","mismos"
    tablas = []
    checks =  []
    if metodo == "aleatorio":
        rng = np.random.default_rng()
        for i in range(tabs):
                tablas.append(rng.choice(range(1, nfichas), size=(6, 8), replace=False))
                
    elif metodo == "unico":
        tablas.append(np.random.default_rng(1).choice(range(1, nfichas), size=(6, 8), replace=False))
        rng = np.random.default_rng()
    
        for i in range(1,tabs):
            tablas.append(rng.choice(range(1, nfichas), size=(6, 8), replace=False))
        
    elif metodo == "mismos":
        for i in range(tabs):
            rng = np.random.default_rng(i)
            tablas.append(rng.choice(range(1, nfichas), size=(6, 8), replace=False))
        
    else:
        print('método = "aleatorio","unico","mismos"')
        
      
    check = np.zeros((tabs,6,8))
    return (tablas, check)



def checker(mCards, nWin ,index):# ncards 1 a 6 cartones
    # En caso de tener varias tablas
    loterias = 0
    # Solo una tabla
   
    for card in mCards[index]:
        
        valor, count = np.unique(card,return_counts=True)
                       
        if ((count[0] == 8) & (valor[0]==1 )): # Numero de fichas en el carton
            loterias = loterias + 1
            #print(loterias)
            
    if (loterias >= nWin):
        return 1
    
    return 0
        
    
# Buscar maneras de integrar y tomar en cuenta como optimizar
#    -Empezar a chekear luego de la 8va ficha anotada
#    -En el chekeador  podrias evitar revisar los catonoes con loteria
#    en caso de tener mas de un win.


def marker(mcards, ficha,index):
    x,y = np.where(mcards[0][index]==ficha)
    if (len(x) != 0):
        mcards[1][index][x,y] = 1
        return True
    else:
        return False
    
def cardWin(mCards,index):# ncards 1 a 6 cartones
    # En caso de tener varias tablas
    cardwin = []
    counter = 0
    # Solo una tabla
   
    for card in mCards[1][index]:
        #print(card)
        valor, count = np.unique(card,return_counts=True)
                       
        if ((count[0] == 8) & (valor[0]==1 )): # Numero de fichas en el carton
            cardwin.append(mCards[0][index][counter])
           # print(card)
            
        counter += 1
        #print(counter)
    
    
    return cardwin

def ronda_de_juego(ntabs,wins,numFichas):
    tabs = ntabs
    nfichas = numFichas
    lFichas = random.sample(range(1,nfichas+1), nfichas)# Lista de fichas
    cuentaFichas = 0
    cuentaCheck = 0
    loteria = 0
    table = gen_cartones(nfichas,tabs, "unico") # True es el mismo carton
    
    for ficha in lFichas:
        cuentaFichas += 1
       
        for i in range (tabs):

            if marker(table, ficha,i):
                cuentaCheck += 1

            if (cuentaCheck >= 8):
                loteria = checker(table[1], wins,i )

            if (loteria == 1):
                #print (table)
                return (cuentaFichas,cardWin(table,i)) # Retorno el carton ganador

              
#####       LANZADA      #####

df_loteria = pd.DataFrame(columns = ["numTablas", "numFichas", "distFichas", "fichasToWin","tabToWin"])
file= r'data/df_loteria_5-1uu80-000_100d1k.csv'
NdeFichas = 80  # Fijo
nwin = 1        # Variar 1,2,3 (Todos ntabas)
nTab = 5        # 5 30 cartones
dist = "uniform"
rondas = 100

for i in range(rondas):
    temp_ftw = ronda_de_juego(nTab,nwin,NdeFichas)[0] # numero de cartones llenos y Numero de fichas 
    temp_ttw = ronda_de_juego(nTab,nwin,NdeFichas)[1] #           "                       "
    data = pd.Series({"numTablas":nTab,"numFichas":NdeFichas
                      , "distFichas":dist, "fichasToWin":temp_ftw
                      ,"tabToWin":temp_ttw})
    
    
    df_loteria = pd.concat([df_loteria,data.to_frame().T],ignore_index=True)
    
df_loteria.to_csv(file, header = True, index = False)  
