##cambiamos si esta arriba o abajo, no se pulsa
from gpiozero import LED, Button
import time
import sys
from datetime import datetime
#import spidev
import os
import smbus

bus=smbus.SMBus(1)

DEVICE=0x20			#Device adress (A0-A2)
IODIRA=0x00			# Byte A 0 salida 1 entrada
IODIRB=0x01			#Byte B = salida 1 entrada
OLATA=0x14			#Salidas A
OLATB=0x15			# Salidas B
GPIOA=0x12			# Registros para entradas A
GPIOB=0x13			# Registro entradas B

#Ponemos entradas/salidas byte A y byte B
bus.write_byte_data(DEVICE,IODIRA,0b10000000)
bus.write_byte_data(DEVICE,IODIRB,0b00111111)

#Ponemos todas las salidas a 0
bus.write_byte_data(DEVICE,OLATA,0b00000000)
bus.write_byte_data(DEVICE,OLATB,0b00000000)



# Definimos entradas y salidas
#Entradas
#Lo lee el programa termostato
#PinSV=Button(21)        # Sensor Ventana
#PinSP=Button(20)         # Sensor Puerta




#Variables
N_VAR_PER=6			# Num. variables
PERSIANA=[0,0,0,0,0,0]
ANT_PERSIANA=[0,0,0,0,0,0]
for i in range(N_VAR_PER):
	PERSIANA[i]=0		# [0]R.Subir;[1]R.Bajar;[2]Posicion;[3]P.Subir;[4]P.Bajar;[5]Error;
        ANT_PERSIANA[i]=0

N_VAR_SEN=2                     # Sensores puertas y ventana abierta
SENSORES=[0,0]                  # [0] vENTANA;[1] PUERTA

CRS=False			# Confirmar Rele Subida
CRB=False			# Confirmar Rele Bajada

PA=False			# Persiana Abierta
PC=False			# Persiana Cerrada

SPA=False                       # Sensor Puerta Abierta


FSPS=False			# Flanco de subida Pulsador Subir
AFSPS=False			# Auxiliar Flanco de Subida Pulsador Subir

FSPB=False			# Flanco de Subida Pulsador Bajar
AFSPB=False			# Auxiliar Flnaco Subida Pulsador Bajar 

AUXP=False			# Auxiliar pulsadores una vez

FSP1=False			# Flanco de Subida Pulsador 1
AFSP1=False			# Auxiliar Flnaco Subida Pulsador 1

FSP2=False			# Flanco de Subida Pulsador 2
AFSP2=False			# Auxiliar Flnaco Subida Pulsador 2

FSP3=False			# Flanco de Subida Pulsador 3
AFSP3=False			# Auxiliar Flnaco Subida Pulsador 3 

POS_ACTUAL=str(0)		# Posicion Persiana Actual)
POS_DESEADA=0			# Posicion Persiana Deseada
POS_DESEADA_WEB=0			# Posicion Persiana Deseada

CONT_1=False			# Auxiliar primer ciclo de ejecucion

AUX_SUBIR=True                  # Auxiliar para saber si persiana esta subiendo o bajando


###Temporizadores
T_CONFIRMAR_RELE=1000		# Tiempo Confirmar Reles 1 segundo

TCRS=[False,0,False]		# Temporizador Confimar Rele Subida [contando el tmepo, tiempo contado,Si ha llegaso a l atemporizacion]			
TCRB=[False,0,False]		# Temporizador Confirmar Rele Bajada

T_POSICION_PERSIANA=29500 # MILISEGUNDOS Tiempo que tarda en subir persiana (segundos)
T_10_VERANO=5000                 # Posicion Verano desde cerrado
T_11_VERANO=6500                 # Posicion Verano desde abierto
T_20_DESPERTAR=7000             # Posicion Despertar desde cerrado
T_21_DESPERTAR=8800             # Posicion Despertar desde abierto
T_50_TRESCUARTO=26000           # Posicion 3/4 desde cerrado
T_51_TRESCUARTO=27000           # Posicion 3/4 desde abierto

TPP=[False,0,False]		# Temporizador Posicion Persiana


# ESTADOS
N_EST_PER=11			# Numero de Estados
P=[0,0,0,0,0,0,0,0,0,0,0]
for i in range(N_EST_PER):
	P[i]=0	# Ponemos todos los estados como falsos



#########################
# COMUNICACION#
global configuracion_hab
global EJECUTANDO
MANUAL_UP=0

def Publicar_estado_actual_persiana():

        #print 'PERSIANA=',PERSIANA
        return PERSIANA

