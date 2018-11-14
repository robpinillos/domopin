

##cambiamos si esta arriba o abajo, no se pulsa
from gpiozero import LED, Button
import time
from datetime import datetime
#import spidev
import os
import glob
import sys




# Definimos entradas y salidas
#Entradas
##PinPS=Button(6)         # Pulsador Subir
##PinPB=Button(13)        # Pulsador Bajar
##PinCRS=Button(21)       # Confirmar Rele Subir
##PinCRB=Button(20)       # Confirmar Rele Bajar	
PinCRR=Button(0)       # Confirmar Rele Radiador
PinVC=Button(6)        # Confirmar Valvula Abierta
##PinSV=Button(12)        # Sensor Ventana
##PinSP=Button(5)         # Sensor Puerta
##PinP1=Button(19)        # Pulsador 1
##PinP2=Button(16)        # Pulsador 2
##PinP3=Button(26)        # Pulsador 3


#Salidas
##PinRSP=LED(4)           # Rele Subir Persiana
##PinRBP=LED(17)  	# Rele Bajar Persiana
PinTCR=LED(14)          # Telerruptor Cerrar Radiador
PinTAR=LED(15)	        # Telerruptor Abrir Radiador
PinTEA=LED(27)          # Telerruptor Encender Ambientadro
PinTAA=LED(18)	        # Telerruptor Apagar Ambientadro

#Inicialiazamos Salidas
##PinRSP.off()
##PinRBP.off()
PinTCR.on()
time.sleep(0.3)
PinTCR.off()
PinTAR.off()
PinTAA.on()
time.sleep(0.3)
PinTAA.off()
PinTEA.off()


## CONSTANTES
C_TEMP_UMBRAL=5                # Umbral para variar la temperatura
C_TEMP_AGUA=400

#Variables Termostato
N_VAR_TER=8			# Num. variables
TERMOSTATO=[0,0,0,0,0,0,0,0]
ANT_TERMOSTATO=[0,0,0,0,0,0,0,0]
RELE=False
ANT_RELE=False

for i in range(N_VAR_TER):
	TERMOSTATO[i]=0		# [0]T Habitacion;[1]TCalle;[2]TConsigan;[3]ReleRadiador;[4]VvulaAbierta;[5]Error;[6]Encendido/Apagado;[7]Encender Caldera
	ANT_TERMOSTATO[i]=0

#Variables Sensores Puerta-Ventana
N_VAR_SEN=2                     # Sensores puertas y ventana abierta

########### PONER [0,0] CUANDO ACTIVO SENSOSERES VENTANA Y PUERTA
SENSORES=[1,1]                  # [0] vENTANA;[1] PUERTA aqu

CRR=False			# Confirmar Rele Radiador

AUX_TRC=False                   # Auxiliar para dejar de pulsar telerruptor Cerrado
AUX_TRA=False                   # Auxiliar para dejar de pulsar telerruptor Abierto


###Temporizadores
T_CONFIRMAR_RELE=1000		# Tiempo Confirmar Reles 1 segundo

TM_CONFIRMAR_RADIADOR_ABIERTO=300 # Segundos
TM_CONFIRMAR_RADIADOR_CERRADO=300
TM_LEER_TEMPERATURA=20          # Tiempo de lectura de temperatura
TM_LEER_FICHERO_TERMO=60
TM_ESPERA_CERRAR_RADIADOR=60    # Original valor 90
TM_DESPUES_SENSOR_VENTANA=15

TCRR=[False,0,False]		# Temporizador Confimar Rele Radiador
TLT=[False,0,False]		# Temporizador Leer Temperatura
TLFT=[False,0,False]		# Temporizador Leer Temperatura
TCRA=[False,0,False]            # Temporizador Confirmar Radiador Abierto
TCRC=[False,0,False]            # Temporizador Confirmar Radiador Cerrado
TECR=[False,0,False]            # Temporizador Espera Cerrar Radiador
TDSV=[False,0,False]            # Temporizador Espera Despues Cerrar Ventana





os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder_0 = glob.glob(base_dir+'28*')[0]
#device_folder_1 = glob.glob(base_dir+'28*')[1]

device_file = '/w1_slave'

