#!/usr/bin/env python

import time
import sys


# Variables


PERSIANA=[0,0,0,0,0,0]   #[0]Subiendo;[1] Bajando; [2]posicion; [3]pulsador arriba;[4]pulsador abajo; [5]error;
ANT_PERSIANA=[0,0,0,0,0,0]

SENSORES=[0,0]                  # [0] vENTANA;[1] PUERTA

AUX_SUBIR=True

#########################
# COMUNICACION#

global configuracion_hab
global EJECUTANDO
global estado_habitacion

def Publicar_estado_actual_persiana():


    return PERSIANA

def Publicar_estado_actual_ventana():


    return SENSORES

def Actualizar_estado_habitacion(estado):

    global estado_habitacion
    estado_habitacion=estado
    #print 'puerta cerrada=',estado_habitacion.array_window[0].door_opened
    #print 'ventana cerrada=',estado_habitacion.array_window[0].window_opened



def Actualizar_valores(datacmd,datavalue):
    
#    print "RADIADOR::Recibido comando :",datacmd,"=",datavalue

    if datacmd=='setposition':
        
        print configuracion_hab['device']['blind'][0]['positions']
        pos_deseada=[]
        for pose in configuracion_hab['device']['blind'][0]['positions']:
            if pose['name']==str(datavalue):
                pos_deseada=pose['value']

        #parsear de position_1 > int

        sentido=0
        if AUX_SUBIR is True:
            sentido=0
        else:
            sentido=1
            
            
        POS_DESEADA_WEB=int(pos_deseada[sentido])
        print 'POS_DESEADA_WEB=',POS_DESEADA_WEB

    elif datacmd=='push_up':
        PERSIANA[3]=1
        

# Programa principal

def Inicio(config_hab):
    
    # En configuracion_hab    se tinenen los datos de configuracion por si se quiere iniciar alguna variable
    ## Ejemplo posiciones de persiana

    global configuracion_hab

    configuracion_hab=config_hab


    
    global EJECUTANDO
    EJECUTANDO=True


def Cerrar_programa():

    global EJECUTANDO
    EJECUTANDO=False
    print "Cerrando persiana.py"

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
    
