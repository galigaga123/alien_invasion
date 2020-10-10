#-*- codding = utf-8 -*-
#author = huang
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    #表示单个外星人
    def __init__(self,ai_settings,screen):
        #初始化外星人位置
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #加载外星人图像
        self.image = pygame.image.load(r'E:\python学习工程\alien_invasion\image\alien.bmp')
        self.rect = self.image.get_rect()
        #每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #存储外星人的准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        #如果位于屏幕边缘就返回true
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        # 外星人群的移动
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        #在指定位置绘制外星人
        self.screen.blit(self.image,self.rect)




