#-*- codding = utf-8 -*-
#author = huang
import sys
import pygame
from setting import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    #创建一个用于存储游戏统计的存储信息实例，并创建积分牌
    stats = GameStats(ai_setting)
    sb = Scoreboard(screen,ai_setting,stats)
    #设置背景颜色
    bg_color = (ai_setting.bg_color)
    #创建一艘飞船
    ship = Ship(ai_setting,screen)
    bullets = Group()
    #创建外星人组
    aliens = Group()
    gf.create_fleet(ai_setting,screen,ship,aliens)
    #创建play按钮
    play_button = Button(ai_setting,screen,"Play")

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_setting,screen,ship,bullets,stats,play_button,aliens,sb)
        #先判断飞船有无生命值
        if stats.game_active:
            #飞船左右移动量
            ship.update()
            #子弹移动
            bullets.update()
            #删除消失的子弹
            gf.update_bullets(ai_setting,screen,ship,aliens,bullets,sb,stats)
            # 更新外星人的位置
            gf.update_aliens(ai_setting,screen,stats,aliens,ship,bullets)
        #绘制屏幕的显示
        gf.update_screen(ai_setting,screen,ship,aliens,bullets,play_button,stats,sb)

run_game()
