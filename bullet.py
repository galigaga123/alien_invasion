#-*- codding = utf-8 -*-
#author = huang
import pygame
from  pygame.sprite import Sprite#引入一个精灵组

class Bullter(Sprite):
    #对于飞船子弹管理的类
    def __init__(self,ai_settings,screen,ship):
        #飞船所在位置创建一个子弹对象
        super().__init__()
        self.screen = screen

        #0,0处创建一个表示子弹的矩形，再设置正确位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        #向上移动的子弹
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        #绘制子弹
        pygame.draw.rect(self.screen,self.color,self.rect)