def Actualizar_estado_habitacion(estado):

    #global estado_habitacion
    estado_habitacion=estado
    #print 'puerta cerrada=',estado_habitacion.array_window[0].door_closed
    #print 'ventana cerrada=',estado_habitacion.array_window[0].window_closed
    #SENSORES=[0,0]                  # [0] vENTANA;[1] PUERTA
    SENSORES[0]=estado_habitacion.array_window[0].window_closed
    SENSORES[1]=estado_habitacion.array_window[0].door_closed


def Actualizar_valores(datacmd,datavalue):
        global POS_DESEADA_WEB
        global MANUAL_UP
    
#    print "RADIADOR::Recibido comando :",datacmd,"=",datavalue
        if datacmd=='setposition':
                
                blind=configuracion_hab['device']['blind'][0]['positions']
                pos_deseada=[]
                for pose in blind:
                    if pose['name']==str(datavalue):
                        pos_deseada=pose['value']
                #parsear de position_1 > int
                sentido=0
                if AUX_SUBIR is True:
                    sentido=0
                else:
                    sentido=1
                    
                    
                POS_DESEADA_WEB=int(pos_deseada[sentido])
                print 'POS_DESEADA_WEB_INICIAL=',POS_DESEADA_WEB

        elif datacmd=='manual':
            
            if datavalue=='up':
                
            
                MANUAL_UP=1
            elif datavalue=='down':
                MANUAL_UP=-1
        


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







###################
# LEEMOS ENTRADAS #
###################

def Leer_entradas():

	global PERSIANA
	global FSPS
	global AFSPS
	global FSPB
	global AFSPB
	global FSP1
	global AFSP1
	global FSP2
	global AFSP2
	global FSP3
	global AFSP3
	global CRS
	global CRB
	global PA
	global PC
	global POS_ACTUAL
	global POS_DESEADA
	global POS_DESEADA_WEB
	global AUX_SUBIR
	global MANUAL_UP

	MyEntradasA=bus.read_byte_data(DEVICE,GPIOA)
	MyEntradasB=bus.read_byte_data(DEVICE,GPIOB)
    
	# Leer P. Subir Persiana
	
        if MyEntradasB & 0b00100000 == 0b00100000 or MANUAL_UP==1:    # Pulsado
                PERSIANA[3]=1
                MANUAL_UP=0
        else:                   # NO Pulsado
                PERSIANA[3]=0
	FSPS,AFSPS=FlancoDeSubida(bool(PERSIANA[3]),AFSPS)	# Flanco Subida Pul. subir
			

	# Leer P. Bajar

        if MyEntradasB & 0b00010000 == 0b00010000 or MANUAL_UP==-1:    # Pulsado
                PERSIANA[4]=1
                MANUAL_UP=0
        else:                   # no Pulsado
                PERSIANA[4]=0
	FSPB,AFSPB=FlancoDeSubida(bool(PERSIANA[4]),AFSPB)	# Flanco Subida Pul. Bajar
			
	# Leer confirmar Rele Subida
        if MyEntradasB & 0b00001000 == 0b00001000:    # Pulsado
                CRS=True
        else:                   # No Pulsado
                CRS=False
                
	# Leer confirmar Rele Bajada
        if MyEntradasA & 0b10000000 == 0b10000000:    # Pulsado
                CRB=True
        else:                   # No Pulsado
                CRB=False

	if (POS_ACTUAL>=T_POSICION_PERSIANA+4000):
		PA=True
		POS_ACTUAL=T_POSICION_PERSIANA
		AUX_SUBIR=False
		POS_DESEADA=POS_ACTUAL
		POS_DESEADA_WEB=POS_ACTUAL  


##		if (POS_ACTUAL==T_POSICION_PERSIANA and PERSIANA[0]==1) or POS_ACTUAL>T_POSICION_PERSIANA:
##                        POS_DESEADA=POS_ACTUAL
	else:
		PA=False

