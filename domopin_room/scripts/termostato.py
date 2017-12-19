##cambiamos si esta arriba o abajo, no se pulsa
from gpiozero import LED, Button
import time
from datetime import datetime
#import spidev
import os
import glob




# Definimos entradas y salidas
#Entradas
PinPS=Button(6)         # Pulsador Subir
PinPB=Button(13)        # Pulsador Bajar
PinCRS=Button(21)       # Confirmar Rele Subir
PinCRB=Button(20)       # Confirmar Rele Bajar	
PinCRR=Button(25)       # Confirmar Rele Radiador
PinVC=Button(11)        # Confirmar Valvula Abierta
PinSV=Button(12)        # Sensor Ventana
PinSP=Button(5)         # Sensor Puerta
PinP1=Button(19)        # Pulsador 1
PinP2=Button(16)        # Pulsador 2
PinP3=Button(26)        # Pulsador 3


#Salidas
PinRSP=LED(4)           # Rele Subir Persiana
PinRBP=LED(17)  	# Rele Bajar Persiana
PinTCR=LED(18)          # Telerruptor Cerrar Radiador
PinTAR=LED(27)	        # Telerruptor Abrir Radiador

#Inicialiazamos Salidas
PinRSP.off()
PinRBP.off()
PinTCR.on()
time.sleep(0.3)
PinTCR.off()
PinTAR.off()

## CONSTANTES
C_TEMP_UMBRAL=15                # Umbral para variar la temperatura

#Variables Termostato
N_VAR_TER=7			# Num. variables
TERMOSTATO=[0,0,0,0,0,0,0]
ANT_TERMOSTATO=[0,0,0,0,0,0,0]

for i in range(N_VAR_TER):
	TERMOSTATO[i]=0		# [0]T Habitacion;[1]TCalle;[2]TConsigan;[3]ReleRadiador;[4]VvulaAbierta;[5]Error;[6]Encendido/Apagado
	ANT_TERMOSTATO[i]=0

#Variables Sensores Puerta-Ventana
N_VAR_SEN=2                     # Sensores puertas y ventana abierta
SENSORES=[0,0]                  # [0] vENTANA;[1] PUERTA

CRR=False			# Confirmar Rele Radiador

AUX_TRC=False                   # Auxiliar para dejar de pulsar telerruptor Cerrado
AUX_TRA=False                   # Auxiliar para dejar de pulsar telerruptor Abierto


###Temporizadores
T_CONFIRMAR_RELE=1000		# Tiempo Confirmar Reles 1 segundo

TM_CONFIRMAR_RADIADOR_ABIERTO=180 # Segundos
TM_CONFIRMAR_RADIADOR_CERRADO=180
TM_LEER_TEMPERATURA=45          # Tiempo de lectura de temperatura
TM_LEER_FICHERO_TERMO=300

TCRR=[False,0,False]		# Temporizador Confimar Rele Radiador
TLT=[False,0,False]		# Temporizador Leer Temperatura
TCRA=[False,0,False]            # Temporizador Confirmar Radiador Abierto
TCRC=[False,0,False]            # Temporizador Confirmar Radiador Cerrado
TLFT=[False,0,False]            # TEmp. Leer Fichero Termostato



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



######################
### ESCRIBIR FICHERO #
######################
##def EscribirFichero():
##	global POS_ACTUAL
##	print("POSICION_ACTUAL="+str(POS_ACTUAL))
##	f=open("posicion.txt","w")
##	f.seek(0,0)
##	f.write('Posicion:\n')
##	f.write(str(int(POS_ACTUAL))+"\n")
##	f.close()
##	return


TERMOSTATO[0]=(get_temp_sens(device_folder_0))
TERMOSTATO[0]=(int(TERMOSTATO[0]*10))
LeerFichero_termo()


######################
# PROGRAMA PRINCIPAL #
######################
#def Init():