def get_temp_sens(device_file):
        device_file = device_file+ '/w1_slave'
	tfile=open(device_file)
	text=tfile.read()
	tfile.close()
	secondline=text.split("\n")[1]
	temperaturedata=secondline.split(" ")[9]
	temperatura=float(temperaturedata[2:])
	temperatura=temperatura/1000.0
	return float(temperatura)

TERMOSTATO[0]=(get_temp_sens(device_folder_0))
TERMOSTATO[0]=(int(TERMOSTATO[0]*10))

#############################
# TEMPORIZADOR MILISEGUNDOS #
#############################
def Temporizador_ms(auxt,tiempo,T,TIEMPO):
	if auxt==False:
		tiempo=int(time.time()*1000)
		auxt=True
		T=False
	else:
		tiempot=int(time.time()*1000)
		if (((tiempot-tiempo))>=TIEMPO):
			T=True

	return auxt,tiempo,T


#########################
# TEMPORIZADOR SEGUNDOS #
#########################
def Temporizador_s(auxt,tiempo,T,TIEMPO):
	if auxt==False:
		tiempo=int(time.time())
		auxt=True
		T=False
	else:
		tiempot=int(time.time())
		if (((tiempot-tiempo))>=TIEMPO):
			T=True
	return auxt,tiempo,T

################
# LEER FICHERO #
################
def LeerFichero_termo():
	global TERMOSTATO
        T_CONS=0
        
	g=open("termostato.txt","r")
        a=0
        while True:
                a=a+1
                linea=g.readline()
                if not linea: break
                if (a%2==0):
                        if (a/2==1):
                                TERMOSTATO[6]=int(linea)
                        elif (a/2==2):
                                TERMOSTATO[2]=linea
                                T_CONS=int(TERMOSTATO[2][0])*100
                                T_CONS=T_CONS+int(TERMOSTATO[2][1])*10
                                T_CONS=T_CONS+int(TERMOSTATO[2][3])
                                TERMOSTATO[2]=T_CONS
        g.close()
	return

TAGUA=0                 # Temp- agua       

#########################
# COMUNICACION#

global EJECUTANDO
EJECUTANDO=False
global MANUAL_CERRAR
MANUAL_CERRAR=-1

def Publicar_estado_actual():
	# TERMOSTATO [T actual, T calle, T consigna, Rele radiador, Valvula abierta, error, ON/OFF GENERAL,Encender Caldera ]
	# SENSORES [0] vENTANA;[1] PUERTA 
	
	return TERMOSTATO, SENSORES


def Actualizar_valores(datacmd,datavalue):
        global TAGUA
        global TERMOSTATO
        global MANUAL_CERRAR
        
        ##print "Hab:",datacmd,"=",datavalue
        if datacmd=='setpoint':
			TERMOSTATO[2]=datavalue
			
        elif datacmd=='temp_agua':
			TAGUA=int(datavalue)
			TERMOSTATO[1]=TAGUA

        elif datacmd=='radiator_manual':
			if datavalue=='auto':
				TERMOSTATO[6]=1
				
			elif datavalue=='manual':
			
				TERMOSTATO[6]=0
				
			elif datavalue=='close':
			
				MANUAL_CERRAR=1
				
			elif datavalue=='open':
				
				MANUAL_CERRAR=0
              

# Programa principal

def Inicio(configuracion_hab):
        # En configuracion_hab    se tinenen los datos de configuracion por si se quiere iniciar alguna variable
        ## Ejemplo posiciones de persiana
        
        global TERMOSTATO
        global EJECUTANDO


        print "Persiana Inicio"
        TERMOSTATO[0]=0
        TERMOSTATO[2]=0
        TERMOSTATO[6]=1
        
        EJECUTANDO=True
        return


def Cerrar_programa():
        global EJECUTANDO
        EJECUTANDO=False
        print "Cerrando radiador.py"
        return

#
#########################


######################
# PROGRAMA PRINCIPAL #
######################
    
def Bucle_principal():
	global TERMOSTATO
	global AUX_TRA
	global AUX_TRC
	global TLT
	global TECR
	global EJECUTANDO
