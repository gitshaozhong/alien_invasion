# import sys
# sys.path.append('E:\\project_Python\\learn\\alien_invasion\src')
import pygame
from button import Button
from game_stats import GameStats
from pygame.sprite import Group
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

import game_functions as gf


def run_game():
	# 初始化背景设置
	pygame.init()
	# 创建Settings实例
	ai_settings = Settings()
	# 设置窗口大小
	screen = pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
	# 设置窗口名称
	pygame.display.set_caption("Alien Invasion")

	# 创建play按钮
	play_button = Button(ai_settings,screen,"Can't catch me!")

	# 创建一个用于存储游戏统计信息的实例
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings,screen,stats)

	# 设置背景颜色
	# bg_color = (230,230,230)
	# 创建一艘ship
	ship = Ship(ai_settings,screen)
	# 创建外星人
	# alien = Alien(ai_settings,screen)
	# 创建一个存储在子弹的编组
	bullets = Group()
	aliens = Group()
	# 创建外星人群
	gf.create_fleet(ai_settings,screen,ship,aliens)

	# 通过while循环来控制整个游戏
	while True:
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,
						aliens,bullets)

		if stats.game_active:
			ship.update()
			# 先更新子弹，再更新外星人，然后检测是否有子弹撞到外星人
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens, bullets)
			gf.update_aliens(ai_settings, screen,stats,sb,ship,aliens,bullets)
		gf.update_screen(ai_settings, screen, stats,sb,ship, aliens, bullets,
						 play_button)


if __name__ == "__main__":
	run_game()