##	if (POS_ACTUAL==0 and PERSIANA[1]==1) or POS_ACTUAL<0:
	if (POS_ACTUAL<=0-4000):
		PC=True
		POS_ACTUAL=0
		AUX_SUBIR=True
		POS_DESEADA=POS_ACTUAL
		POS_DESEADA_WEB=POS_ACTUAL
	else:
		PC=False

        # Leer Pulsador 1,2 o 3

	#Pulsasdo 1
	if MyEntradasB & 0b00000001 == 0b00000001:    # Pulsado 1
		FSP1,AFSP1=FlancoDeSubida(True,AFSP1)
		FSP2,AFSP2=FlancoDeSubida(False,AFSP2)
		FSP3,AFSP3=FlancoDeSubida(False,AFSP3)
		if FSP1==True and AUX_SUBIR==True:
			POS_DESEADA=T_10_VERANO
		elif FSP1==True and AUX_SUBIR==False:
			POS_DESEADA=T_11_VERANO

	elif MyEntradasB & 0b00000010 == 0b00000010:    #Pulsado 2
		FSP2,AFSP2=FlancoDeSubida(True,AFSP2)
		FSP1,AFSP1=FlancoDeSubida(False,AFSP1)
		FSP3,AFSP3=FlancoDeSubida(False,AFSP3)
		if FSP2==True and AUX_SUBIR==True:
			POS_DESEADA=T_20_DESPERTAR
		elif FSP2==True and AUX_SUBIR==False:
			POS_DESEADA=T_21_DESPERTAR

	elif MyEntradasB & 0b00000100 == 0b00000100:    #Pulsado 3
		FSP3,AFSP3=FlancoDeSubida(True,AFSP3)
		FSP1,AFSP1=FlancoDeSubida(False,AFSP1)
		FSP2,AFSP2=FlancoDeSubida(False,AFSP2)
		if FSP3==True and AUX_SUBIR==True:
			POS_DESEADA=T_50_TRESCUARTO
		elif FSP3==True and AUX_SUBIR==False:
			POS_DESEADA=T_51_TRESCUARTO             
	

        # Leer Sensor Puerta Abierta
#        if PinSP.is_pressed:    # No pulsado
        #SENSORES[1]=1 # Esto es 0   
        #else:                   # Pulsado
        #        SENSORES[1]=1
	return
	

####################
# FLANCO DE SUBIDA #
####################
def FlancoDeSubida(P,AFSP):
	FSP=False		

	if P==True:
		if AFSP==False:
			FSP=True
		else:
			FSP=False
	if P==True:
		AFSP=True
	else:
		AFSP=False

	return(FSP,AFSP)




################
# TEMPORIZADOR #
################
def Temporizador(auxt,tiempo,T,TIEMPO):
	if auxt==False:
		tiempo=int(time.time()*1000)
		auxt=True
		T=False
	else:
		tiempot=int(time.time()*1000)
		if (((tiempot-tiempo))>=TIEMPO):
			T=True

	return auxt,tiempo,T


###########
# SALIDAS #
###########
def Salidas():
	global PERSIANA
	global ANT_PERSIANA

	salidaB=bus.read_byte_data(DEVICE,OLATB)

	if (PERSIANA[0]==0 and ANT_PERSIANA[0]==1):
		salidaB=salidaB & 0b01111111	
		EscribirFichero()
	
	if (PERSIANA[0]==1 and ANT_PERSIANA[0]==0):
		salidaB=salidaB | 0b10000000	

	
	if (PERSIANA[1]==0 and ANT_PERSIANA[1]==1):
		salidaB=salidaB & 0b10111111	
		EscribirFichero()
	
	if (PERSIANA[1]==1 and ANT_PERSIANA[1]==0):
		salidaB=salidaB | 0b01000000	

	if (PERSIANA[5]==1):
		print("ERROR EN RELE SUBIR")

	if (PERSIANA[5]==2):
		print("ERROR EN RELE BAJAR")

	if(ANT_PERSIANA!=PERSIANA):
		for i in range(N_VAR_PER):
			ANT_PERSIANA[i]=PERSIANA[i]
	bus.write_byte_data(DEVICE,OLATB,salidaB)
	return


################
# LEER FICHERO #
################
def LeerFichero():
	global POS_ACTUAL
	global PERSIANA

	f=open("posicion.txt","r")
	a=0
	while True:
		a=a+1
		linea=f.readline()
		if not linea: break
		if (a%2==0):
			POS_ACTUAL=int(linea)
			PERSIANA[2]=POS_ACTUAL
	f.close()
	return



####################
# ESCRIBIR FICHERO #
####################
def EscribirFichero():
	global POS_ACTUAL
	global PERSIANA
	print("POSICION_ACTUAL="+str(POS_ACTUAL))
	PERSIANA[2]=POS_ACTUAL
	f=open("posicion.txt","w")
	f.seek(0,0)
	f.write('Posicion:\n')
	f.write(str(int(POS_ACTUAL))+"\n")
	f.close()
	return



