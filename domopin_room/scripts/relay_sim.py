#!/usr/bin/env python

import time
import sys



ESTADO=[1,0,0] # [0] MODO {0=manual, 1=auto} ,[1] ESTAADO {0=abierto,1=cerrado};[2] Error 
ACCION=-1
MANUAL_CERRAR=1





#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():

    return ESTADO


def Actualizar_valores(datacmd,datavalue):

    global ESTADO
    global ACCION

    print "RELAY::Recibido comando :",datacmd,':',datavalue

    if datacmd=='setrelay':
        if datavalue=='off':
            ACCION=0

        elif datavalue=='on':
            ACCION=1
        
    elif datacmd=='mode':
        
        if datavalue=='auto':
        
            ESTADO[0]=1
            
        elif datavalue=='manual':
        
            ESTADO[0]=0

   
    
# Programa principal

def Inicio(configuracion_hab):
    

    print "Relay Inicio"
    
 
    global EJECUTANDO
    EJECUTANDO=True


def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando relay.py"

#
#########################

    
def Bucle_principal():
    
    global ESTADO
    global ACCION
    print 'Bucle_principal'
    while EJECUTANDO:
        
        if (MANUAL_CERRAR==1):
            
            if ACCION==0: #abrir
                ESTADO[1]=0
                ACCION=-1
            
            elif ACCION==1: #cerrar
                ESTADO[1]=1
                ACCION=-1
			
		
		
	time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
