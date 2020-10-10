#-*- codding = utf-8 -*-
#author = huang
import sys
import pygame
from bullet import Bullter
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    #向下按键的事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)


def check_keyup_events(event,ship):
    #向上按键的事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
    #监视键和鼠的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() #退出
        elif event.type == pygame.KEYDOWN: #左右移控制
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb):
    #玩家单击play按钮时开始游戏
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #游戏运行的时候隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏信息
        stats.reset_stats()
        #开始游戏标志
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        #清空外星人和子弹
        aliens.empty()
        bullets.empty()
        #创建新的外星人，并让其居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_screen(ai_settings,screen,ship,aliens,bullets,play_button,stats,sb):
    #重绘屏幕
    screen.fill(ai_settings.bg_color)
    #绘制飞船、外星人、记分牌和子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活跃状态时，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    ##让屏幕绘制可见
    pygame.display.flip()


def update_bullets(ai_settings,screen,ship,aliens,bullets,sb,stats):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collissions(ai_settings,screen,ship,aliens,bullets,sb,stats)

def check_bullet_alien_collissions(ai_settings,screen,ship,aliens,bullets,sb,stats):
    #检察是否有子弹击中外星人，并且删除相应的外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    #击中外星人后加分
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        #检查是否超过最高得分然后更新最高得分
        check_high_score(stats,sb)
    #检察外星人是否为空，然后创建外星人
    if len(aliens) == 0:
        #删除现有的子弹并创建一组新的外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高飞船的等级
        stats.level += 1
        sb.prep_level()
        #创建外星人
        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一个新的子弹到编组bullters中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullter = Bullter(ai_settings, screen, ship)
        bullets.add(new_bullter)

def get_number_aliens_x(ai_settings,alien_width):
    #根据屏幕的大小获取外星人的数量
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    #根据屏幕大小获取外星人的行数
    available_space_y = (ai_settings.screen_height - (3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #创建外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    #创建一组外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def change_fleet_direction(ai_settings,alines):
    #外星人向下移动，并改变方向
    for alien in alines.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings,aliens):
    #外星人到达边缘后采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def ship_hit(ai_settings,screen,stats,aliens,ship,bullets):
      #响应被外星人撞到飞船后的结果
    if stats.ship_left > 0:
        #将stats.ship_left减1
        stats.ship_left -= 1
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新外星人，并将飞船放到屏幕底部
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,aliens,ship,bullets):
    #检察外星人是否到达底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #飞船像被撞到一样处理
            ship_hit(ai_settings,screen,stats,aliens,ship,bullets)
            break

def update_aliens(ai_settings,screen,stats,aliens,ship,bullets):
    #更新外星人的位置
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,aliens,ship,bullets)
    #检察是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings,screen,stats,aliens,ship,bullets)

def check_high_score(stats,sb):
    #检查是否超过最高得分然后更新最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
