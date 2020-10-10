#-*- codding = utf-8 -*-
#author = huang
class GameStats():
    #跟踪游戏的统计信息
    def __init__(self,ai_settings):
        #初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动时处于非活跃状态
        self.game_active = False
        #游戏最高得分在任何情况下都不能被重置
        self.high_score = 0


    def reset_stats(self):
        #初始化游戏中的变化统计信息
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1