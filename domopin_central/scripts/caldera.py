##cambiamos si esta arriba o abajo, no se pulsa
#from gpiozero import LED, Button
import time
from datetime import datetime
#import spidev
import os
import glob




#Variables Termostato
N_VAR_CAL=3			# Num. variables
CALDERA=[0,0,0]         # [0]ENCENDIDO/Apagado ;[1]TAgua;[2]Error;
ANT_CALDERA=[0,0,0] 


for i in range(N_VAR_CAL):
	CALDERA[i]=0		
	ANT_CALDERA[i]=0

global CRC			# Confirmar Rele Caldera

global AUX_CC                   # Auxiliar para dejar de pulsar telerruptor Cerrado
global AUX_CA                   # Auxiliar para dejar de pulsar telerruptor Abierto


###Temporizadores
TM_CONFIRMAR_RELE=5	        # Tiempo Confirmar Reles 1 segundo

TM_LEER_TEMPERATURA_AGUA=30     # Tiempo de lectura de temperatura
TM_LEER_FICHERO_CALDERA=60

TLTA=[False,0,False]		# Temporizador Leer Temperatura
TCRC=[False,0,False]		# Temporizador Confirmar Rele
TLFC=[False,0,False]            # TEmp. Leer Fichero Termostato

global TERMOSTATO

#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():

    # CALDERA     [0]ENCENDIDO/Apagado ;[1]TAgua;[2]Error;

    return CALDERA


def Actualizar_valores(datacmd,datavalue):
    
    #print "CALDERA::Recibido comando :",datacmd,"=",datavalue
    
    if datacmd=='TERMOSTATO':
        global TERMOSTATO
        TERMOSTATO=int(datavalue)
        

    

def Inicio(configuracion_hab):

    # En configuracion_hab    se tinenen los datos de configuracion por si se quiere iniciar alguna variable
    ## Ejemplo posiciones de persiana

    print 'Inicio caldera'
    global TERMOSTATO
    TERMOSTATO=0
    global CRC
    global AUX_CC
    global AUX_CA
    CRC=False
    AUX_CC=False
    AUX_CA=False
    
    global EJECUTANDO
    EJECUTANDO=True



def Cerrar_programa():
    
    global EJECUTANDO
    EJECUTANDO=False
   

# FIN COMUNICACION#
#########################





######################
# PROGRAMA PRINCIPAL #
######################
def Bucle_principal():

    global CRC
    global AUX_CC
    global AUX_CA
    while EJECUTANDO:
        
        CALDERA[0]=TERMOSTATO
        
        if CALDERA[0]==1:
            CALDERA[1]+=5
            
        elif CALDERA[0]==0:
            CALDERA[1]=180
    
        time.sleep(2.0)
