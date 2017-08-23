import time
from datetime import datetime
#import spidev
import os
import wiringpi2 as wiringpi

wiringpi.wiringPiSetupGpio()

# Definimos entradas y salidas
#Entradas
wiringpi.pinMode(6,0)		# Pulsador Subir
wiringpi.pinMode(13,0)		# Pulsador Bajar
wiringpi.pinMode(19,0)		# Confirmar Rele Subir
wiringpi.pinMode(26,0)		# Confirmar Rele Bajar	


#Salidas
wiringpi.pinMode(27,1)		# Rele Subir Persiana
wiringpi.pinMode(17,1)		# Rele Bajar Persiana


#Inicialiazamos Salidas
wiringpi.digitalWrite(27,0)
wiringpi.digitalWrite(17,0)



#Variables
N_VARIABLES=7			# Num. variables
actual=[0,0,0,0,0,0,0]
anterior=[0,0,0,0,0,0,0]
for i in range(N_VARIABLES):
	actual[i]=0		# [0]R.Subir;[1]R.Bajar;[2]Posicion;[3]P.Subir;[4]P.Bajar;[5]Error;[6]Temperatura
        anterior[i]=0


CRS=False			# Confirmar Rele Subida
CRB=False			# Confirmar Rele Bajada

PA=False			# Persiana Abierta
PC=False			# Persiana Cerrada


FSPS=False			# Flanco de subida Pulsador Subir
AFSPS=False			# Auxiliar Flanco d eSubida Pulsador Subir

FSPB=False			# Flanco de Subida Pulsador Bajar
AFSPB=False			# Auxiliar Flnaco Subida Pulsador Bajar 

AUXP=False			# Auxiliar pulsadores una vez

POS_ACTUAL=str(0)			# Posicion Persiana Actual)
POS_DESEADA=0			# Posicion Persiana Deseada

CONT_1=False			# Auxiliar primer ciclo de ejecucion


###Temporizadores
T_CONFIRMAR_RELE=1		# Tiempo Confirmar Reles 1 segundo

TCRS=[False,0,False]		# Temporizador Confimar Rele Subida [contando el tmepo, tiempo contado,Si ha llegaso a l atemporizacion]			
TCRB=[False,0,False]		# Temporizador Confirmar Rele Bajada

T_POSICION_PERSIANA=12000 # Tiempo que tarda en subir persiana (segundos)
TPP=[False,0,False]		# Temporizador Posicion Persiana


# ESTADOS
N_ESTADOS=6			# Numero de Estados
E=[0,0,0,0,0,0,0]
for i in range(N_ESTADOS):
	E[i]=0	# Ponemos todos los estados como falsos



###################
# LEEMOS ENTRADAS #
###################

