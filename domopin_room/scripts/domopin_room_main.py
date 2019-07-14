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
#import radiador_sim as radiator
import relay_sim as relay

#import persiana as blind
import termostato as radiator

import time_alert 


global room_config
global current_radiator_schedule
global current_blind_schedule
global current_relay_schedule


stepDelay = 0.5                    # Number of seconds between each sequence step


def load_json(path):
    print "load " ,path   
    # Reading data
    with open(path, 'r') as f:
        data = json.load(f)

    return data
    

def callback_service(req):
    
    
    jreq = json.loads(req.json_req)
    
    if jreq['type']=='save_schedule':
        
        timealert.save_schedule(jreq['value'])
        print 'saved'
        schedule=timealert.schedule
        list_tasks=timealert.list_tasks
        
        print 'list_tasks'
                    
        ret={"current_schedule": schedule, "list_tasks":list_tasks}
        
        return json.dumps(ret)
    
    
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

    current_status=RoomStatus()
    current_status.roomid=room_config['roomid']
    current_status.connected_central= True
    
    
    #print 'room_config=',room_config
    try:
        datablind=blind.Publicar_estado_actual_persiana()
    except:
        datablind=[0,0,0,0,0,0,0]

    current_blind_status=BlindStatus()
    current_blind_status.id=1
    current_blind_status.auto_mode=True
    current_blind_status.up=bool(datablind[0])
    current_blind_status.down=bool(datablind[1] )
    current_blind_status.position_value=int(datablind[2])
    current_blind_status.position_name=status_blind_position(current_blind_status.position_value)
    current_blind_status.push_up=bool(datablind[3]) 
    current_blind_status.push_down=bool(datablind[4]) 
    current_blind_status.error=int(datablind[5])
    
    current_blind_status.current_schedule=current_blind_schedule
    
    current_status.array_blind.append(current_blind_status)
    
    try:
        dataradiator,datawindow=radiator.Publicar_estado_actual()
    except:
        dataradiator=[0,0,0,0,0,0,0,0]
        datawindow=[0,0]
        
    current_radiator_status=RadiatorStatus()
    current_radiator_status.id=1
    current_radiator_status.auto_mode=bool(dataradiator[6])
    current_radiator_status.relay_closed=bool(dataradiator[3])
    current_radiator_status.valve_opened=bool(dataradiator[4])
    current_radiator_status.boiler_on=bool(dataradiator[7])
    current_radiator_status.current_temp=int(dataradiator[0])
    current_radiator_status.setpoint_temp=int(dataradiator[2])
    current_radiator_status.water_temp=int(dataradiator[1])
    current_radiator_status.error=int(dataradiator[5])
    
    current_radiator_status.current_schedule=current_radiator_schedule
    
    current_status.array_rad.append(current_radiator_status)
    
    
    current_window_status=WindowStatus()
    current_window_status.id=1
    current_window_status.outside_temp=int(0)
    current_window_status.humidity=int(0)
    current_window_status.window_closed=bool(datawindow[0])
    current_window_status.door_closed=bool(datawindow[1])
    current_window_status.error=0
    
    
    
    current_status.array_window.append(current_window_status)

    try:
        datarelay=relay.Publicar_estado_actual()
    except:
        datarelay=[0,0]
        
    current_relay_status=RelayStatus()
    current_relay_status.id=1
    current_relay_status.auto_mode=bool(datarelay[0])
    current_relay_status.relay_closed=bool(datarelay[1])
    current_relay_status.error=datarelay[2]
    
    current_relay_status.current_schedule=current_relay_schedule
    
    current_status.array_rel.append(current_relay_status)
   
    pub_msg_room_status.publish(current_status)
    
    blind.Actualizar_estado_habitacion(current_status)
    #radiator.Actualizar_estado_habitacion(current_status)
        
#    print "Published pub_msg_room_status"




