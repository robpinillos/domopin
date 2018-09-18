#!/usr/bin/env python

import rospy
import std_srvs.srv 
from std_msgs.msg import String
from domopin_msgs.msg import *
from domopin_msgs.srv import *


import time
import json
import os


from array import *

import threading


import caldera as boiler


global room_config
global rooms_list

stepDelay = 0.5                    # Number of seconds between each sequence step


def load_json(path):
    print "load " ,path   
    # Reading data
    with open(path, 'r') as f:
        data = json.load(f)

    return data
    



def callback_status(msg):
    #action=Action()

    #print 'Recibido command room=',msg.roomid

    global rooms_list

    b_new=True
    for i in range(len(rooms_list)):
        
        if rooms_list[i].roomid == msg.roomid:
            rooms_list[i]=msg
            b_new=False
               
    if b_new is True:
        rooms_list.append(msg)
        



def callback_command(req):
    
    jreq = json.loads(req.data)
    #action=Action()
    for iaction in jreq['action']:
        if iaction['roomid']==room_config['roomid']:

            if iaction['type']=='CONFIG':
            
                print 'CONFIG::',iaction
        
            if iaction['type']=='COMMAND':
            
                if  iaction['device']=='boiler':
    
                    boiler.Recibir_comando_web(iaction['command'],iaction['value'])
                

    
def publish_room_state():


    #print 'room_config=',room_config
    try:
        databoiler=boiler.Publicar_estado_actual()
    except:
        databoiler=[0,0,0]
        
    current_status=BoilerStatus()
    
    
    current_status.on_off=bool(databoiler[0])
    current_status.water_temp=int(databoiler[1])
    current_status.error=int(databoiler[2])
    
    current_status.active_rooms=[]
    
    for iroom in rooms_list:
        
        for iradiator in iroom.array_rad:
        
            if iradiator.boiler_on == 1:
                current_status.active_rooms.append(iroom.roomid)
    
    

   
    pub_msg_room_status.publish(current_status)
    #print "Published pub_msg_room_status"

def update():
    
    print 'update'
    while not rospy.is_shutdown():
        
        ### TERMOSTATO 
        valtermostato=0
        
        for iroom in rooms_list:
            
            for iradiator in iroom.array_rad:
            
                if iradiator.boiler_on == 1:
                    valtermostato=1


        boiler.Actualizar_valores('TERMOSTATO',valtermostato)

        publish_room_state()
        
        time.sleep(stepDelay)                   # Wait between steps

    
    
def shutdown():
    
    print "shutdown"

    try:
        boiler.Cerrar_programa()
    except:
        pass

    
if __name__ == "__main__":
    
    global room_config
    
        
    name_configfile=rospy.get_param('/config_file', '../conf/room_config.json')

    print 'name_configfile=',name_configfile
    room_config=load_json(name_configfile)

    rospy.init_node('domopin_central')
    rospy.on_shutdown(shutdown)

    pub_msg_room_status=rospy.Publisher('domopin/central_status', BoilerStatus, queue_size=1)
    
    rospy.Subscriber("domopin/room_status", RoomStatus, callback_status)    
    rospy.Subscriber("domopin/command", String, callback_command)
    

    boiler.Inicio(room_config)

    t_boiler= threading.Thread(target=boiler.Bucle_principal)
    t_boiler.start() 

    global rooms_list
    rooms_list=[]    
    print "Started"
    
    update()
    
#    t_update = threading.Thread(target=update)
#    t_update.start()



    #rospy.spin()
    
    
    
