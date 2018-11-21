#!/usr/bin/env python

import time
import sys

PinCRR=Button(5)       # Confirmar Rele Ambientador

PinTEA=LED(27)          # Telerruptor Encender Ambientador / cerrar rele
PinTAA=LED(18)	        # Telerruptor Apagar Ambientador /abrir rele


PinTAA.on()
time.sleep(0.3)
PinTAA.off()
PinTEA.off()

CRR=False			# Confirmar Rele Radiador

ESTADO=[0,0] # [0] ESTAADO {0=abierto,1=cerrado};[1] Error 
ACCION=-1
global EJECUTANDO




#########################
# COMUNICACION#

global EJECUTANDO

def Publicar_estado_actual():

    return ESTADO


def Actualizar_valores(datacmd):
    
    print "RELAY::Recibido comando :",datacmd

    if datacmd=='open':
        ACCION=0

    elif datacmd=='close':
        ACCION=1
        
        
    
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
        #Leemos Confirmar Rele Radiador
        if PinCRR.is_pressed:    # No pulsado
            CRR=False
        else:                   # Pulsado
            CRR=True
            
        if (MANUAL_CERRAR==1):
                if(AUX_TRA==True):
                        print 'Termostato ENCENDIDO'
                        PinTAR.off()
                        AUX_TRA=False
                        TERMOSTATO[3]=True
                        MANUAL_CERRAR=-1
                if(TERMOSTATO[3]==False and CRR==False):
                        print'Radiador ENCENDIDO'
                        PinTAR.on()
                        AUX_TRA=True
                                        
                                        
        elif (MANUAL_CERRAR==0):
                if (AUX_TRC==True):
                        print'Termostato APAGADO'
                        PinTCR.off()
                        AUX_TRC=False
                        TERMOSTATO[3]=False
                        MANUAL_CERRAR=-1
                if (CRR==True and TERMOSTATO[3]==True):
                        print'Radiador APAGADO'
                        PinTCR.on()
                        AUX_TRC=True        
		if ACCION==0:
			ESTADO[0]=0
		
		elif ACCION==1:
			ESTADO[0]=1
			
		ACCION=-1
		
		time.sleep(2.0)
    
    print "Cerrado"
    sys.exit(0)
    