def Leer_entradas():

	global actual
	global FSPS
	global AFSPS
	global FSPB
	global AFSPB
	global CRS
	global CRB
	global PA
	global PC
	global POS_ACTUAL
	
	actual[3]=wiringpi.digitalRead(6)			# Leer P. Subir Persiana
	FSPS,AFSPS=FlancoDeSubida(bool(actual[3]),AFSPS)	# Flanco Subida Pul. subir
			
	actual[4]=wiringpi.digitalRead(13)			# Leer P. Bajar
	FSPB,AFSPB=FlancoDeSubida(bool(actual[4]),AFSPB)	# Flanco Subida Pul. Bajar
			
	CRS=wiringpi.digitalRead(19)				# Leer confirmar Rele Subida
	CRB=wiringpi.digitalRead(26)				# Leer Confirmar Rele Bajada
	
	if (POS_ACTUAL>=T_POSICION_PERSIANA):
		PA=True
		POS_ACTUAL=T_POSICION_PERSIANA
	else:
		PA=False

	if (POS_ACTUAL<=0):
		PC=True
		POS_ACTUAL=0
	else:
		PC=False
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
		tiempo=time.time()
		auxt=True
		T=False
	else:
		tiempot=time.time()
		if (((tiempot-tiempo)//1)>=TIEMPO):
			T=True

	return auxt,tiempo,T


###########
# SALIDAS #
###########
def Salidas():
	global actual
	global anterior

	if (actual[0]==0 and anterior[0]==1):	
		wiringpi.digitalWrite(27,0)
		EscribirFichero()
	
	if (actual[0]==1 and anterior[0]==0):
		wiringpi.digitalWrite(27,1)
	
	if (actual[1]==0 and anterior[1]==1):
		wiringpi.digitalWrite(17,0)
		EscribirFichero()
	
	if (actual[1]==1 and anterior[1]==0):
		wiringpi.digitalWrite(17,1)

	if (actual[5]==1):
		print("ERROR EN RELE SUBIR")

	if (actual[5]==2):
		print("ERROR EN RELE BAJAR")

	if(anterior!=actual):
		for i in range(N_VARIABLES):
			anterior[i]=actual[i]

	return


################
# LEER FICHERO #
################
def LeerFichero():
	global POS_ACTUAL

	f=open("posicion.txt","r")
	a=0
	while True:
		a=a+1
		linea=f.readline()
		if not linea: break
		if (a%2==0):
			POS_ACTUAL=int(linea)
	f.close()
	return



####################
# ESCRIBIR FICHERO #
####################
def EscribirFichero():
	global POS_ACTUAL
	print("POSICION_ACTUAL="+str(POS_ACTUAL))
	f=open("posicion.txt","r+")
	f.seek(0,0)
	f.write('Posicion:\n')
	f.write(str(int(POS_ACTUAL)))
	f.close()
	return



######################
# PROGRAMA PRINCIPAL #
######################
#def Init():

while True:
		
	Leer_entradas()			# Leemos las entradas

		
		# ESTADO 0 - Leer de fichero tras ejecucion nueva
	i=1
	while (i<N_ESTADOS):
		if (E[i]==0):
			E[0]=1
		else:
			E[0]=0	
			break
		i=i+1
		
		

	# ESTADO 1 - Espera
	if ((E[0]==1 and CONT_1==True) or
            (E[2]==1 and (PA==True or (FSPS==True and AUXP==True))) or
	    (E[4]==1) or
            (E[3]==1 and (PC==True or (FSPB==True and AUXP==True))) or
            (E[5]==1)):
		E[1]=1
		E[0]=0
		E[2]=0
		E[3]=0
		E[4]=0
		E[5]=0


	# ESTADO 2 - Subir
	if ((E[1]==1 and FSPS==True and AUXP==False and PA==False and actual[4]==0 and actual[5]!=1) or
            (E[3]==1 and FSPS==True and actual[5]!=1 and PA==False)):    
		E[2]=1
		E[1]=0
		E[3]=0
		

	# ESTADO 3 - Bajar
	if ((E[1]==1 and FSPB==True and AUXP==False and PC==False and actual[3]==0 and actual[5]!=2) or
            (E[2]==1 and FSPB==True and actual[5]!=2 and PC==False)):
		E[3]=1
		E[1]=0
		E[2]=0

		
	# ESTADO 4 - Error Rele Subir
	if (E[2]==1 and CRS==False and TCRS[2]==True):
		E[4]=1
		E[2]=0


	# ESTADO 5 - Error Rele Bajar
	if (E[3]==1 and CRB==False and TCRB[2]==True):
		E[5]=1
		E[3]=0
			
			
	#print "E="+str(E)	
	#time.sleep(2)
	#### EFECTOS
	if (E[0]==1):	# Leemos valores de fichero
		LeerFichero()
		CONT_1=True

	if (E[1]==1):	# Espera
		AUXP=False	# Ponemos el pulsador auxiliar en Falsp

	if (E[2]==1):	# Subir
		actual[0]=1
		TCRS[0],TCRS[1],TCRS[2]=Temporizador(TCRS[0],TCRS[1],TCRS[2],T_CONFIRMAR_RELE)
		AUXP=True
			
	else:
		actual[0]=0
		TCRS[0]=False
		TCRS[2]=False
			
	if (E[3]==1):	# Bajar
		actual[1]=1
		TCRB[0],TCRB[1],TCRB[2]=Temporizador(TCRB[0],TCRB[1],TCRB[2],T_CONFIRMAR_RELE)
		AUXP=True
			
	else:
		actual[1]=0
		TCRB[0]=False
		TCRB[2]=False

			 
	if (E[2]==1 or E[3]==1):	# Calulo posicion persiana
		TPP[0],TPP[1],TPP[2]=Temporizador(TPP[0],TPP[1],TPP[2],T_POSICION_PERSIANA)
		if (E[2]==1):
			POS_ACTUAL=POS_ACTUAL+int((time.time()-TPP[1])//1) # Sumamos tiempo
		else:
			POS_ACTUAL=POS_ACTUAL-int((time.time()-TPP[1])//1) # Restamos tiempo
	else:
		TPP[0]=False
		TPP[2]=False
		
	if (E[4]==1):	# Error Rele Subir
		actual[5]=1
	elif (E[5]==1):	# Error Rele Bajar
		actual[5]=2
	
	#print "actual  ="+str(actual)
	#print "anterior="+str(anterior)
	#print "POS_ACTUAL="+str(POS_ACTUAL)
	#print "PA="+str(PA)
	#print "PC="+str(PC)
	#print "AUXP="+str(AUXP)
	Salidas()
	
	
	time.sleep(0.2)

			

	
	