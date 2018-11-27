#!/usr/bin/env python

import time
import sys



ESTADO=[0,0] # [0] ESTAADO {0=abierto,1=cerrado};[1] Error 
ACCION=-1
MANUAL_CERRAR=1





#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():

    return ESTADO


def Actualizar_valores(datacmd):
    
    print "RELAY::Recibido comando :",datacmd

    if datacmd=='open':
        ACCION=1

    elif datacmd=='close':
        ACCION=0
        
        
    
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
		if ACCION==0:
		    ESTADO[0]=0
		
		elif ACCION==1:
		    ESTADO[0]=1
			
		ACCION=-1
		
	time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
