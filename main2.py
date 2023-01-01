import pygame
from pygame.locals import *
import pymunk
from pymunk import pygame_util
import sys
import random as rd
import time
import math

CREATE_FIREBALL=USEREVENT+1

class Firework:
    def __init__(self):
        pygame.init()
        self.W,self.H=800,1000
        self.screen=pygame.display.set_mode((self.W,self.H))
        self.draw_options=pygame_util.DrawOptions(self.screen)
        pygame.display.set_caption("2023元旦烟花")
        self.space=pymunk.Space()
        self.space.gravity=(0,300)
        self.space.collision_persistence=0
        self.fireball_radius=2
        self.fire_radius=2
        self.fireballs=[]
        self.colors=[
            (255,0,0),(255,127,80),(255,140,0),(255,160,122),(240,128,128),(255,99,71),(255,69,0),
            (255,105,180),(255,20,147),(208,32,144),(176,48,96),(153,50,204),(255,48,48),
            (238,44,44),(205,38,38),(255,255,0),(255,215,0),(255,185,15),(238,201,0),
            (34,139,34),(46,139,87),(60,179,113),(0,255,127)
        ]
        self.fires=[]

    def listen(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit()
            if event.type==CREATE_FIREBALL:
                self.create_firework(x=rd.randint(0,self.W))

    def create_firework(self,x):
        fireball_body=pymunk.Body(mass=1,moment=100,body_type=pymunk.Body.DYNAMIC)
        fireball_body.position=x,self.H
        fireball_shape=pymunk.Circle(fireball_body,self.fireball_radius)
        fireball_shape.elasticity=0.5
        self.space.add(fireball_body,fireball_shape)
        self.fireballs.append([fireball_shape,rd.choice(self.colors),time.time(),rd.uniform(1,2.2)]) # shape,color,startTime,lastTime
        fireball_body.apply_impulse_at_local_point((0,rd.randint(-730,-500)),(0,0))

    def draw(self):
        self.screen.fill((0,0,0))
        i=0
        while i<len(self.fireballs):
            fireball,color,startTime,lastTime=self.fireballs[i]
            pygame.draw.circle(self.screen,color,fireball.body.position,self.fireball_radius)
            nowTime=time.time()
            boomTime=startTime+lastTime
            if nowTime>boomTime:
                popball=self.fireballs.pop(i)
                length=50
                for degree in range(90,450,10):
                    bias=1
                    length+=rd.randint(-bias,bias)
                    maximum,minimum=100,25
                    if length>maximum:
                        length=maximum
                    elif length<minimum:
                        length=minimum
                    radians=math.radians(degree)
                    x_force=math.sin(radians)*length
                    y_force=math.cos(radians)*length
                    body=pymunk.Body(mass=1,moment=100,body_type=pymunk.Body.DYNAMIC)
                    body.position=popball[0].body.position
                    shape=pymunk.Circle(body,self.fire_radius)
                    self.space.add(body,shape)
                    self.fires.append([shape,popball[1],time.time(),rd.uniform(0.5,1.5)]) # shape,color,startTime,lastTime
                    body.apply_impulse_at_local_point((x_force,y_force),(0,0))
                self.space.remove(popball[0])
                i-=1
            i+=1
        i=0
        while i<len(self.fires):
            fire,color,startTime,lastTime=self.fires[i]
            pos=fire.body.position
            pygame.draw.circle(self.screen,color,pos,self.fire_radius)
            nowTime=time.time()
            deleteTime=startTime+lastTime
            if nowTime>deleteTime:
                self.fires.pop(i)
                self.space.remove(fire)
                i-=1
            elif pos[0]<0 or pos[0]>self.W or pos[1]>self.H:
                self.fires.pop(i)
                self.space.remove(fire)
                i-=1
            i+=1

    def run(self):
        clock=pygame.time.Clock()
        FPS=60
        pygame.time.set_timer(CREATE_FIREBALL,120)
        while True:
            clock.tick(FPS)
            self.listen()
            self.draw()
            self.space.step(1/FPS)
            pygame.display.update()


if __name__=="__main__":
    firework=Firework()
    firework.run()