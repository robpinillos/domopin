#!/usr/bin/env python

import rospy

from std_msgs.msg import String
from domopin_msgs.msg import *
from domopin_msgs.srv import *

import sys, pygame

from itertools import cycle
from pygame.locals import *
from constants import *
from menu import *



import time
import os
import numpy as np;
import json
from array import *
from datetime import *
from threading import Thread

## ---surfaces
global screen
global menudisplay
global tabledisplay

global room_status


IDROOM=2
OFF=0
ON=1
blink_surfaces = cycle([OFF, ON])


def callback_status(msg):
    #action=Action()
    global room_status
    #print 'Recibido command room=',msg.roomid

    if msg.roomid==IDROOM:
        room_status=msg
    
def publicar_comando(data):
    
    #"action": [{"roomid": 2,"device":"blind", "id": 1,"command":"position" , "value":1 }]
    if data=='setpoint170':
        
        #value=170
        value="1"
    elif data=='setpoint210':
        
        #value=210 
        value="position_
    #cmd={"action": [{"roomid": IDROOM,"device":"radiator", "id": 1,"command":"setpoint" , "value":value }]}
    cmd={"action": [{"roomid": 4,"device":"blind", "id": 1,"command":"setposition" , "value":value }]}    
    pub_command.publish(json.dumps(cmd))



def main_menu(): 
    
    global global_piece
    global pending_tasks
    global room_status



        
    buttons_surface=pygame.Surface((DISPLAY_BUTTONS['w'],DISPLAY_BUTTONS['h']))
    buttons_surface.fill(BLACK)
    list_menu = cMenu(DISPLAY_BUTTONS['x'], DISPLAY_BUTTONS['y'], DISPLAY_BUTTONS['w'], DISPLAY_BUTTONS['h'],40,20, 'horizontal',buttons_surface,None,
                       [('210', 80,50, GREEN, BRIGHT_GREEN,'setpoint210'),
                        ('170', 80,50, BLUE, BRIGHT_BLUE, 'setpoint170'),
                        ('Salir', 80,50,RED, BRIGHT_RED, 'exit')])
    
    
    screen.blit(buttons_surface,(DISPLAY_BUTTONS['x'], DISPLAY_BUTTONS['y'], DISPLAY_BUTTONS['w'], DISPLAY_BUTTONS['h'])) 

    info_surface=pygame.Surface((screen.get_width()-buttons_surface.get_width(),screen.get_height()))
    
        
    intro = True  
    while intro is True and not rospy.is_shutdown():
        info_surface.fill(BLACK)
        
        
        # PARSEAR VARIABLES
        try:
            Tint=float(room_status.array_rad[0].current_temp/10.0)
            Tsetpoint=float(room_status.array_rad[0].setpoint_temp/10.0)
            
            if room_status.array_rad[0].relay_opened is True:
                relay_status='ON'
                relay_color=GREEN
            elif room_status.array_rad[0].relay_opened is False:
                relay_status='OFF'
                relay_color=RED
                
            if room_status.array_rad[0].valve_opened is True:
                valve_status='ON'
                valve_color=GREEN
            elif room_status.array_rad[0].valve_opened is False:
                valve_status='OFF'
                valve_color=RED                    

            Twater=float(room_status.array_rad[0].water_temp/10.0)
        except:
                
            Tint='--.-'
            Tsetpoint='--.-'
            valve_status='--'
            relay_status='--'
            relay_color=valve_color=WHITE
            Twater='--.-'

            
            
            # INFO

            ## title

