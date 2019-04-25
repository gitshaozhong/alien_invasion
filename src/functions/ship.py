import pygame
from pygame.sprite import Sprite


# 'E:\\project_Python\\learn\\alien_invasion\\images\\ship.bmp'
image_path = r'E:/project_Python/learn/alien_invasion/images/ship.bmp'

class Ship(Sprite):

	def __init__(self,ai_settings,screen):
		"""初始化飞船，并设置其起始位置"""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# 加载ship图像，并获取外接矩形
		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# 将每艘新ship放在屏幕中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# 在飞船的属性center中存储小数值
		self.center = float(self.rect.centerx)

		# 添加一个moving_right属性用来实现ship向右的持续移动
		self.moving_right = False
		#添加一个moving_left属性用来实现ship向左的持续移动
		self.moving_left = False

	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		# 根据self.center更新rect对象
		self.rect.centerx = self.center

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		self.center = self.screen_rect.centerx