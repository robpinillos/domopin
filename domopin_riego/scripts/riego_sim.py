#!/usr/bin/env python

import time
import sys


# Variables


RIEGO=[0,0,0,0,0,0]   #[0]Subiendo;[1] Bajando; [2]posicion; [3]pulsador arriba;[4]pulsador abajo; [5]error;
ANT_RIEGO=[0,0,0,0,0,0]



#########################
# COMUNICACION#
global configuracion
global EJECUTANDO
global estado_riego

def Publicar_estado_actual():


    return RIEGO


def Actualizar_valores(datacmd,datavalue):
    


    if datacmd=='start':
        RIEGO[3]=1
    elif datacmd=='stop':
        RIEGO[3]=0
        

# Programa principal

def Inicio(config_hab):
    
    # En configuracion_hab    se tinenen los datos de configuracion por si se quiere iniciar alguna variable
    ## Ejemplo posiciones de persiana

    global configuracion_riego

    configuracion_riego=config_hab
    
    global EJECUTANDO
    EJECUTANDO=True


def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando riego.py"

#
#########################

def Bucle_principal():
    
    print 'Bucle_principal'
    while EJECUTANDO:
        
        Publicar_estado()
        time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