#        black_square_that_is_the_size_of_the_screen = pygame.Surface(screen.get_size())
#        black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
#        screen.blit(black_square_that_is_the_size_of_the_screen, (0, 0))


        centrex_c1=info_surface.get_width()/4
        centrex_c2=int(info_surface.get_width()/2+centrex_c1)
        
        ## T interior
        font = pygame.font.Font(None, 30)
        text = font.render("Interior", 1, BRIGHT_BLUE)
        textpos = text.get_rect(center=(centrex_c1-10,10))
        info_surface.blit(text, textpos)

        
        font = pygame.font.Font(None, 50)
        text = font.render(str(Tint), 1, WHITE)
        textpos = text.get_rect(center=(centrex_c1-10,40))
        info_surface.blit(text, textpos)
    
        font = pygame.font.Font(None, 20)
        textF = font.render(u'\u00b0' + "C", 1, WHITE)
        textposF = textpos[0] + textpos[2], textpos[1] + 10
        info_surface.blit(textF, textposF)
        

        ## Vertical Line

    
        pygame.draw.line(info_surface, GREEN, [info_surface.get_width()/2, 5], [info_surface.get_width()/2,80], 1) #vertical

        
        ## T exterior  
        font = pygame.font.Font(None, 30)
        text = font.render("Consigna", 1, BRIGHT_BLUE)
        textpos = text.get_rect(center=(centrex_c2-10,10))
        info_surface.blit(text, textpos)
    
        font = pygame.font.Font(None, 50)
        text = font.render(str(Tsetpoint), 1, WHITE)
        ##    text = font.render("188.8", 1, WHITE)
        textpos = text.get_rect(center=(centrex_c2-10,40))
        info_surface.blit(text, textpos)
    
        font = pygame.font.Font(None, 20)
        textF = font.render( u'\u00b0' +" C", 1, WHITE)
        textposF = textpos[0] + textpos[2], textpos[1] + 10    
        info_surface.blit(textF, textposF)

                

        ## Horizontal Line
        pygame.draw.line(info_surface, GREEN, [2, 80], [info_surface.get_width()-2,80], 1)
 


        ## Relay
        font = pygame.font.Font(None, 20)
        text = font.render("Rele", 1, BRIGHT_BLUE)
        textpos = text.get_rect(center=(30,90))
        info_surface.blit(text, textpos)

        
        font = pygame.font.Font(None, 30)
        text = font.render(str(relay_status), 1, relay_color)
        textpos = text.get_rect(center=(30,120))
        info_surface.blit(text, textpos)
    
        

        ## Vertical Line

    
        pygame.draw.line(info_surface, GREEN, [info_surface.get_width()/3, 80], [info_surface.get_width()/3,180], 1) #vertical

        
        ## Valve
        font = pygame.font.Font(None, 20)
        text = font.render("Valvula", 1, BRIGHT_BLUE)
        textpos = text.get_rect(center=(centrex_c1+50,90))
        info_surface.blit(text, textpos)

        
        font = pygame.font.Font(None, 30)
        text = font.render(str(valve_status), 1, valve_color)
        textpos = text.get_rect(center=(centrex_c1+50,120))
        info_surface.blit(text, textpos)
 
        ## Vertical Line

    
        pygame.draw.line(info_surface, GREEN, [info_surface.get_width()/1.5, 80], [info_surface.get_width()/1.5,180], 1) #vertical

        
        ## T water 
        font = pygame.font.Font(None, 20)
        text = font.render("T agua", 1, BRIGHT_BLUE)
        textpos = text.get_rect(center=(centrex_c2+20,90))
        info_surface.blit(text, textpos)

        
        font = pygame.font.Font(None, 30)
        text = font.render(str(Twater), 1, WHITE)
        textpos = text.get_rect(center=(centrex_c2+20,120))
        info_surface.blit(text, textpos)
        
        
        
        ## Hora
        currentime = datetime.now().strftime('%H:%M:%S') 
        font = pygame.font.Font(None, 25)
        text = font.render(currentime, 1, BLUE)
        textpos = text.get_rect(center=(info_surface.get_width()/2,215))
        info_surface.blit(text, textpos)

      
        screen.blit(info_surface,(DISPLAY_BUTTONS['w'], 0)) 
        # FIN INFO
            
        # SI HAY PULSACION EN MENU

        for event in pygame.event.get():
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    action=list_menu.update(event)
                    #SELECTION                                           
                    if action=='setpoint210':
                        
                        publicar_comando('setpoint210')
                        #menu_tasks()   
                        #intro = False
                    elif action=='setpoint170':
                        #configure()
                        publicar_comando('setpoint170')
                        #intro = False
                    elif action=='exit':
                        quitpygame()

                                           
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # FIN MENU
        
        pygame.display.update()
        clock.tick(15)

    quitpygame()
    print 'Shutdown'   
    
    

    

    
def configure (): 
    pass

    
def quitpygame():
    pygame.quit()
    
    quit()

def shutdown():
    
    print "shutdown"
    quitpygame()
    
if __name__ == "__main__":
    


    rospy.init_node('interface_room_'+str(IDROOM))
    rospy.on_shutdown(shutdown)

    
    rospy.Subscriber("domopin/room_status", RoomStatus, callback_status)
    pub_command=rospy.Publisher("domopin/command", String, queue_size=1)
    

    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    #screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    
    # Set the window caption
    pygame.display.set_caption("INTERFACE")

    
    pygame.init()

    clock = pygame.time.Clock()

    thread_update = Thread(target=main_menu)
    thread_update.start() 
    print "Started"
    #rospy.spin()
    

