#!/usr/bin/env python

import rospy
import std_srvs.srv 
from std_msgs.msg import String
from domopin_msgs.msg import *
from domopin_msgs.srv import *


import time

import os


from array import *

import threading
import persiana_sim as persiana


IDROOM='room_1'
IDBLIND='blind_1'


pub_msg_room_status=rospy.Publisher('domopin/room_status', RoomStatus, queue_size=1)


def callback_command(msg):
    #action=Action()
    print 'Recibido command room=',msg.nameroom,' dev=',msg.namedev,' action=',msg.action
    if msg.nameroom ==IDROOM :
    
        print 'OK::',msg.action
        persiana.Recibir_comando_web(msg.namedev,msg.action)

def callback_set_action(req):
    print 'callback_set_action req=', req
    
    data = req.array_actions
    for i in range(len(data)):
        
        if data[i].nameroom ==IDROOM :
            persiana.Recibir_comando_web( data[i])
            
        
    return True
    
def publish_room_state(data):

    current_status=RoomStatus()
    current_status.idroom=IDROOM
    current_status.temp=data[6]	
    current_blind_status=BlindStatus()
    current_blind_status.id=IDBLIND
    current_blind_status.up=data[0]
    current_blind_status.down=data[1] 
    current_blind_status.position=data[2] 
    current_blind_status.push_up=data[3] 
    current_blind_status.push_down=data[4] 
    current_blind_status.error=data[5]
    current_status.array_blind.append(current_blind_status)     
    pub_msg_room_status.publish(current_status)
    #print "Published pub_msg_room_status"

def thread_blind():
    
    blind_1=persiana.Inicio()

def shutdown():
    print "shutdown"
    
if __name__ == "__main__":
    
    rospy.init_node('domopin_'+IDROOM)
    rospy.on_shutdown(shutdown)

    rospy.Service('domopin/set_action_'+IDROOM,ServAction,callback_set_action)
    
    rospy.Subscriber("domopin/command", Command, callback_command)


    t_blind = threading.Thread(target=thread_blind)
    t_blind.start()
    t_blind.join()

    print "Started"
    rospy.spin()
    
    
