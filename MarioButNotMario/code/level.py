import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from tiles import Tile 
from settings import tile_size, screen_width, screen_height
from player import Player
import time
from menu import *
from settings import *
import xlsxwriter
import openpyxl
global score
score = 0
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
def gamequit():
    pygame.quit()
    quit()

def click(msg,x, y, w, h, ic, ac, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
		if click[0] == 1 and action !=None:

			action()
	else:
		pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
	pygame.init()
	smallText = pygame.font.Font("8-BIT WONDER.TTF", 15)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x+(w/2)), (y+(h/2)))
	gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()
class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.display_surface = surface 
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0
		self.score = 0


	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				
				if cell == 'X':
					tile = Tile(tile_size,x,y)
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y))
					self.player.add(player_sprite)

	def scroll_x(self):
		global score
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			if self.score <= 0:
				pass
			else:
				score = score - 8
				self.score = self.score - 8
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.score = self.score + 8
			score = score + 8
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8
	def get_score(self):
		score = self.score
		return score

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def leaderboard():
		while True:
			wb = openpyxl.load_workbook('leaderboard.xlsx')
			sheet = wb.active
			x1 = sheet['A1'].value
			if int(x1) < score:
				workbook = xlsxwriter.Workbook('leaderboard.xlsx')
				worksheet = workbook.add_worksheet()
				worksheet.write('A1', str(score))
				workbook.close()
				high = score
			else:
				high = x1

			screen = pygame.display.set_mode((screen_width, screen_height))
			clock = pygame.time.Clock()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			screen.fill('beige')
			largetext = pygame.font.Font('8-BIT WONDER.TTF', 30)
			mediumtext = pygame.font.Font('8-BIT WONDER.TTF', 20)
			TextSurf, TextRect = text_objects("Le Leaders", largetext)
			TextRect.center = ((screen_width / 2), (screen_height * 4 / 100))
			gameDisplay.blit(TextSurf, TextRect)

			TextSurf, TextRect = text_objects("Top score is "+str(high), mediumtext)
			TextRect.center = ((screen_width / 2), (screen_height * 30 / 100))
			gameDisplay.blit(TextSurf, TextRect)

			TextSurf, TextRect = text_objects("Your score is "+ str(score), mediumtext)
			TextRect.center = ((screen_width / 2), (screen_height * 50 / 100))
			gameDisplay.blit(TextSurf, TextRect)

			click("Quit", screen_width *45/100, screen_height * 2 / 3, 100, 50, (0, 200, 0), (0, 255, 0), gamequit)
			pygame.display.update()
			clock.tick(60)
	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			death = True
			while death:
				self.playing = False
				screen = pygame.display.set_mode((screen_width, screen_height))
				clock = pygame.time.Clock()

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				screen.fill('beige')
				largetext = pygame.font.Font('8-BIT WONDER.TTF', 30)
				TextSurf, TextRect = text_objects("You died lmao hehehahahaha trash", largetext)
				TextRect.center = ((screen_width / 2), (screen_height / 2))
				gameDisplay.blit(TextSurf, TextRect)

				click("Leaderboard", screen_width/3, screen_height*2/3, 175, 50, (0, 200, 0), (0, 255, 0), Level.leaderboard)

				click("Quit", screen_width*2/3, screen_height*2/3, 100, 50, (100, 0, 255), (0, 0, 255), gamequit)
				pygame.display.update()
				clock.tick(60)
	def run(self):
		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()


		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)
		self.check_death()