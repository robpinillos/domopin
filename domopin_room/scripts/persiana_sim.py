#!/usr/bin/env python

import time
import sys


# Variables


actual=[0,0,2,0,0,0,0]   #[0]Subiendo;[1] Bajando; [2]posicion; [3]pulsador arriba;[4]pulsador abajo; [5]error; [6]temperatura
anterior=[0,0,0,0,0,0,0]
web=['000','0','0','000'] #0-POSICION,1-subir,2-bajar,3-temperatura

#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():


    return actual


def Actualizar_valores(datacmd,datavalue):
    
#    print "RADIADOR::Recibido comando :",datacmd,"=",datavalue

    if datacmd=='setpoint':
        TERMOSTATO[2]=datavalue

    elif datacmd=='temp_agua':
        TAGUA=datavalue
        

# Programa principal

def Inicio(configuracion_hab):
    
    # En configuracion_hab    se tinenen los datos de configuracion por si se quiere iniciar alguna variable
    ## Ejemplo posiciones de persiana

    print "Persiana Inicio"

    
    global EJECUTANDO
    EJECUTANDO=True


def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando radiador.py"

#
#########################

def Bucle_principal():
    
    print 'Bucle_principal'
    while EJECUTANDO:
        
#        actual[6]=actual[6]+10
#        print 'PERSIANA:'
#        print 'actual[6]=',actual[6]
        #Publicar_estado()
        time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando persiana.py"
