#!/bin/bash


echo "Comprobando conexion internet"


while sleep 1
do
	ping_test=`ping -c 2 8.8.8.8 > /dev/null`
	if [ $? == 0 ]
	then sleep 1
		echo "iniciando"
		./start_domopin_tmux.sh
		break
	fi
	#if [ $count == 5 ]
	#then echo "." 
	#	break
	#fi
	#((count++))
	echo "..."
done









 

