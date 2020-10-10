#-*- codding = utf-8 -*-
#author = huang
class Settings():
    #存储游戏所有的设置
    def __init__(self):
        #初始化游戏的静态设置
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,200,255)
        #飞船设置
        self.ship_limit = 0
        #子弹设置
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        #外星人设置
        self.fleet_drop_speed = 5
        #随着等级提升游戏速度和得分提升
        self.speedup_scale = 2
        self.socre_scale = 1.5
        #动态调用
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #随游戏变化的动态设置
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed_factor = 1
        #fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
        #计分
        self.alien_points = 50

    def increase_speed(self):
        #提高速度设置
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        #提高得分设置
        self.alien_points = int(self.alien_points*self.socre_scale)