def parse_command(data):
    
    global current_radiator_schedule
    global current_blind_schedule
    global current_relay_schedule

    #{"type":"action","action": [{"roomid": room_config['roomid'],"device":"blind", "id": 1,"command":"position" , "value":value }]}  
    #{"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  

    if data['type']=="action":
        
        for iaction in data['action']:
            
            if iaction['roomid']==room_config['roomid']:
                
                print 'PARSE COMMAND  iaction=',iaction
                 
                
     
                if  iaction['device']=='blind':
                    
                    if iaction['command']=='setposition':
                
                        
                        current_blind_schedule.type="schedule"
                        current_blind_schedule.value=int(iaction['value'])
                        current_blind_schedule.end_time=0
                        
                        blind.Actualizar_valores(iaction['command'],iaction['value'])
                    
                    elif iaction['command']=='position_adj_temp':
                
                        
                        timealert.adj_temp('blind','setposition',current_blind_schedule.value,iaction['value']['end_time']) #timealert.adj_temp(device,command,current_setpoint,adj_end_time)
                        
                        
                        current_blind_schedule.type="temporary"
                        current_blind_schedule.value=int(iaction['value']['value'])
                        current_blind_schedule.end_time=iaction['value']['end_time']
                        
                        blind.Actualizar_valores('setposition',current_blind_schedule.value)
                        
                        publish_room_state()
                        
                        time.sleep(0.2)
                        value=timealert.list_tasks
                        cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  
                  
                        pub_command.publish(json.dumps(cmd))


                    elif iaction['command']=='cancel_position_adj_temp':
                        
                        timealert.update_cal()
    
                        current_blind_schedule.type="default"
                        #current_radiator_schedule.value=data['value']['value']
                        #current_radiator_schedule.end_time=data['value']['end_time']


                        publish_room_state()

                        time.sleep(0.2)
                        value=timealert.list_tasks
                        cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}


                        pub_command.publish(json.dumps(cmd))
					
                    else:
                                         
                        
                        blind.Actualizar_valores(iaction['command'],iaction['value'])
    
    
                elif  iaction['device']=='radiator':
                    
                    if iaction['command']=='setpoint':
                
                        
                        current_radiator_schedule.type="schedule"
                        current_radiator_schedule.value=iaction['value']
                        current_radiator_schedule.end_time=0
                        
                        radiator.Actualizar_valores(iaction['command'],iaction['value'])
                    
                    elif iaction['command']=='radiator_adj_temp':
                
                        
                        timealert.adj_temp('radiator','setpoint',current_radiator_schedule.value,iaction['value']['end_time']) #timealert.adj_temp(device,command,current_setpoint,adj_end_time)
                        
                        current_radiator_schedule.type="temporary"
                        current_radiator_schedule.value=int(iaction['value']['value'])
                        current_radiator_schedule.end_time=iaction['value']['end_time']
                        
                        radiator.Actualizar_valores('setpoint',current_radiator_schedule.value)
                        
                        publish_room_state()
                        
                        time.sleep(0.2)
                        value=timealert.list_tasks
                        cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  
                  
                        pub_command.publish(json.dumps(cmd))


                    elif iaction['command']=='cancel_radiator_adj_temp':
                        
                        timealert.update_cal()
    
                        current_radiator_schedule.type="default"
                        #current_radiator_schedule.value=data['value']['value']
                        #current_radiator_schedule.end_time=data['value']['end_time']


                        publish_room_state()

                        time.sleep(0.2)
                        value=timealert.list_tasks
                        cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}


                        pub_command.publish(json.dumps(cmd))
					
                    else:
                        radiator.Actualizar_valores(iaction['command'],iaction['value'])

                elif  iaction['device']=='relay':

                    relay.Actualizar_valores(iaction['command'],iaction['value'])	

    elif data['type']=='config': 
        
        if data['roomid']==room_config['roomid']:
            
   
            if data['action']=='refresh_schedule':
                    
                timealert.update_cal()
                
                value=timealert.schedule
                
                cmd={"type":"config","roomid": room_config['roomid'],"action":"current_schedule","value": value}
                
                
                pub_command.publish(json.dumps(cmd))
                
                time.sleep(0.2) 

                value=timealert.list_tasks
                cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  
          
                pub_command.publish(json.dumps(cmd))
        
            elif data['action']=='get_schedule':
                    
                value=timealert.schedule
                
                cmd={"type":"config","roomid": room_config['roomid'],"action":"current_schedule","value": value}
                
                time.sleep(0.2) 
                pub_command.publish(json.dumps(cmd))
        
                
            elif data['action']=='get_next_tasks':
                    
                value=timealert.list_tasks
                time.sleep(0.2) 
                cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  
                  
                pub_command.publish(json.dumps(cmd))

