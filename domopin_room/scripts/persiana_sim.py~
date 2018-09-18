#!/usr/bin/env python

import time
import sys


# Variables


actual=[0,0,2,0,0,0,0]   #[0]Subiendo;[1] Bajando; [2]posicion; [3]pulsador arriba;[4]pulsador abajo; [5]error; [6]temperatura
anterior=[0,0,0,0,0,0,0]
web=['000','0','0','000'] #0-POSICION,1-subir,2-bajar,3-temperatura

global EJECUTANDO

global alarma_tiempo

def Refrescar_estado():

    temp=actual[6]
    #domopin_main.publish_blind_state(actual)
    #domopin_room.publish_room_state(actual)
    return actual
    

def Actualizar_alarma(data):
    
    global alarma_tiempo
    alarma_tiempo=data
    print "Proxima alarma:",alarma_tiempo

def Recibir_comando_web(datacmd,datavalue):
    
    print "Recibido comando web:",datacmd,',',datavalue
    
          
# Programa principal

def Inicio(configuracion_hab):
    print "Persiana Inicio"
    global alarma_tiempo
    alarma_tiempo=1200
    
    global EJECUTANDO
    EJECUTANDO=True
    #Bucle_principal()
    
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
