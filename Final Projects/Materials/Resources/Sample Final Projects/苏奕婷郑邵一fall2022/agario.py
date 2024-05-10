
import pygame
from pygame.locals import *
import time
from random import randint, choice
import math as mt
import sys
import os


#display
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height), HWSURFACE | FULLSCREEN)
pygame.display.set_caption(("Agar.io"))


keret = pygame.image.load(os.path.join('img', 'keret.png'))
jobbNyil = pygame.image.load(os.path.join('img', 'jobb_nyil.png'))
balNyil = pygame.image.load(os.path.join('img', 'bal_nyil.png'))
keret.convert()
jobbNyil.convert()
balNyil.convert()

#változók
run = True # --> FONTOS!!!
menu = False
x = int(width/2)
y = int(height/2)
r = 20
xm = 100
ym = 100
rm = 20
speed = 5
food_timer = 20
color_switch = 2
color_list = (
     (255, 0, 0),
     (0, 255, 0),
     (0, 0, 255),
     (0, 51, 102),
     (51, 102, 153),
     (153, 102, 255)
     )

#USEREVENT
timer_event = pygame.USEREVENT +1
pygame.time.set_timer(timer_event, 1000)

#funkciók

def draw_lines():
     for vert in range(0, width, 20):
        for hor in range(0, height, 20):
            pygame.draw.line(screen, (202, 204, 206), (vert, 0), (vert, height))
            pygame.draw.line(screen, (202, 204, 206), (0, hor), (width, hor))

def food_dict():
    global food_list
    food_list = []

    for i in range (21600):
        innerlist = []
        for j in range (2):
            innerlist.append(randint(0, width))
        food_list.append(innerlist)

class circle:
     def __init__(self, color, x, y, r):
          self.color = color
          self.x = x
          self.y = y
          self.r = r
          pygame.draw.circle(screen, color, (x, y), r+2)
          pygame.draw.circle(screen, (255, 0, 0), (x, y), r)

def draw_food(food_list):
    for i in range(food_timer):
        x = food_list[i][0]
        y = food_list[i][1]
        list = [
                (x, y),
                (x+4, y),
                (x+6, y+2),
                (x+6, y+6),
                (x+4, y+8),
                (x, y+8),
                (x-2, y+6),
                (x-2, y+2),
                ]
        pygame.draw.polygon(screen, (0, 0, 255), list)

def eat_food(food_list):
     global r, rm
     for food in food_list[:food_timer]:
          if (food[0]-x)**2+(food[1]-y)**2 <= r**2:
               food_list.remove(food)
               r += 1
          if (food[0]-xm)**2+(food[1]-ym)**2 <= rm**2:
               food_list.remove(food)
               rm += 1

def eat_player():
     global r, rm, player1, player2
     if (x-xm)**2+(y-ym)**2 <= rm**2 and r < rm:
          rm += r
          del player1
          del r
     if (xm-x)**2+(ym-y)**2 <= r**2 and rm < r:
          r += rm
          rm = 0
          del player2


food_dict()

def draw_skins_choice():
     global xi, yi
     xi = width/2+140
     yi = height*0.45+140
     screen.blit(keret, (width/2-120, height*0.45))
     screen.blit(jobbNyil, (xi, yi))
     screen.blit(balNyil, (width/2-218, height*0.45+140))

#menu
while menu == True:

     for event in pygame.event.get():
          if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
               pygame.quit()
               sys.exit()
          #if event.type == pygame.MOUSEBUTTONDOWN:
               
                
     screen.fill((255, 255, 255))
     draw_lines()
     draw_skins_choice()
     circle(color_list[color_switch], x, y+140, 60)
     pygame.display.flip()

     
#main WHILE loop
while run == True:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            run == False
            
        if event.type == timer_event:
            food_timer += 2

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        y -= speed
    if key[pygame.K_DOWN]:
        y += speed
    if key[pygame.K_LEFT]:
        x -= speed
    if key[pygame.K_RIGHT]:
        x += speed
    if key[pygame.K_w]:
        ym -= speed
    if key[pygame.K_s]:
        ym += speed
    if key[pygame.K_a]:
        xm -= speed
    if key[pygame.K_d]:
        xm += speed

    screen.fill((255, 255, 255))
    draw_lines()
    draw_food(food_list)

    player1 = circle((0, 255, 0), x, y, r)
    player2 = circle((0, 0, 255), xm, ym, rm)

    del player1

    eat_food(food_list)
    eat_player()
    
    pygame.display.flip()