def status_blind_position(value):
    
    min_val=100000
    min_name=-1
    
    for pos in room_config['device']['blind'][0]['positions']:
        
        
        
        if abs( int(pos['value'][0]) -value) < min_val:
            min_val=abs(int(pos['value'][0]) -value)
            min_name=pos['name']
            
        if abs(int(pos['value'][1]) -value) < min_val:
            
            min_val=abs(int(pos['value'][1]) -value)
            min_name=pos['name']
            
    return int(min_name)
        
   
def get_next_tasks(device):
    
    
    next_tasks=[]
    
    for task in timealert.list_tasks:
        
        print 'task=',task
        if  task['action'][0]["device"]==device:
            next_tasks.append(task)
    return next_tasks
    
def update():
    
#    print 'update'
    while not rospy.is_shutdown():
        
        task_alarm=timealert.check_alarm()
        if task_alarm is not None:
            print 'ALARM'
            print 'task_command=',task_alarm
            parse_command(task_alarm)
            
            
            publish_room_state()
            
            value=timealert.list_tasks
            time.sleep(0.2) 
            cmd={"type":"config","roomid": room_config['roomid'],"action":"set_next_tasks","value": value}  
                  
            pub_command.publish(json.dumps(cmd))
            
        

        publish_room_state()
        
        time.sleep(stepDelay)                   # Wait between steps

    
    
def shutdown():
    
    print "shutdown"
    blind.Cerrar_programa()
    radiator.Cerrar_programa()
    
if __name__ == "__main__":
    
    global room_config
    global current_radiator_schedule
    global current_blind_schedule
    global current_relay_schedule
        
    name_configfile=rospy.get_param('/config_file', '../conf/room_config.json')

    print 'name_configfile=',name_configfile
    room_config=load_json(name_configfile)

    rospy.init_node('domopin_room_'+str(room_config['roomid']))
    rospy.on_shutdown(shutdown)

    pub_msg_room_status=rospy.Publisher('domopin/room_status', RoomStatus, queue_size=1)
    pub_command=rospy.Publisher("domopin/command", String, queue_size=1)
    
#    rospy.Service('domopin/set_action',ServAction,srv_callback_set_action)
    
    rospy.Subscriber("domopin/command", String, callback_command)
    rospy.Subscriber("domopin/central_status", BoilerStatus, callback_central_status)
    
    srv_command = rospy.Service('domopin/srv_command_'+str(room_config['roomid']),ServCommand,callback_service)
        
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
        


    #EXTRA RELAY
    if len(room_config['device']['relay'])>0:     
        relay.Inicio(room_config)
  
        t_relay = threading.Thread(target=relay.Bucle_principal)
        t_relay.start()
        

        
    else:     
        pass        

    current_radiator_schedule=CurrentSchedule()
    current_radiator_schedule.type="default"
    current_radiator_schedule.value=100
    current_blind_schedule=CurrentSchedule()
    current_blind_schedule.type="default"
    current_relay_schedule=CurrentSchedule()
    current_relay_schedule.type="default"
          
    # SCHEDULE
    timealert=time_alert.TimeAlarm(10, '../conf/schedule.json',room_config['roomid'])
    timealert.start_worker()
    
    print "Started"
    
    update()
    
#    t_update = threading.Thread(target=update)
#    t_update.start()



    #rospy.spin()
    
    
    
