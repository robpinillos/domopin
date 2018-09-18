#! /usr/bin/python

#-------------------------------------------------------------------------------
#---[ Imports ]-----------------------------------------------------------------
#-------------------------------------------------------------------------------
import pygame
from constants import *
import json
#############
#button_sound = pygame.mixer.Sound('./sounds/crash.wav')



#-------------------------------------------------------------------------------
#---[ cMenu Class ]-------------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used to display and control a menu
#
class cMenu:
    
    def __init__(self, x, y,w,h, h_pad, v_pad, orientation, background, color_background, buttonList):
        self.menu_items = []                      # List of menu items
        self.font = pygame.font.Font(None, 32)    # Font to use
        self.x = x                                # Top left corner (of surface)
        self.y = y                                # relative to the screen/window
        self.w = w                                # 
        self.h = h                                # 
        self.orientation = orientation            # See description above
        self.horizontal_padding = h_pad           # See description above
        self.vertical_padding = v_pad             # See description above

        self.color = BLACK                      # Color for unselected text
        self.p_color = RED                        # Color for selected text

        self.background = background     # The unedited background image
        self.color_background = color_background            # Surface to draw to
        self.centered = False                     # True if the menu is centered
        self.centeredOnScreen = True             # True if the menu is centered
        self.offset= (0,0)

        # This dictionary contains the alignment orientation of the buttons
        # related to each other.  It shifts the button within the bounds of
        # 'max_width' and 'max_height' in the self.position_buttons() method.
        self.alignment = {'vertical'  :'top','horizontal':'left'}

        # Now add any buttons that were sent in
        self.add_buttons(buttonList)

    ## ---[ __init__ ]-----------------------------------------------------------
    def add_buttons(self, buttonList):
        init_x=0
        init_y=0
        
        bFirst=True
        
        if self.color_background!= None:
            #pygame.draw.rect(self.background, self.color_background,(self.x, self.y,self.w,self.h))
            self.background.fill(self.color_background)
        for button in buttonList:
            
            if bFirst:
                self.menu_items.append(self.create_button(button,init_x,init_y))
                
                init_x=0
                init_y=0
                bFirst=False
            else:
                if self.orientation == 'horizontal':
                    init_x=init_x+button[1]
                    if init_x +button[1]> self.w:
                        init_x=0
                        init_y=init_y+button[2]+self.vertical_padding
                    else :
                        init_x=init_x+self.horizontal_padding
                         
                elif self.orientation == 'vertical':
                    init_y=init_y+button[2]
                    if init_y +button[2]> self.h:
                        init_y=0
                        init_x=init_x+button[1]+self.horizontal_padding
                    else :
                        init_y=init_y+self.vertical_padding
                        
    
                self.menu_items.append(self.create_button(button,init_x,init_y))

        #return self.menu_items




    def create_button(self, button_info, x,y):
        
        button_rect = pygame.Rect((x, y), (button_info[1], button_info[2]))
        new_button = {'text'    : button_info[0],
                    'rect'    : button_rect,
                    'action': button_info[5]                    
                    }

        pygame.draw.rect(self.background, button_info[3],new_button['rect'])            
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurface = smallText.render(new_button['text'], True, WHITE)
        textRect=textSurface.get_rect()
        textRect.center = ( (button_rect[0]+(button_rect[2]/2)), (button_rect[1]+(button_rect[3]/2)) )
        self.background.blit(textSurface, textRect)
             
        return new_button
        
    def update(self, event):       
        act=None
        x_selected=event.pos[0]-self.x
        y_selected=event.pos[1]-self.y
        for button in self.menu_items:
            
            if button['rect'].collidepoint(x_selected,y_selected):
                ####################################
#                pygame.mixer.Sound.play(button_sound)
#                pygame.mixer.music.stop()
                ####################################
                #if button['rect'][0]+button['rect'][2] > event.pos[0] > button['rect'][0] and button['rect'][1]+button['rect'][3] > event.pos[0] > button['rect'][1]:
                act= button['action']

        return act
#---[ END OF FILE ]-------------------------------------------------------------
