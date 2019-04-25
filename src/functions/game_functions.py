import sys
from time import sleep

import pygame
from bullet import Bullet

from alien import Alien


def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		# 向右移动
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		# 向左移动
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	# 添加一个退出游戏的Q键
	elif event.key == pygame.K_q:
		sys.exit()
		

def fire_bullet(ai_settings,screen,ship,bullets):
	# 创建一颗子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		# 向右移动
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		# 向左移动
		ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	# 通过for循环来监听每一个事件（事件指的是例如鼠标移动，键盘输入之类）
	for event in pygame.event.get():
		# 通过多个if语句来匹配所监听到的事件
		if event.type == pygame.QUIT:
			# 根据匹配到的事件执行相应的操作
			sys.exit()

		# 每次按键都被注册为一个KEYDOWN事件
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		# 每次松开按键被注册为一个KEYUP事件
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,
							  aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,
					  aliens,bullets,mouse_x,mouse_y):
	"""在玩家点击play按钮时开始新的游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
	#if play_button.rect.collidepoint(mouse_x,mouse_y):
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True

		# 重置计分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	# 每次更新屏幕都重新绘制颜色
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重新绘制所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 更新屏幕（通过隐藏原始位置，显示新位置来达到更新屏幕的效果）
	ship.blitme()
	# alien.blitme()
	aliens.draw(screen)

	# 显示得分
	sb.show_score()

	# 如果游戏处于非活动状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()
	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""更新子弹的位置，并删除已经消失的子弹"""
	bullets.update()
	# 删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# print(len(bullets)) 用于验证子弹数量是否逐渐消失
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
								  aliens,bullets)


def check_bullet_alien_collisions(ai_settings, screen,stats,sb,
								  ship, aliens, bullets):
	"""响应子弹和外星人发生碰撞"""
	# 删除发生碰撞的子弹和外星人
	collisions = pygame.sprite.groupcollide(aliens,bullets, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens) == 0:
		# 删除现有子弹并创建一群外星人
		bullets.empty()
		ai_settings.increase_speed()

		# 提高等级
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings,screen,ship,aliens)


def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行能容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height -
		(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	# 创建一个外星人，并计算一行能容纳多少个
	# 外星人间距为外星人的宽度
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
		alien.rect.height)
	
	# 创建外星人群
	for row_number in range(number_rows):
		# 创建第一行外星人
		for alien_number in range(number_aliens_x):
			# 创建一个外星人并将其加入当前行
			create_alien(ai_settings,screen,aliens,alien_number,
				row_number)

def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""响应被外星人碰撞到的飞船"""
	if stats.ships_left > 0:
		# 将ships_left减1
		stats.ships_left -= 1

		# 更新计分牌
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人，并将飞船放到屏幕底端中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""检测是否有外星人达到屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样处理
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			print("被包围了吧，小姑娘！")
			break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	'''
	检查是否有外星人到达屏幕边缘
	然后更新所有外星人的位置
	'''
	check_fleet_edges(ai_settings,aliens)
	"""更新外星人群中所有外星人的位置"""
	aliens.update()

	# 检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
		print("哈哈哈，被我逮到了吧！")

	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
	"""检查是否诞生了新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()