while True:
		
	  # Leer Tempertua
	TLT[0],TLT[1],TLT[2]=Temporizador_s(TLT[0],TLT[1],TLT[2],TM_LEER_TEMPERATURA)

	if (TLT[2]==True):
                TERMOSTATO[0]=(get_temp_sens(device_folder_0))
                TERMOSTATO[0]=(int(TERMOSTATO[0]*10))
                print "Leer Temperatura="+str(TERMOSTATO[0]/10.0)
        
                TLT[0]=False
		TLT[2]=False
                
        # Leer Fichero Termostato
	TLFT[0],TLFT[1],TLFT[2]=Temporizador_s(TLFT[0],TLFT[1],TLFT[2],TM_LEER_FICHERO_TERMO)

	if (TLFT[2]==True):
                LeerFichero_termo()
                TLFT[0]=False
		TLFT[2]=False
		print "Leer Fichero"

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


        # Leer Sensor Ventana
        if PinSV.is_pressed:    # No pulsado
                SENSORES[0]=0
        else:                   # Pulsado
                SENSORES[0]=1

        # Leer Sensor Puerta
        if PinSP.is_pressed:    # No pulsado
                SENSORES[1]=0
        else:                   # Pulsado
                SENSORES[1]=1
	
##	print('actual='+str(TERMOSTATO))
##	time.sleep(2)

		
        if(TERMOSTATO[6]==1):
                if (SENSORES[0]==1 and SENSORES[1]==1):
                        if (TERMOSTATO[0]<TERMOSTATO[2]):
                                TERMOSTATO[3]=1
                                if(AUX_TRA==True):
                                        #print 'Termostato ENCENDIDO'
                                        PinTAR.off()
                                        AUX_TRA=False
                                if(ANT_TERMOSTATO[3]==0):
                                        print'Termostato ENCENDIDO'
                                        PinTAR.on()
                                        AUX_TRA=True
                        elif (TERMOSTATO[0]>(TERMOSTATO[2]+C_TEMP_UMBRAL)):
                                TERMOSTATO[3]=0
                                if (AUX_TRC==True):
                                       # print'Termostato APAGADO'
                                        PinTCR.off()
                                        AUX_TRC=False
                                if (ANT_TERMOSTATO[3]==1):
                                        print'Termostato APAGADO'
                                        PinTCR.on()
                                        AUX_TRC=True
                        # Temporizador Confirmar Rele Error Rele
                        if (TERMOSTATO[3]==1):
                                TCRR[0],TCRR[1],TCRR[2]=Temporizador_ms(TCRR[0],TCRR[1],TCRR[2],T_CONFIRMAR_RELE)
                                if (TCRR[2]==True and CRR==False):
                                        TERMOSTATO[5]=1
                                        
                        else:
                                TCRR[0]=False
                                TCRR[2]=False
                                
                        

                        # Temporizador Error Confimar Radiador Abierto
                        if (TERMOSTATO[3]==1 and TERMOSTATO[4]==0):
                                TCRA[0],TCRA[1],TCRA[2]=Temporizador_s(TCRA[0],TCRA[1],TCRA[2],TM_CONFIRMAR_RADIADOR_ABIERTO)
                                if (TCRA[2]==True):
                                        TERMOSTATO[5]=2
                                        
                        else:
                                TCRA[0]=False
                                TCRA[2]=False

                else:
                        if (AUX_TRC==True):
                                PinTCR.off()
                                AUX_TRC=False
                        if (ANT_TERMOSTATO[3]==1):
                                print'Apagado CALDERA'
                                TERMOSTATO[3]=0
                                AUX_TRC=True
                                PinTCR.on()
                        
                        

        else:
                if (AUX_TRC==True):
                                PinTCR.off()
                                AUX_TRC=False
                if (CRR==True or TERMOSTATO[3]==1):
                        print 'Termostato APAGADO'
                        TERMOSTATO[3]=0
                        AUX_TRC=True
                        PinTCR.on()

                        
        # Temporizador Error Confimar Radiador Cerrado
                if (TERMOSTATO[3]==0 and TERMOSTATO[4]==1):
                        TCRC[0],TCRC[1],TCRC[2]=Temporizador_s(TCRC[0],TCRC[1],TCRC[2],TM_CONFIRMAR_RADIADOR_CERRADO)
                        if (TCRC[2]==True):
                                TERMOSTATO[5]=3
                                
                else:
                        TCRC[0]=False
                        TCRC[2]=False
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
