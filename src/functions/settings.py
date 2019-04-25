class Settings():
	"""本部分存储着游戏所有设置的类"""

	def __init__(self):
		self.screen_width = 1000
		self.screen_height = 600
		self.bg_color = (255,192,203)

		# ship移动的速度属性
		self.ship_speed_factor = 1.2
		self.ship_limit = 3

		# 子弹设置
		self.bullet_speed_factor = 20
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3

		# 外形人设置
		self.alien_speed_factor = 0.5
		self.fleet_drop_speed = 10
		# fleet_direction为“1”表示向右移动，为“-1”表示向左移动
		self.fleet_direction = 1

		# 加快游戏节奏
		self.speedup_scale = 1
		# 外星人点数的提高速度
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):

		# 计分
		self.alien_points = 50

	def increase_speed(self):
		"""提高速度设置和外星人点数"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points*self.score_scale)
		# print(self.alien_points)