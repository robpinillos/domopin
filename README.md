# domopin
Home automation under ROS with raspberry pi


##LAUNCH

roscd domopin_central
roslaunch domopin_central domopin.launch


roscd domopin_room
roslaunch domopin_room domopin_room.launch


roslaunch rosbridge_server rosbridge_websocket.launch

* interface

roscd interface_touchscreen/www
python -m SimpleHTTPServer

>> Go to http://localhost:8000/index.html 

##TODO

### ROBERTO
* Apagar luz pantalla
* Interfaz pantalla táctil web
* Comprobar pérdida comunicación > T agua

#### PERSIANA
* Leer config_room (path)

#### INTERFAZ
* PRINCIPAL
	> T actual grande
	> T consigna y próxima cambio
	> Estado caldera
	> Estado relé
	> Estado persiana y próximo cambio
* RADIADOR
	> Ajuste temporal


## TMUX

   tmux a  --> connect (atached)
   ctrl + B, n(screen number)
   ctrl + b, d --> disconnect (detached)
   tmux kill-server --> close all sessions


##DEPENDENCIAS
* multimaster:
	git clone https://github.com/fkie/multimaster_fkie.git
* sensor de temperatura:
	En /boot/config.txt añadir:
		dtoverlay=w1-gpio,gpiopin=19
* librería gpiozero:
	sudo apt-get install python-gpiozero
* tmux:
	sudo apt-get install tmux

##MULTIMASTER


* en ~/.bashrc:
	export ROS_MASTER_URI=http://<hostname or IP local>:11311

*  Activar multicast:
 > Para cada PC comprobar si está activado el multicast:
 ```
 cat /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts 
 ```
 Si devuelve 0 está activado.
 Si no:
  > en /etc/sysctl.conf añadir:
 ```
 net.ipv4.icmp_echo_ignore_broadcasts=0
 ```
  > PAra reiniciar el servicio:
 ```
 sudo service procps restart
 ```
* PAra comprobar que interfaz multicast está activa (defecto 224.0.0.1):
 ```
 netstat -g
 ```
* Si todo está bien configurado con el siguiente comando debería responder cada una de las IPs presentes en multicast
 ```
 ping 224.0.0.1
 ```

* En cada PC exportar ROS_MASTER_URI con su propia IP:

export ROS_MASTER_URI=http://<hostname or IP local>:11311

* En cada PC en /etc/hosts añadir los hostname de cada PC (todos en todos)

03/10/2018

* Changed  "/domopin/command" wich NOW is  type={'config','action'}

    #{"type":"action","action": [{"roomid": room_config['roomid'],"device":"blind", "id": 1,"command":"position" , "value":value }]}  
    #{"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  

05/07/2018

* room status data is full available now in termostato.py and persiana.py
* Multimaster
* Added ping to google in start launcher


29/08/2017

* domopin_room_main call persiana.Publicar_estado() periodically
* Create class to manage the ros topics and the communications between domopin_main and persiana


28/08/2017

* domopin_room is able to work without central
* Load room' configuration from /conf/config_room.json
* Room' schedule is available in /conf/schedule.json
* Subscribed to "/domopin/command" wich NOW is type "String" (json_stringfy) type={'CONFIG','COMMAND'}

	{ "type":"CONFIG", "roomid": 1, "action":"refresh"}
	{ "type":"COMMAND", "roomid": 1, "action":[{"device":"blind", "id": 1,"command":"position" , "value":1 }]}
	{ "type":"COMMAND", "roomid": 1, "action":[{"device":"radiator", "id": 1,"command":"position" , "value":1 }]}
	{ "type":"COMMAND", "roomid": 1, "action":[{"device":"radiator", "id": 1,"command":"setpoint" , "value":270 }]}










