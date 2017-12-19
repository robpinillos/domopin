# domopin
Home automation under ROS with raspberry pi




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


rostopic pub -1 domopin/command std_msgs/String '{ "type":"COMMAND", "roomid": 1, "action":[{"device":"radiator", "id": 1,"command":"setpoint" , "value":270 }]}' 

rostopic pub -1 domopin/command std_msgs/String '{"action":[{"room":2,"device":"radiator", "id": 1,"command":"setpoint" , "value":270 }]}' 

 

TODO:

* Read the schedule and and check the conditions to launch the tasks
* Publish command to enable/disable the termostat

* Pygame interface LCD32 inchs




