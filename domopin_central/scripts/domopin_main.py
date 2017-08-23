#!/usr/bin/env python

import rospy

from std_msgs.msg import String
from domopin_msgs.msg import *
from domopin_msgs.srv import *


import time

import os

import numpy as np;

import yaml

import json
import json_utils


from array import *

from collections import namedtuple
from dateutil import parser
from dateutil import tz
from datetime import datetime
from datetime import timedelta

import threading




global global_schedule



def callback_refresh_schedule(req):
    global global_schedule
    #blind_schedule=[]  
    #global_schedule=json_utils.load("./conf/schedule.json")
    json_utils.write_schedule_json('save',global_schedule)
    msg='Actualizado'
    
    return True
                    
                    
def callback_action(req):
    print req
    data = req.array_actions
    for i in range(len(data)):
        
        publish_action(data[i])
    
def publish_action(act):
    
    
    array_act=[]
    array_act.append(act)
    
    action_call=rospy.ServiceProxy('domopin/set_action_'+act.nameroom,ServAction)
    resp= action_call(array_act)
    

    if resp.ret:
        print 'OK'





def shutdown():
    print "shutdown"

    
if __name__ == "__main__":
    
    rospy.init_node('domopin_main')
    rospy.on_shutdown(shutdown)


    rospy.Service('domopin/refresh_schedule',ServEmpty,callback_refresh_schedule)
    rospy.Subscriber("domopin/array_action", ArrayAction, callback_action)  
    
 
    global global_schedule

#    global_schedule=json_utils.read_schedule_json("blind")
    global_schedule=json_utils.load("../conf/schedule.json")

    print "Started"
    rospy.spin()
    
    
