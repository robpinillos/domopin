#!/usr/bin/env python
from array import *

import rospy
from calendar import timegm
from dateutil import parser
from dateutil import tz
from datetime import datetime
from datetime import timedelta

from threading import Thread
import json
import time



class TimeAlarm:

    def __init__(self,update_delay=30, file_name='../conf/schedule.json'):
        self.tz_utc = tz.gettz('UTC')

        self.path_file = file_name

        self.update_delay = update_delay

        self.update_worker = Thread(target=self.waiting_run)
        
        self.list_tasks=[]
        
        self.target_time=None
        
        self.next_task=None
        
        self.b_alarm=False
        
        self.update_cal()
        
        print 'Time_alarm started'
        
    def start_worker(self):
        self.update_worker.start()
        
    def find_pending(self, type_event, num):
        #num = num of events returned , 0=all of them
        
#        list_pending = []
#        
#        if len(list_tasks) > 0:
#            for i in range(len(list_tasks)):
#                
#                if list_tasks[i].event == type_event:
#                    
#                    list_pending.append(list_tasks[i])
#                    if num == len(list_pending):
#                        continue
#                    
#        return list_pending      
        return 1
            
            
    def waiting_run(self):
        

        # make sure we can be killed here
        while not rospy.is_shutdown():

            #if exist next event
            if self.target_time:
                
                strtimenow=datetime.now().strftime('%H:%M') 
                temptimenow=strtimenow.replace(':','')
                timenow=int(temptimenow)
                
                if timenow < self.target_time :
                    
                    print 'timenow=',timenow
                    print 'self.target_time=',self.target_time
#                    next_task=self.find_pending(type_event_required,1)                    
#                    publish_next_task(next_task)
                    
                elif timenow ==self.target_time :
                    self.b_alarm=True
                
                
                
            rospy.sleep(self.update_delay)
                
                #Start event
                #publish_task(list_tasks[0])
                

    def check_alarm(self):
        
        if self.b_alarm is True:
            
            print 'check::self.list_tasks=',self.list_tasks
                 
            aux_event=self.list_tasks.pop(0)
            self.update_next_task()
            
            self.b_alarm=False
            return self.next_task
            
        else:
            
            return None
        
                    
        
             
    def run(self):
        print 'run'
        
        
    def recurring_day(self,rec_type_str):

        rec_type_str=rec_type_str.split('#')
        rec_type=rec_type_str[0].split('_')
        
        ok_today=False
        if rec_type[0]=='day':
            ok_today=True
        elif rec_type[0]=='week':
            
            today_d=datetime.today().weekday()
            day_n=rec_type[4].split(',')
            
            for i in range(len(day_n)):
                
                if day_n[i]==str(today_d):
                    ok_today=True
                    
                    
        elif rec_type[0]=='month':
            print 'month'
        return ok_today
        
    def update_cal(self):
        
        with open(self.path_file, 'r') as f:
            data = json.load(f)

        events=data['task']
    
        strtimenow=datetime.now().strftime('%H:%M') 
        temptimenow=strtimenow.replace(':','')
        timenow=int(temptimenow)
                
        
        
        for ievent in events:
            
            if timenow <= ievent['timealert']:
            
                if len(self.list_tasks) ==0:

                    self.list_tasks.append(ievent)
                    print "append first task"
                    
    
                else :
                    
                    for i in range(len(self.list_tasks)):
                        print i, ievent['timealert']
                        if ievent['timealert']< self.list_tasks[i]['timealert'] :
                            self.list_tasks.insert(i,ievent)
                            print "insert"
                            
                        else:
                            
                            self.list_tasks.append(ievent)
                            print "append"
                    
            
            #a.insert(0, x) inserta al principio de la lista, y a.insert(len(a), x) equivale a a.append(x)
            #current_task=list_tasks.pop([0])
            
        self.update_next_task()
            
    def update_next_task(self):
        
        if len(self.list_tasks) >0:
            self.target_time = self.list_tasks[0]['timealert']
            self.next_task =self.list_tasks[0]
        else:            
            self.target_time = None
            self.next_task =None
                    
        print "LISTA EVENTOS"

        print self.list_tasks

#if __name__ == '__main__':
#    
#    timealert=TimeAlarm(5, '../conf/schedule.json')
#    
#    timealert.start_worker()
#    
#    while not rospy.is_shutdown():
#    
#
#        ret=timealert.check_alarm()
#        if ret is not None:
#            print 'ret=',ret
#        
#        time.sleep(0.3)                   # Wait between steps
#


  