######################
# PROGRAMA PRINCIPAL #
######################
def Bucle_principal():
        global EJECUTANDO
        global CONT_1
        global P
        global POS_DESEADA
        global POS_DESEADA_WEB
        global POS_ACTUAL
        
        while EJECUTANDO:

        ##        print'POS_DESEADA_WEB_ANTES ENTRADAS='+str(POS_DESEADA_WEB)                        
                Leer_entradas()			# Leemos las entradas
        ##	print('actual='+str(PERSIANA))
        ##	time.sleep(2)
        ##        print'POS_DESEADA_WEB_DESPUES ENTRADAS='+str(POS_DESEADA_WEB)                        

                        
                        # ESTADO 0 - Leer de fichero tras ejecucion nueva
                i=1
                while (i<N_EST_PER):
                        if (P[i]==0):
                                P[0]=1
                        else:
                                P[0]=0	
                                break
                        i=i+1
                        
                        

                # ESTADO 1 - Espera
                if ((P[0]==1 and CONT_1==True) or
                    (P[2]==1 and ( PA==True or (FSPS==True and AUXP==True) or POS_DESEADA!=POS_ACTUAL)) or
                    (P[4]==1) or
                    (P[3]==1 and ( PC==True or (FSPB==True and AUXP==True) or POS_DESEADA!=POS_ACTUAL)) or
                    (P[5]==1) or
                    (P[8]==1)):
##              (P[6]==1 and (POS_DESEADA_WEB<=POS_ACTUAL or PA==True or FSPS==True or FSPB==True or SENSORES[1]==0)) or
##                    (P[7]==1 and (POS_DESEADA_WEB>=POS_ACTUAL or PC==True or FSPB==True or FSPS==True or SENSORES[1]==0))):
                        P[1]=1
                        P[0]=0
                        P[2]=0
                        P[3]=0
                        P[4]=0
                        P[5]=0
##                        P[6]=0
##                        P[7]=0
                        P[8]=0


                # ESTADO 2 - Subir
                if ((P[1]==1 and FSPS==True and AUXP==False and PA==False and PERSIANA[4]==0 and PERSIANA[5]!=1) or
                    (P[3]==1 and FSPS==True and AUXP==True and PERSIANA[5]!=1 and PA==False)):    
                        P[2]=1
                        P[1]=0
                        P[3]=0
                        

                # ESTADO 3 - Bajar
                if ((P[1]==1 and FSPB==True and AUXP==False and PC==False and PERSIANA[3]==0 and PERSIANA[5]!=2) or
                    (P[2]==1 and FSPB==True and AUXP==True and PERSIANA[5]!=2 and PC==False)):
                        P[3]=1
                        P[1]=0
                        P[2]=0

                        
                # ESTADO 4 - Error Rele Subir
                if (P[2]==1 and CRS==False and TCRS[2]==True):
                        P[4]=1
                        P[2]=0
                        P[1]=1


                # ESTADO 5 - Error Rele Bajar
                if (P[3]==1 and CRB==False and TCRB[2]==True):
                        P[5]=1
                        P[3]=0
                        P[1]=1

                # ESTADO 6 - Subir Automatico
                if (P[1]==1 and POS_DESEADA>POS_ACTUAL ):
                        P[6]=1
                        P[1]=0
                        
                # ESTADO 7 - BajarAutomatico
                if (P[1]==1 and POS_DESEADA<POS_ACTUAL):
                        P[7]=1
                        P[1]=0
                        
                # ESTADO 9 - Bajar Automatico web
                if (P[1]==1 and POS_DESEADA_WEB<POS_ACTUAL and SENSORES[1]==1 and PC==False):
                        P[9]=1
                        P[1]=0

               # ESTADO 10 - Subir Automatico web
                if (P[1]==1 and POS_DESEADA_WEB>POS_ACTUAL and SENSORES[1]==1 and PA==False):
                        P[10]=1
                        P[1]=0

                
##                print 'P="'+str(P)
                # ESTADO 8 - Cuando hay paro de subir/bajar automatico
                if ((P[6]==1 and (POS_ACTUAL>=POS_DESEADA or PA==True or FSPS==True or FSPB==True)) or
                    (P[7]==1 and (POS_ACTUAL<=POS_DESEADA or PC==True or FSPB==True or FSPS==True)) or
                    (P[9]==1 and (SENSORES[1]==0 or POS_ACTUAL<=POS_DESEADA_WEB or PC==True or FSPS==True or FSPB==True)) or
                    (P[10]==1 and (SENSORES[1]==0 or POS_ACTUAL>=POS_DESEADA_WEB or PA==True or FSPB==True or FSPS==True))):
                        P[8]=1
                        P[6]=0
                        P[7]=0
                        P[9]=0
                        P[10]=0
