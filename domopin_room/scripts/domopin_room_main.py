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

import persiana_sim as blind

import radiador_sim as radiator

import time_alert 


global room_config


stepDelay = 0.5                    # Number of seconds between each sequence step


def load_json(path):
    print "load " ,path   
    # Reading data
    with open(path, 'r') as f:
        data = json.load(f)

    return data
    

def callback_central_status(msg):
    #action=Action()

    #print 'Recibido callback_central_status room=',msg.idroom

 
    val=msg.water_temp
    #print 'val water_temp=',val
    radiator.Actualizar_valores('temp_agua',val)


def callback_command(req):
    #action=Action()
    jreq = json.loads(req.data)
    
    parse_command(jreq)
    
    
def publish_room_state():


    #print 'room_config=',room_config
    try:
        datablind=blind.Publicar_estado_actual()
    except:
        datablind=[0,0,0,0,0,0,0]
    current_status=RoomStatus()
    current_status.roomid=room_config['roomid']
    current_blind_status=BlindStatus()
    current_blind_status.id=1
    current_blind_status.up=datablind[0]
    current_blind_status.down=datablind[1] 
    current_blind_status.position=datablind[2] 
    current_blind_status.push_up=datablind[3] 
    current_blind_status.push_down=datablind[4] 
    current_blind_status.error=datablind[5]
    current_status.array_blind.append(current_blind_status)
    
    try:
        dataradiator=radiator.Publicar_estado_actual()
    except:
        dataradiator=[0,0,0,0,0,0,0,0]
        
    current_radiator_status=RadiatorStatus()
    current_radiator_status.id=1
    current_radiator_status.on_off=bool(dataradiator[6])
    current_radiator_status.relay_opened=bool(dataradiator[3])
    current_radiator_status.valve_opened=bool(dataradiator[4])
    current_radiator_status.boiler_on=bool(dataradiator[7])
    current_radiator_status.current_temp=int(dataradiator[0])
    current_radiator_status.setpoint_temp=int(dataradiator[2])
    current_radiator_status.water_temp=int(dataradiator[1])
    current_radiator_status.error=int(dataradiator[5])
    current_status.array_rad.append(current_radiator_status)
    

    current_window_status=WindowStatus()
    current_window_status.id=1
    current_window_status.outside_temp=0
    current_window_status.window_opened=False
    current_window_status.door_opened=False
    current_window_status.error=-1
    current_status.array_window.append(current_window_status)
    
   
    pub_msg_room_status.publish(current_status)
#    print "Published pub_msg_room_status"




def parse_command(data):
    #print 'Recibido command room=',data['name],' dev=',msg.namedev,' action=',msg.action
    for iaction in data['action']:
        if iaction['roomid']==room_config['roomid']:
            
            print 'PARSE COMMAND  iaction=',iaction
            if  iaction['device']=='CONFIG':  
            
                pass

            elif  iaction['device']=='blind':       

                blind.Actualizar_valores(iaction['command'],iaction['value'])


            elif  iaction['device']=='radiator':

                radiator.Actualizar_valores(iaction['command'],iaction['value'])
            

def update():
    
#    print 'update'
    while not rospy.is_shutdown():
        
        task_alarm=timealert.check_alarm()
        if task_alarm is not None:
            print 'ALARM'
            print 'task_command=',task_alarm
            parse_command(task_alarm)
            
            
        publish_room_state()
        
        time.sleep(stepDelay)                   # Wait between steps

    
    
def shutdown():
    
    print "shutdown"
    blind.Cerrar_programa()
    radiator.Cerrar_programa()
    
if __name__ == "__main__":
    
    global room_config
    
        
    name_configfile=rospy.get_param('/config_file', '../conf/room_config.json')

    print 'name_configfile=',name_configfile
    room_config=load_json(name_configfile)

    rospy.init_node('domopin_room_'+str(room_config['roomid']))
    rospy.on_shutdown(shutdown)

    pub_msg_room_status=rospy.Publisher('domopin/room_status', RoomStatus, queue_size=1)
    
#    rospy.Service('domopin/set_action',ServAction,srv_callback_set_action)
    
    rospy.Subscriber("domopin/command", String, callback_command)
    rospy.Subscriber("domopin/central_status", BoilerStatus, callback_central_status)
        
    ## BLIND
    if len(room_config['device']['blind'])>0: 
        blind.Inicio(room_config)
        
        t_blind = threading.Thread(target=blind.Bucle_principal)
        t_blind.start()
        
    #RADIATOR
    if len(room_config['device']['radiator'])>0:     
        radiator.Inicio(room_config)
    
        t_radiator = threading.Thread(target=radiator.Bucle_principal)
        t_radiator.start() 
    
    # SCHEDULE
    timealert=time_alert.TimeAlarm(10, '../conf/schedule.json')
    timealert.start_worker()
    
    print "Started"
    
    update()
    
#    t_update = threading.Thread(target=update)
#    t_update.start()



    #rospy.spin()
    
    
    
