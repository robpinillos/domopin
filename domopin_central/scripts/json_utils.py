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

from array import *


class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)



class Tree(object):
    def __init__(self, name, childTrees=None):
        if childTrees is None:
            childTrees = []
        self.task = childTrees

class TreeTask(object):
    def __init__(self, idtask, title, condition, action, enable):
        self.id = idtask
        self.title = title
        if condition is None:
            condition = []
        self.condition = condition
        if action is None:
            action = []
        self.action = action
        self.enable = enable

        
class TreeAction(object):
    def __init__(self, nameroom, namedev, nameaction , enable):
        self.nameroom = nameroom
        self.namedev = namedev
        self.nameaction = nameaction
        self.enable = enable
        
class TreeCondition(object):
    def __init__(self, typecondition, name, value):
        self.type = typecondition
        self.name = name
        self.value = value
        


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if isinstance(obj, Tree):
            return obj.__dict__ 
        elif isinstance(obj, TreeTask):
            return obj.__dict__ 
        elif isinstance(obj, TreeAction):
            return obj.__dict__
        elif isinstance(obj, TreeCondition):
            return obj.__dict__ 
        else:
            return super(MyEncoder, self).default(obj)
            


    
def load(path):
    print "load " ,path   
    # Reading data
    with open(path, 'r') as f:
        data = json.load(f)

    return data



def write(path,data):
    

    jsonData=json.dumps(data)

    fh = open(path,"w")
    fh.write(jsonData)
    fh.close()
        
            

def write_schedule_json(name_func,data_schedule):
    

    encode_data = Tree("task",data_schedule["task"])
    
    jsonData=json.dumps(encode_data, cls=MyEncoder,indent=2 )

    print 'jsonData=',jsonData
    fh = open('../conf/out_schedule.json',"w")
    fh.write(jsonData)
    fh.close()



  
