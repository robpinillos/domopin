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

import riego_sim as riego


import time_alert 


global config


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
    
    
def publish_riego_state():


    
    try:
        datariego_dev=riego_dev.Publicar_estado_actual()
    except:
        datariego_dev=[0,0,0,0,0,0,0]
    current_status=RiegoStatus()
    current_status.roomid=room_config['roomid']
   
   
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
    riego_dev.Cerrar_programa()
    
if __name__ == "__main__":
    
    global config
    
        
    name_configfile=rospy.get_param('/config_file', '../conf/room_config.json')

    print 'name_configfile=',name_configfile
    config=load_json(name_configfile)

    rospy.init_node('domopin_riego')
    rospy.on_shutdown(shutdown)

    pub_msg_riego_status=rospy.Publisher('domopin/riego_status', RiegoStatus, queue_size=1)
    
#    rospy.Service('domopin/set_action',ServAction,srv_callback_set_action)
    
    rospy.Subscriber("domopin/command", String, callback_command)
    rospy.Subscriber("domopin/central_status", BoilerStatus, callback_central_status)
        

        

    riego_dev.Inicio(config)
    
    t_riego= threading.Thread(target=riego_dev.Bucle_principal)
    t_riego.start() 
    
    # SCHEDULE
    timealert=time_alert.TimeAlarm(10, '../conf/schedule.json')
    timealert.start_worker()
    
    print "Started"
    
    update()
    

    
    
