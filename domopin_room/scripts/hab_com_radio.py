#!/usr/bin/env python



from nrf24 import NRF24

import time
import random
import os
import sys
from datetime import datetime


import domopin_room
# Variables


N_CAMBIO=False


pipes=[[0x65, 0x64, 0x6f, 0x4e, 0x34],[0x65, 0x64, 0x6f, 0x4e, 0x33]]

radio = NRF24()
radio.begin(0, 0, 25, 18)  #selecionamos los pins CE y IRQ
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setPALevel(NRF24.PA_MAX)

radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])

radio.startListening()
radio.printDetails()
radio.powerUp()

# ESTADOS
N_ESTADOS=8
C=[0,0,0,0,0,0,0,0]

# CONTADORES
C_HABITACIONES=1
CONTH=0

C_ESPERA=3  # sin sleep 20
CONTC=0

#TEMPORIZADORES
T_COMUNICAR=250 #80
TC=False
tempTC=0

T_ESPERA_LEER=7
TLC=False
tempTLC=0


#VARIABLES AUXILIARES
LECTURA=False
CAMBIO=False
LW=False


#[],0-subir,1-bajar,2-posicion,3-b.subir,4-b.bajar,5-error,6-temp

#actual=['0','0','000','0','0','0','000']
#anterior=['0','0','000','0','0','0','000']
#web=['000','0','0','000'] #0-POSICION,1-subir,2-bajar,3-temperatura

actual=[0,0,2,0,0,0,0]   #[0]Subiendo;[1] Bajando; [2]posicion; [3]pulsador arriba;[4]pulsador abajo; [5]error; [6]temperatura
anterior=[0,0,0,0,0,0,0]
web=['000','0','0','000'] #0-POSICION,1-subir,2-bajar,3-temperatura


def Publicar_estado():

    temp=actual[6]
    #domopin_main.publish_blind_state(actual)
    domopin_room.publish_room_state(actual)
    


def Recibir_comando_web(dispositivo,accion):
    
    print "Recibido comando web: dispositivo:",dispositivo,", accion:",accion



# FUNCION LEER RF
def leer(recv_buffer):
    global LECTURA
    global actual
    global CONTH



    recibido=''.join(chr(i) for i in recv_buffer)
#    print 'RECIBIDO ='+recibido
#    print 'RECIBIDO ='+recibido[0:8]
#    print '==HA0'+str(CONTH)+'#RB#'
#    print 'CONTH='+str(CONTH)
    if (recibido[0:8]=='HA0'+str(CONTH+1)+'#RB#'):
        recibido=recibido[0:25].split('#')
        #print 'recibido='+str(recibido)
        for i in range(len(actual)):		
            actual[CONTH][i]=str(recibido[i+2])
        LECTURA=True

    else :
        LECTURA=False
    
#    print 'Funcion leer,LECTURA='+str(LECTURA)
#    print 'actual[]='+str(actual[CONTH])
    
    return


#FUNCION ESCRIBIR RF

def escribir():
    
    global CONTH
    global actual
    global envio
    global LW
	
	
    if (LW==True):
        envio='RB#HA0'+str(CONTH+1)+'#W'
        for i in range(len(web)):
            envio=envio+'#'+str(web[i])
        LW=False
    else:
        envio='RB#HA0'+str(CONTH+1)+'#C#'
#    print 'escribir actual['+str(CONTH)+']='+str(actual[CONTH])
#    print 'envio='+str(envio)	
#    print CONTH
#    print str(LW[CONTH])


    return
                
# FUNCION SALIDA

def salida():
    global actual
    global anterior
    global CONTH
    global CAMBIO
    global N_CAMBIO

