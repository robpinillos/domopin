#!/usr/bin/env python

import time
import sys


# Variables

    # TERMOSTATO [T actual, T agua, T consigna, Rele radiador, Valvula abierta, error, ON/OFF GENERAL ,Encender caldera ]
#Variables Termostato
N_VAR_TER=8		# Num. variables
TERMOSTATO=[0,0,0,0,0,0,0,0]
ANT_TERMOSTATO=[0,0,0,0,0,0,0,0]

for i in range(N_VAR_TER):
	TERMOSTATO[i]=0		# [0]T Habitacion;[1]TCalle;[2]TConsigan;[3]ReleRadiador;[4]VvulaAbierta;[5]Error;[6]Encendido/Apagado
	ANT_TERMOSTATO[i]=0

#web=['000','0','0','000'] #0-POSICION,1-subir,2-bajar,3-temperatura
web=[0,0,0,0] #0-POSICION,1-subir,2-bajar,3-temperatura
global EJECUTANDO




#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():

    # TERMOSTATO [T actual, T calle, T consigna, Rele radiador, Valvula abierta, error, ON/OFF GENERAL ,Encender caldera ]

    return TERMOSTATO


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
    global TERMOSTATO
    TERMOSTATO[0]=0
    TERMOSTATO[2]=0
    
    
    global EJECUTANDO
    EJECUTANDO=True


def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando radiador.py"

#
#########################

    
def Bucle_principal():
    
    global TERMOSTATO
    print 'Bucle_principal'
    while EJECUTANDO:
        
        if TERMOSTATO[0]< TERMOSTATO[2]:
            TERMOSTATO[7]=1
            TERMOSTATO[0]=TERMOSTATO[0]+10
            TERMOSTATO[1]=TERMOSTATO[1]+5
        else:
            TERMOSTATO[7]=0
            
        print 'RADIADOR:'
        print 'TERMOSTATO[0]=',TERMOSTATO[0]
        #Publicar_estado()
        time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