##        global RELE
	global TAGUA
	global MANUAL_CERRAR
	
	print 'Bucle_principal'

	while EJECUTANDO:
		# Leer Tempertua
		TLT[0],TLT[1],TLT[2]=Temporizador_s(TLT[0],TLT[1],TLT[2],TM_LEER_TEMPERATURA)
		
		if (TLT[2]==True):
				TERMOSTATO[0]=(get_temp_sens(device_folder_0))
				TERMOSTATO[0]=(int(TERMOSTATO[0]*10))
				print "Leer Temperatura="+str(TERMOSTATO[0]/10.0)
				TLT[0]=False
				TLT[2]=False

		# Leer Fichero Termostato
		##TLFT[0],TLFT[1],TLFT[2]=Temporizador_s(TLFT[0],TLFT[1],TLFT[2],TM_LEER_FICHERO_TERMO)

		##if (TLFT[2]==True):
		##        LeerFichero_termo()
		##        TLFT[0]=False
		##        TLFT[2]=False
		##        print "Leer Fichero"

		#Leemos Confirmar Rele Radiador
		if PinCRR.is_pressed:    # No pulsado
				CRR=False
		else:                   # Pulsado
				CRR=True

		# Leer Valvula de Radiador
		if PinVC.is_pressed:    # No pulsado
				TERMOSTATO[4]=0
		else:                   # Pulsado
				TERMOSTATO[4]=1
				
#####ACTIVARLO CUANDO HAYA SENSORES DE VEENTANA
##                # Leer Sensor Ventana
##                if PinSV.is_pressed:    # No pulsado
##                        SENSORES[0]=0
##                else:                   # Pulsado
##                        SENSORES[0]=1
##
##                # Leer Sensor Puerta
##                if PinSP.is_pressed:    # No pulsado
##                        SENSORES[1]=0
##                else:                   # Pulsado
##                        SENSORES[1]=1
##
##### HASTA AQUI
                        