CAMBIO=False
print 'actual['+str(CONTH)+']='+str(actual[CONTH])
print 'anterior['+str(CONTH)+']='+str(anterior[CONTH])
for i in range (len(actual)):
    if (str(actual[i])!=str(anterior[i])):
        anterior[i]=str(actual[i])
        CAMBIO=True
        if (i==2):
            N_CAMBIO=True
    elif (i==2 and str(actual[i])==str(anterior[i]) and N_CAMBIO==True):
        N_CAMBIO=False
        if (str(actual[i])=='575' or str(actual[i])=='675' or str(actual[i])==610):
            os.system ('echo "Persiana ABIERTA" | mutt -s "PERSIANA" antoniopinillos@hotmail.com,lapiti-19@hotmail.com')	
            #print 'PERSIANA ABIERTA'
        elif (str(actual[i])=='240' or str(actual[i])=='140'):
            os.system ('echo "Persiana posicion DESPERTAR" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA DESPERTAR'
        elif (str(actual[i])=='315' or str(actual[i])=='215'):
            os.system ('echo "Persiana posicion 1/4" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')
            #print 'PERSIANA 1/4'
        elif (str(actual[i])=='210' or str(actual[i])=='110'):
            os.system ('echo "Persiana posicion VERANO" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA VERANO'
        elif (str(actual[i])=='000'):
            os.system ('echo "Persiana posicion CERRADA" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA CERRADO'
        elif (str(actual[i])=='495' or str(actual[i])=='395'):
            os.system ('echo "Persiana posicion 1/2 (MEDIA VENTANA)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')
            #print 'PERSIANA 1/2'
        elif (str(actual[i])=='590' or str(actual[i])=='490'):
            os.system ('echo "Persiana posicion 3/4" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA 3/4'
        elif (int(actual[i])<495):
            os.system ('echo "Persiana en parte inferior" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA 3/4'
        elif (int(actual[i])>495):
            os.system ('echo "Persiana en parte superior" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
            #print 'PERSIANA 3/4'

#    print 'CAMBIO='+str(CAMBIO)
#    print 'N_CAMBIO='+str(N_CAMBIO)
#    print int(actual[0][2])
    return
	

while True:  

    pipe=[0]

    if (radio.available(pipe)):      
        while (radio.available(pipe)):
            ecv_buffer=[]
            radio.read(recv_buffer)
        leer(recv_buffer)
    else:
        LECTURA=False
	

    if FSS0_HA01==True:
        print ''
    elif (FSS_HA01==True or FSS1_HA01==True):
#        web[0][0]='675'
#        LW[0]=True
#        num_random=random.randint(-15,15)
#        HORA_SUBIR_HA01=HORA_RANDOM_SHA01-int(num_random)
#        #HORA_VERANONOCHE_HA01=HORA_SUBIR_HA01+39
#        #HORA_SUBIR1_HA01=HORA_RANDOM_S1HA01-int(random.randint(-20,20))
#        (FSS_HA01,AFSS_HA01)=Hora(HORA_SUBIR_HA01,False,AFSS_HA01)	
#        #(FSS1_HA01,AFSS1_HA01)=Hora(HORA_SUBIR1_HA01,False,AFSS1_HA01)	
#        #os.system ('echo "Subiendo" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
#        f=open("hora.txt","r+")
#        f.seek(7,0)
#        f.write(str(HORA_SUBIR_HA01)+'\n')
#        #f.seek(21,0)
#        #f.write(str(HORA_SUBIR1_HA01)+'\n')
#        #f.seek(69,0)
#        #f.write(str(HORA_VERANONOCHE_HA01)+'\n')
#        f.close()
        pass

    elif (FSD_HA01==True):	#DESPERTAR
        web[0]='240'  # estos valores son si esta la persiana arriba
        LW=True
        #os.system ('echo "En posicion 2 (despertar)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
	

	elif FSVN_HA01==True: 	#1/4
		web[0]='315'
		LW=True
		#os.system ('echo "En posicion 3 (1/4 ventana)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	

	elif FSV_HA01==True:  	#VERANO
		web[0]='210'
		LW=True
		#os.system ('echo "En posicion 1 (verano)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
	
	elif FSB_HA01==True or FSB1_HA01==True:
#		web[0][0]='000'
#		LW[0]=True
#		HORA_RANDOM_BHA01=HORA_RANDOM_BHA01+1
#		HORA_BAJAR_HA01=HORA_RANDOM_BHA01-int(random.randint(-15,15))
#		(FSB_HA01,AFSB_HA01)=Hora(HORA_BAJAR_HA01,False,AFSB_HA01)	
#		if (HORA_BAJAR_HA01%100>59):
#			HORA_BAJAR_HA01=HORA_BAJAR_HA01-40
#		#os.system ('echo "Persiana cerrada" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
#		f=open("hora.txt","r+")
#		f.seek(81,0)
#		f.write(str(HORA_BAJAR_HA01)+'\n')
#		f.close()
            

    elif FSBN_HA01==True:	#1/2
        web[0]='495'
        LW=True
        #os.system ('echo "En posicion 4 (media ventana)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
	

    elif FSL_HA01==True:	#3/4
        web[0]='590'
        LW=True
        #os.system ('echo "En posicion 5 (3/4 ventana)" | mutt -s "PERSIANA" antoniopinillos@hotmail.com ,lapiti-19@hotmail.com')	
	
#	



    # ESTADO C0
    i=1
    while(i<N_ESTADOS):

        if(C[i]==0):
            C[0]=1
        else:
            C[0]=0
            break
        i=i+1
	
    if ((C[5]==1 or C[6]==1) and CONTH>=C_HABITACIONES):
        C[0]=1
        C[5]=0
        C[6]=0

    if (C[0]==1):
        tempTC=tempTC+1
        if (tempTC>=T_COMUNICAR):
            TC=True
        else:
            tempTC=0
            TC=False
		
    #ESTADO C1 
    if (C[0]==1 and TC==True):
        C[1]=1
        C[0]=0
    		
    if (C[1]==1):
        CONTH=0

	
    #ESTADO C2
    if (C[1]==1 or((C[5]==1 or C[6]==1) and CONTH<C_HABITACIONES)):
        C[2]=1
        C[1]=0
        C[5]=0
        C[6]=0
    if (C[2]==1):
        CONTE=0

    #ESTADO C3 
    if (C[2]==1 or(C[7]==1 and (CONTE<C_ESPERA and TEL==True))):
    C[3]=1
    C[2]=0
    C[7]=0
    
    if (C[3]==1):
        escribir()
        radio.stopListening()
        ok = radio.write(envio)
#            if (ok==0):
#                print 'ERROR DE ENVIO'
#            else:
#                print 'ENVIO o.k.'
			
       radio.startListening()
#		print 'ENVIO='+envio

        CONTE=CONTE+1
        tempTEL=0
        TEL=False
#	else:
#		LW[CONTH-1]=False


    #ESTADO 7
    if (C[3]==1):
        C[7]=1
        C[3]=0
    if (C[7]==1):
        tempTEL=tempTEL+1
        if (tempTEL>=T_ESPERA_LEER):
            TEL=True
#		LW[CONTH]=False

    else:
        tempTEL=0
        TEL=False
        #LW[CONTH]=False
		

    #ESTADO C4 
    if (C[7]==1 and ((TEL==True and CONTE>=C_ESPERA)or LECTURA==True)):
        C[4]=1
        C[7]=0
    
    if (C[4]==1):
        salida()
    
    #ESTADO C5
    if (C[4]==1 and CAMBIO==True):
        C[5]=1
        C[4]=0
    if (C[5]==1):
        CONTH=CONTH+1
    
    #ESTADO C6
    if (C[4]==1 and CAMBIO==False):
        C[6]=1
        C[4]=0
    if (C[6]==1):
        CONTH=CONTH+1

	
	
#   print 'C='+str(C)
#   time.sleep(0.5)
    time.sleep(0.05)
#   print str(LW)

    # SALIDAS
#	
#   if(C[5]==1):
#   print 'HA0'+ str(CONTH)+'='+str(actual[CONTH-1]) +'     ('+str(datetime.now().hour)+':'+str(datetime.now().minute)+')'	
#   print "Despertar_HA01: " + str(HORA_DESPERTAR_HA01)
#   print "Verano_HA01: " + str(HORA_VERANO_HA01)
#   print "VeranoNoche_HA01: " + str(HORA_VERANONOCHE_HA01)
#   print "Subir_HA01: " + str( HORA_SUBIR_HA01)
#   print "Subir1_HA01: " + str( HORA_SUBIR1_HA01)
#   print "Bajar_HA01: " + str(HORA_BAJAR_HA01)
#   print "Bajar Noche_HA01: " + str(HORA_BAJAR_NOCHE_HA01)

    
          
