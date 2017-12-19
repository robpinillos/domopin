##cambiamos si esta arriba o abajo, no se pulsa
from gpiozero import LED, Button
import time
from datetime import datetime
#import spidev
import os
import glob




# Definimos entradas y salidas
#Entradas
PinCRC=Button(19)       # Confirmar Rele Caldera


#Salidas
PinCC=LED(20)           # Telerruptor Cerrar Caldera
PinCA=LED(22)   	# Telerruptor Abrir Caldera


#Inicialiazamos Salidas
PinCA.on()
time.sleep(0.3)
PinCA.off()


#Variables Termostato
N_VAR_CAL=3			# Num. variables
CALDERA=[0,0,0]         # [0]ENCENDIDO/Apagado ;[1]TAgua;[2]Error;
ANT_CALDERA=[0,0,0] 

for i in range(N_VAR_CAL):
	CALDERA[i]=0		
	ANT_CALDERA[i]=0

CRC=False			# Confirmar Rele Caldera

AUX_CC=False                   # Auxiliar para dejar de pulsar telerruptor Cerrado
AUX_CA=False                   # Auxiliar para dejar de pulsar telerruptor Abierto


###Temporizadores
TM_CONFIRMAR_RELE=5	        # Tiempo Confirmar Reles 1 segundo

TM_LEER_TEMPERATURA_AGUA=30     # Tiempo de lectura de temperatura
TM_LEER_FICHERO_CALDERA=60

TLTA=[False,0,False]		# Temporizador Leer Temperatura
TCRC=[False,0,False]		# Temporizador Confirmar Rele
TLFC=[False,0,False]            # TEmp. Leer Fichero Termostato


#########################
# COMUNICACION#


def Refrescar_estado():

    # TERMOSTATO [T actual, T calle, T consigna, Rele radiador, Valvula abierta, error, ON/OFF GENERAL ]
    # CALDERA     [0]ENCENDIDO/Apagado ;[1]TAgua;[2]Error;

    temp=[CALDERA[1],-1,-1,CALDERA[0],-1,CALDERA[2],1]
    

def Actualizar_alarma(data):
    
    global alarma_tiempo
    alarma_tiempo=data
    print "Proxima alarma:",alarma_tiempo

def Recibir_comando_web(datacmd,datavalue):
    
    print "Recibido comando web:",datacmd,',',datavalue
    
   

# FIN COMUNICACION#
#########################




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
def LeerFichero_caldera():
	global TERMOSTATO
        T_CONS=0
        
	h=open("caldera.txt","r")
        a=0
        while True:
                a=a+1
                linea=h.readline()
                if not linea: break
                if (a%2==0):
                        if (a/2==1):
                                TERMOSTATO=int(linea)
        h.close()
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





######################
# PROGRAMA PRINCIPAL #
######################
def Inicio():

    while True:
    
            # Leer Estado Contacto Rele
            if PinCRC.is_pressed:    # No pulsado
                    CRC=False
            else:                   # Pulsado
                    CRC=True
                    
            # Leer Fichero Caldera
    	TLFC[0],TLFC[1],TLFC[2]=Temporizador_s(TLFC[0],TLFC[1],TLFC[2],TM_LEER_FICHERO_CALDERA)
    
    	if (TLFC[2]==True):
                    LeerFichero_caldera()
                    TLFC[0]=False
    		TLFC[2]=False
    		print "Leer Fichero"
    		
            if (TERMOSTATO==1):
                      # Leer Tempertua
                    TLTA[0],TLTA[1],TLTA[2]=Temporizador_s(TLTA[0],TLTA[1],TLTA[2],TM_LEER_TEMPERATURA_AGUA)
                    if (TLTA[2]==True):
                            CALDERA[1]=(get_temp_sens(device_folder_0))
                            CALDERA[1]=(int(CALDERA[1]*10))
                            print "Leer Temperatura="+str(CALDERA[1]/10.0)
            
                            TLTA[0]=False
                            TLTA[2]=False
    
                    
                    CALDERA[0]=1
                   
                    
                    if (AUX_CC==True):
                            PinCC.off()
                            AUX_CC=False
                    if (ANT_CALDERA[0]==0):
                            PinCC.on()
                            AUX_CC=True
                            print('Encendida CALDERA')
    
                    TCRC[0],TCRC[1],TCRC[2]=Temporizador_s(TCRC[0],TCRC[1],TCRC[2],TM_CONFIRMAR_RELE)
                    if (TCRC[2]==True and CRC==False):
                            CALDERA[2]=1
    ##                        print ('ERROR RELE')
    ##                print ('TCRC='+str(TCRC))
    ##                print ('TLTA='+str(TLTA))
    ##                time.sleep(2)
                                            
            else:
                    CALDERA[0]=0
                    TCRC[0]=False
                    TCRC[2]=False
                    if (AUX_CA==True):
                            PinCA.off()
                            AUX_CA=False
                            if (CRC==True):
                                    CALDERA[2]=2
                    if (ANT_CALDERA[0]==1):
                            PinCA.on()
                            AUX_CA=True
                            print('CALDERA APAGADA')
    		
           
            print 'T='+str(CALDERA)
            print 'TA='+str(ANT_CALDERA)
            if(ANT_CALDERA!=CALDERA):
                    for i in range(N_VAR_CAL):
                            ANT_CALDERA[i]=CALDERA[i]
            print 'CRR='+str(CRC)
            print 'TERMOSTATO='+str(TERMOSTATO)
            #print 'Ventana=['+str(SENSORES)+']'
            if (CALDERA[2]==1):
                    print 'ERROR RELE AL CERRAR'
            elif (CALDERA[2]==2):
                    print 'CALDERA ABIERTA RELE CERRADO'
    
    	time.sleep(2)