##                print('actual='+str(TERMOSTATO))
##                print ('Tagua='+str(TAGUA))
##	time.sleep(2)

		if(TERMOSTATO[6]==0): # MODO MANUAL
			
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
							
			
		elif(TERMOSTATO[6]==1):
                        if (SENSORES[0]==1 and SENSORES[1]==1):
                                if (TDSV[2]==True):
                                        if (TERMOSTATO[0]<TERMOSTATO[2]-int(C_TEMP_UMBRAL/2)):
                                                TERMOSTATO[7]=1
                                                TECR[0]=False
                                                TECR[2]=False
                                                if (TAGUA>C_TEMP_AGUA):
                                                        if(AUX_TRA==True):
                                                                #print 'Termostato ENCENDIDO'
                                                                PinTAR.off()
                                                                AUX_TRA=False
                                                                TERMOSTATO[3]=True
                                                        if(TERMOSTATO[3]==False and CRR==False):
                                                                print'Radiador ENCENDIDO'
                                                                PinTAR.on()
                                                                AUX_TRA=True
                                                                
                                                else:
                                                        if (AUX_TRC==True):
                                                               # print'Termostato APAGADO'
                                                                PinTCR.off()
                                                                AUX_TRC=False
                                                        if (CRR==True and TERMOSTATO[3]==True):
                                                                print'Radiador APAGADO'
                                                                PinTCR.on()
                                                                AUX_TRC=True
                                                                TERMOSTATO[3]=False
                                                        
                                        elif (TERMOSTATO[0]>(TERMOSTATO[2]+C_TEMP_UMBRAL)and (TERMOSTATO[3]==1 or TERMOSTATO[7]==1)):
                                                TERMOSTATO[7]=0
                                                if (TECR[2]==True):
                                                        print 'dentro del tiempo para apagar radiador'
                                                        if (AUX_TRC==True):
                                                               # print'Termostato APAGADO'
                                                                PinTCR.off()
                                                                AUX_TRC=False
                                                                TECR[0]=False
                                                                TECR[2]=False
                                                                TERMOSTATO[3]=0
                                                        elif (CRR==True or TERMOSTATO[3]==1):
                                                                print'Radiador APAGADO'
                                                                PinTCR.on()
                                                                AUX_TRC=True
                                                        else:
                                                                TECR[0]=False
                                                                TECR[2]=False
                                                else:
                                                       TECR[0],TECR[1],TECR[2]=Temporizador_s(TECR[0],TECR[1],TECR[2],TM_ESPERA_CERRAR_RADIADOR)
                                                       
                                        if (TERMOSTATO[3]==True):
                                                TCRR[0],TCRR[1],TCRR[2]=Temporizador_ms(TCRR[0],TCRR[1],TCRR[2],T_CONFIRMAR_RELE)
                                        else:
                                                TCRR[0]=False
                                                TCRR[2]=False

                                        if (TERMOSTATO[3]==True and TCRR[2]==True and CRR==False):
                                                TERMOSTATO[5]=1
                                        # Temporizador Error Confimar Radiador Abierto
                                        if (TERMOSTATO[3]==True and TERMOSTATO[4]==0):
                                                TCRA[0],TCRA[1],TCRA[2]=Temporizador_s(TCRA[0],TCRA[1],TCRA[2],TM_CONFIRMAR_RADIADOR_ABIERTO)
                                        else:
                                                TCRA[0]=False
                                                TCRA[2]=False
                                        if (TCRA[2]==True and TERMOSTATO[3]==True and TERMOSTATO[4]==0):
                                                TERMOSTATO[5]=2
                                else:
                                        TDSV[0],TDSV[1],TDSV[2]=Temporizador_s(TDSV[0],TDSV[1],TDSV[2],TM_DESPUES_SENSOR_VENTANA)
                                      

                        elif (TERMOSTATO[7]==1):
                                TDSV[0]=False
                                TDSV[2]=False
                                if (AUX_TRC==True):
                                        PinTCR.off()
                                        AUX_TRC=False
                                        TERMOSTATO[3]=0
                                        print 'Radiador APAGADO'
                                elif (CRR==True or TERMOSTATO[3]==True):
                                        PinTCR.on()
                                        AUX_TRC=True  
                                if (TECR[2]==True and TERMOSTATO[7]==1):
                                        TERMOSTATO[7]=0
                                        print 'Caldera APAGADA'
                                        TECR[0]=False
                                        TECR[2]=False
                                elif (TERMOSTATO[7]==1):
                                        TECR[0],TECR[1],TECR[2]=Temporizador_s(TECR[0],TECR[1],TECR[2],TM_ESPERA_CERRAR_RADIADOR)
                                
                                TCRR[0]=False
                                TCRR[2]=False
                                TCRA[0]=False
                                TCRA[2]=False

                elif (TERMOSTATO[3]==1):
                        TERMOSTATO[7]=0
                        if (TECR[2]==True):
                                if (AUX_TRC==True):
                                        PinTCR.off()
                                        AUX_TRC=False
                                        TECR[0]=False
                                        TECR[2]=False
                                        TERMOSTATO[3]=0
                                elif (CRR==True and TERMOSTATO[3]==True):
                                        print'Apagado CALDERA'
                                        AUX_TRC=True
                                        PinTCR.on()
                                else:
                                        TECR[0]=False
                                        TECR[2]=False
                        else:
                                TECR[0],TECR[1],TECR[2]=Temporizador_s(TECR[0],TECR[1],TECR[2],TM_ESPERA_CERRAR_RADIADOR/2)
                        TCRR[0]=False
                        TCRR[2]=False
                        TCRA[0]=False
                        TCRA[2]=False
     
       
               
                 # Temporizador Error Confimar Radiador Cerrado
                if (TERMOSTATO[3]==False and TERMOSTATO[4]==1):
                        TCRC[0],TCRC[1],TCRC[2]=Temporizador_s(TCRC[0],TCRC[1],TCRC[2],TM_CONFIRMAR_RADIADOR_CERRADO)
                else:
                        TCRC[0]=False
                        TCRC[2]=False 
                if (TCRC[2]==True and TERMOSTATO[3]==False and TERMOSTATO[4]==1):
                        TERMOSTATO[5]=3
                                                        
        
##        print 'T='+str(TERMOSTATO)
##        print 'TA='+str(ANT_TERMOSTATO)
                if(ANT_TERMOSTATO!=TERMOSTATO):
                        for i in range(N_VAR_TER):
                                ANT_TERMOSTATO[i]=TERMOSTATO[i]
        #print 'CRR='+str(CRR)
        #print 'Ventana=['+str(SENSORES)+']'
                if (TERMOSTATO[5]==1):
                        print 'ERROR RELE'
                elif(TERMOSTATO[5]==2):
                        print 'ERROR tiempo de apertura valvula superado'
                elif (TERMOSTATO[5]==3):
                        print 'ERROR tiempo de Cerrar valvula superado'
                time.sleep(0.5)

        sys.exit(0)
