#!/usr/bin/env python


from lxml import etree
from array import *

from calendar import timegm
from dateutil import parser
from dateutil import tz
from datetime import datetime
from datetime import timedelta

from threading import Thread



global target_time
global file_name_calendar
global list_tasks
global path_name 

priority = {'Predefinido': 2, 'Ruta': 3}

class Cal:

    def __init__(self,update_wait=60, file_name=None):
        self.tz_utc = tz.gettz('UTC')
        if file_name is not None:
            self.uri = file_name
        else:
            self.uri = file_name_calendar
        self.update_wait = update_wait

        self.update_worker = Thread(target=self.waiting_run)
        
    def start_worker(self):
        self.update_worker.start()
        
    def find_pending(self, type_event, num):
        #num = num of events returned , 0=all of them
        
        list_pending = []
        
        if len(list_tasks) > 0:
            for i in range(len(list_tasks)):
                
                if list_tasks[i].event == type_event:
                    
                    list_pending.append(list_tasks[i])
                    if num == len(list_pending):
                        continue
                    
        return list_pending      
            
    def waiting_run(self):
        
        global target_time
        # make sure we can be killed here
        while not rospy.is_shutdown():
            #if exist next event
            if target_time:
                while datetime.now() < target_time and not rospy.is_shutdown():
                    #print 'update'
                    next_task=self.find_pending(type_event_required,1)                    
                    publish_next_task(next_task)
                    rospy.sleep(5)
                
                #Start event
                #publish_task(list_tasks[0])
                action_pub_sec(list_tasks[0])
                aux_event=Event()
                aux_event=list_tasks.pop(0)
                #if is hour recurring  event
                print "aux_event.recur_hour" , aux_event.recur_hour
                if not aux_event.recur_hour ==0:
                    aux_event.start_time=aux_event.start_time + timedelta(minutes=aux_event.recur_hour)
                    if aux_event.start_time < aux_event.end_time:
                        if len(list_tasks) >0:
                            for i in range(len(list_tasks)):
                                
                                if aux_event.start_time < list_tasks[i].start_time :
                                    list_tasks.insert(i,aux_event)
                                    print "insert"
                                    break
                                elif aux_event.start_time == list_tasks[i].start_time:
                                    aux_event.start_time=aux_event.start_time + timedelta(minutes=1)
                                    #list_tasks.insert(i,aux_event)
                                    print "change"
                                    #continue
                                elif i == len(list_tasks)-1:
                                    list_tasks.append(aux_event)
                                    #print "append"
                        else:
                            list_tasks.append(aux_event)
                        
                if len(list_tasks) >0:
                    target_time = list_tasks[0].start_time
                else:
                    
                    target_time = None
                    
                print "LISTA"
                for i in range(len(list_tasks)):
                    print list_tasks[i].name,list_tasks[i].start_time
             
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
        doc = etree.parse(self.uri)
        #print etree.tostring(doc,pretty_print=True ,xml_declaration=True, encoding="utf-8")        
        events=doc.findall("event")
        
        global list_tasks 
        list_tasks = []
        
        for i in range(len(events)):
            new_event = Event()
            new_event.name=events[i].find("text_name").text
            new_event.id_task=events[i].find("id").text
            print new_event.name
            start_str=events[i].find("start_date").text
            new_event.start_time=datetime.strptime(start_str, '%Y-%m-%d %H:%M')
            print new_event.start_time
            end_str=events[i].find("end_date").text
            new_event.end_time=datetime.strptime(end_str, '%Y-%m-%d %H:%M')
            print new_event.end_time
            now = datetime.now()
            
            
            if events[i].find("event_pid").text: # Recurring event modified
                #print "event_pid" 
                pid=events[i].find("event_pid").text
                
                for i in range(len(list_tasks)):
                    print "PID" , i
                    if pid == list_tasks[i].id_task :
                        p=list_tasks.pop(i)
                        print "recurring removed"
                        for i in range(len(list_tasks)):
                            print list_tasks[i].name,list_tasks[i].event,list_tasks[i].start_time
                        break
                 
             
            
            if now > new_event.end_time: # Past event 
                continue
            today_t= now.replace(hour=23, minute=59, second=0, microsecond=0)
            if today_t < new_event.start_time: # After today event 
                continue
            
            if events[i].find("rec_type").text: # Recurring event
                rec_type_str=events[i].find("rec_type").text
                if self.recurring_day(rec_type_str): #Today event
                    #print 'recurring'
                    
                    length=int(events[i].find("event_length").text)                       
                    new_event.start_time=today_t.replace(hour=new_event.start_time.hour, minute=new_event.start_time.minute)
                    new_event.end_time=new_event.start_time + timedelta(seconds=length)
                    if now > new_event.end_time: # Past event 
                        continue
                                     
                else: #Not today
                    #print 'not recurring'
                    
                    continue
            

                        
            
            new_event.recur_hour=int(events[i].find("rec_hour").text)
            if new_event.recur_hour != 0: # Recurring event in same day
                
                while now > new_event.start_time:
                    new_event.start_time=new_event.start_time + timedelta(minutes=new_event.recur_hour)
                    #print "rec_hour" ,new_event.start_time
                
   
            #Today event
            
            #print start_t
            aux_e=()
            aux_e=events[i].find("ev").text
            aux_e=aux_e.split("#")
            new_event.requeriments=aux_e[0]
            new_event.type_task=aux_e[1]
            new_event.event=aux_e[2]
            
            if new_event.type_task=='Predefinido':
                aux_e.insert(3,new_event.event)
                new_event.event=new_event.type_task
            if len(aux_e)==3:
                aux_e.append("")
                
            new_event.args=[]    
            #arguments from aux_event[3]
            for i in range(len(aux_e)):
                if i >2:
                    new_event.args.append(aux_e[i])
            
            
            #Priority
            if priority.has_key(new_event.type_task):
                new_event.priority=priority[new_event.type_task]
                #print "priority=", new_event.priority   
                
            # Insert event in the list_task
                        

            if len(list_tasks) >0:
                for i in range(len(list_tasks)):
                    print i, new_event.start_time
                    if new_event.start_time < list_tasks[i].start_time :
                        list_tasks.insert(i,new_event)
                        print "insert"
                        print list_tasks[i].name,list_tasks[i].event,list_tasks[i].start_time
                        break
                    elif new_event.start_time == list_tasks[i].start_time:
                        if new_event.priority > list_tasks[i].priority:
                            list_tasks[i].start_time=new_event.start_time + timedelta(minutes=1)
                            aux_event2= Event()
                            aux_event2=list_tasks.pop(i)
                            list_tasks.insert(i,new_event)
                            new_event=aux_event2
                            print "change"
                            #continue
                    elif i == len(list_tasks)-1:
                        list_tasks.append(new_event)
                        print "append"
            else:
                list_tasks.append(new_event)
                print "append else"
                
            
            #a.insert(0, x) inserta al principio de la lista, y a.insert(len(a), x) equivale a a.append(x)
            #current_task=list_tasks.pop([0])
            
        global target_time
        if len(list_tasks) >0:
            target_time = list_tasks[0].start_time
        else:            
            target_time = None
                    
        print "LISTA EVENTOS"
        for i in range(len(list_tasks)):
            print list_tasks[i].name,list_tasks[i].event,list_tasks[i].start_time

  