##        	print "P="+str(P)	
##        	time.sleep(2)
                #### EFECTOS
                if (P[0]==1):	# Leemos valores de fichero
                        LeerFichero()
                        CONT_1=True
                        POS_DESEADA=POS_ACTUAL
                        POS_DESEADA_WEB=POS_ACTUAL  

                if (P[1]==1):	# Espera
                        AUXP=False	# Ponemos el pulsador auxiliar en Falsp
        ##		POS_DESEADA=POS_ACTUAL

                if (P[2]==1 or P[6]==1 or P[10]==1):	# Subir
                        PERSIANA[0]=1
                        TCRS[0],TCRS[1],TCRS[2]=Temporizador(TCRS[0],TCRS[1],TCRS[2],T_CONFIRMAR_RELE)
                        AUXP=True
                        
                else:
                        PERSIANA[0]=0
                        TCRS[0]=False
                        TCRS[2]=False
                                
                if (P[3]==1 or P[7]==1 or P[9]==1):	# Bajar
                        PERSIANA[1]=1
                        TCRB[0],TCRB[1],TCRB[2]=Temporizador(TCRB[0],TCRB[1],TCRB[2],T_CONFIRMAR_RELE)
                        AUXP=True
                                
                else:
                        PERSIANA[1]=0
                        TCRB[0]=False
                        TCRB[2]=False

                
                if (P[2]==1 or P[3]==1 or P[6]==1 or P[7]==1 or P[9]==1 or P[10]==1):	# Calulo posicion persiana
                        
                        TPP[0],TPP[1],TPP[2]=Temporizador(TPP[0],TPP[1],TPP[2],T_POSICION_PERSIANA)
                        Tactual=int(time.time()*1000)
                        if (P[2]==1 or P[6]==1 or P[10]==1):
        ##                        print'POS_ACTUAL'+str(POS_ACTUAL)
        ##                        print'start='+str(TPP[1])
        ##                        print'time='+str(Tactual)
                                
                                POS_ACTUAL=POS_ACTUAL+Tactual-TPP[1] # Sumamos tiempo
        ##        		print'POS_ACTUAL'+str(POS_ACTUAL)
                                
                        else:
                                POS_ACTUAL=POS_ACTUAL-(Tactual-TPP[1]) # Restamos tiem
                                
                        TPP[1]=Tactual
                        PERSIANA[2]=int(POS_ACTUAL)
                        if (P[2]==1 or P[3]==1):
                                POS_DESEADA=POS_ACTUAL
                                POS_DESEADA_WEB=POS_ACTUAL                        
                else:
                        TPP[0]=False
                        TPP[2]=False
                
                if (P[4]==1):	# Error Rele Subir
                        PERSIANA[5]=1
                elif (P[5]==1):	# Error Rele Bajar
                        PERSIANA[5]=2

                if (P[8]==1):
                        POS_DESEADA=POS_ACTUAL
                        POS_DESEADA_WEB=POS_ACTUAL
          
        ##	print "actual  ="+str(PERSIANA)
        ##	print "anterior="+str(ANT_PERSIANA)
  ##      	print "POS_ACTUAL="+str(POS_ACTUAL)
  ##      	print "POS_DESEADA="+str(POS_DESEADA)
##       	print "POS_DESEADA_WEB="+str(POS_DESEADA_WEB)
        ##	print "PA="+str(PA)
        ##	print "PC="+str(PC)
        ##	print "AUXP="+str(AUXP)
                Salidas()
                
                #print "Confirmar Rele Radiador  ="+str(wiringpi.digitalRead(PinCRR))
                #print "Ventana  ="+str(wiringpi.digitalRead(PinVA))
        ##	print "Puerta  ="+str(wiringpi.digitalRead(PinPA))
        ##      print "Valvula Radiador  ="+str(wiringpi.digitalRead(PinVC))
        ##	print "Pulsador Subir  ="+str(wiringpi.digitalRead(PinPS))
        ##	print "Pulsador Bajar ="+str(wiringpi.digitalRead(PinPB))
        ##	print "Pulsador_1  ="+str(wiringpi.digitalRead(PinP1))
        ##	print "Pulsador_2  ="+str(wiringpi.digitalRead(PinP2))
        ##	print "Pulsador_3  ="+str(wiringpi.digitalRead(PinP3))
        ##	print "Abrir Radiador  ="+str(wiringpi.digitalRead(PinTAR))
        ##	print "Cerrar Radiador  ="+str(wiringpi.digitalRead(PinTCR))
        ##	print "=============="
        ##	time.sleep(0.2)
        ##	time.sleep(0.2)
                time.sleep(0.05)
                #wiringpi.digitalWrite(PinTCR,1)
        ##        time.sleep(0.5)
                #wiringpi.digitalWrite(PinTAR,1)
        ##        print'PA='+str(PA)
                                

                
                
        print "Cerrado"
        sys.exit(0)
