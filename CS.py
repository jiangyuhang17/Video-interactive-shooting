# -*- coding:utf-8 -*-
import pygame
import time
import random
import GunShot

import serial
#ser = serial.Serial('COM4', 9600)

#设置各种全局常量
screen_width = 1280
screen_height = 760
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
num_highest = 0
fullscreen = False

pygame.init()#初始化Pygame

#创建Pygame窗口，并实例化为screen对象
screen = pygame.display.set_mode((screen_width, screen_height), 0)#设置窗口大小（宽度，高度）
pygame.display.set_caption('CS')#设置窗口标题（文字内容）
clock = pygame.time.Clock()#设置时钟

#加载图片
background = pygame.image.load('background.jpg')
gun = pygame.image.load('gun.png')
bullet = pygame.image.load('bullet.png')
SWAT = pygame.image.load('enemy.png')
SWAT_2 = pygame.image.load('enemy_2.png')
SWAT_3 = pygame.image.load('enemy_3.png')
headshot = pygame.image.load('headshot.png')
headshot_gold = pygame.image.load('headshot_gold.png')
shot = pygame.image.load('shot.png')
#加载声音
sound_gun = pygame.mixer.Sound('gun.wav')
sound_headshot = pygame.mixer.Sound('headshot.wav')
sound_headshot_gold = pygame.mixer.Sound('headshot_gold.wav')
sound_shot = pygame.mixer.Sound('shot.wav')
#加载音乐
music = pygame.mixer.music.load('music.mp3')


def message_display(text,textSize,textColor,x,y):#添加文字的方法
	font = pygame.font.Font(None, textSize)#创建字体对象（字体，大小）
	textImage = font.render(text, True, textColor, None)#将字体转换为图片（文字，是否反锯齿，颜色，背景）
	screen.blit(textImage,(x - textImage.get_width()/2, y - textImage.get_height()/2))#添加图片，即转换成图片过后的文字

def game_intro():
	while True:
		global fullscreen
		
		for event in pygame.event.get():#获取Pygame事件
			if event.type == pygame.QUIT:#如果获取到的事件类型为QUIT，则退出游戏
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:#按F1退出游戏
					pygame.quit()
					quit()
				if event.key == pygame.K_f:#按f转换全屏模式
					if fullscreen == False:
						pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
					else:
						pygame.display.set_mode((screen_width, screen_height), 0)
					fullscreen = not fullscreen
				if event.key == pygame.K_SPACE:#按下空格，进入游戏主界面
					game_loop()

		
		screen.fill(green)#填充窗口（颜色）
		screen.blit(background, (0,0))#添加图片（图片，位置）
		message_display('Press SPACE to start game', 50, bright_green,screen_width/2, screen_height/2)
		
		pygame.display.update()#更新Pygame窗口


class enemy:
	health = 0
	x = 0
	y = 0
	width = 0
	height = 0
	direction = 0
	character = 0
	rand_attack = 0
	
	def __init__(self, num_character):  
		self.health = 100
		self.x = random.randrange(0, screen_width - SWAT.get_width())
		self.y = random.randrange(350, screen_height - 100)
		self.width = int(self.y * 0.25 - 40)
		self.height = int(self.y * 0.5 - 70)
		self.direction = random.randrange(0,2)
		self.character = random.randrange(0,num_character)
	def appear(self):
		#产生随机大小、随机角色的敌人
		if self.character == 0:
			new_SWAT = pygame.transform.scale(SWAT, (int(self.y * 0.25 - 40), int(self.y * 0.5 - 70)))
		elif self.character == 1:
			new_SWAT = pygame.transform.scale(SWAT_2, (int(self.y * 0.25 - 40), int(self.y * 0.5 - 70)))
		else:
			new_SWAT = pygame.transform.scale(SWAT_3, (int(self.y * 0.25 - 40), int(self.y * 0.5 - 70)))
		#放置在随机位置
		screen.blit(new_SWAT, (self.x, self.y))
		pygame.draw.rect(screen, red, (self.x + 10, self.y - 10, self.health, 10))#显示血量条


#游戏主进程
def game_loop():

	#游戏主进程需要用到的变量
	target_radius = 15
	num_shot = 0
	num_headshot = 0
	num_headshot_gold = 0
	num_total = 0
	num_bullet = 10
	my_health = 100
	state = 1
	
	list = []
	list.append(enemy(state))
	
	
	while True:
		global fullscreen, num_highest
		
		#导入openCV
		mouse_x,mouse_y = GunShot.center()
		
		#导入Arduino
#		line = ser.readline()
#		data = [int(val) for val in line.split()]
		
		#增加难度的条件
		if num_total % 10 == 0:
			if state == num_total / 10:
				list.append(enemy(state))
				state = state + 1
		
		mouse_x, mouse_y = pygame.mouse.get_pos()#获取到鼠标位置
		target_x = mouse_x#靶心X坐标
		target_y = mouse_y#靶心Y坐标
		
		#填充窗口，添加图片
		screen.blit(background, (0,0))
		screen.blit(gun, (mouse_x - gun.get_width()/2, screen_height - gun.get_height()))
		
		for event in pygame.event.get():#获取Pygame事件
			if event.type == pygame.QUIT:#如果获取到的事件类型为QUIT，则退出游戏
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:#按F1退出游戏
					pygame.quit()
					quit()
				if event.key == pygame.K_f:#按f转换全屏模式
					fullscreen = not fullscreen
					if fullscreen == False:
						pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN, 32)
					else:
						pygame.display.set_mode((screen_width,screen_height), 0, 32)
			if event.type == pygame.MOUSEBUTTONDOWN:#按下鼠标的事件
				if event.button == 1 and num_bullet != 0:#按下鼠标左键的事件
#		print data
#		if data[0] == 1:
					pygame.mixer.Sound.play(sound_gun)#开枪发出的声音
					num_bullet = num_bullet - 1#消耗一枚子弹
					
					for item in list:#对不同射击方式进行结算
					
						if mouse_x > item.x + item.width * 0.383 and mouse_x < item.x + item.width * 0.458 and mouse_y > item.y + item.height * 0.031 and mouse_y < item.y + item.height * 0.108:
							item.health = item.health - random.randrange(90, 110)#黄金爆头的话，每次打掉对面100点血
							
							if item.health <= 0:#黄金爆头打死
								list.remove(item)#删除这个敌人
								list.append(enemy(state))#新加入一个敌人
								pygame.mixer.Sound.play(sound_headshot_gold)#播放声音
								num_headshot_gold = num_headshot_gold + 1#增加相应击杀数
								num_total = num_total + 1#也会增加总击杀数
						
						elif mouse_x > item.x + item.width * 0.318 and mouse_x < item.x + item.width * 0.527 and mouse_y > item.y + item.height * 0.031 and mouse_y < item.y + item.height * 0.191:
							item.health = item.health - random.randrange(40, 60)#爆头的话，每次打掉对面50点血
							
							if item.health <= 0:#爆头打死
								list.remove(item)
								list.append(enemy(state))
								pygame.mixer.Sound.play(sound_headshot)
								num_headshot = num_headshot + 1
								num_total = num_total + 1
						
						elif mouse_x > item.x + item.width * 0.127 and mouse_x < item.x + item.width * 0.729 and mouse_y > item.y + item.height * 0.031 and mouse_y < item.y + item.height * 0.955:
							item.health = item.health - random.randrange(15, 25)#普通的话，每次打掉对面20点血
							
							if item.health <= 0:#普通打死
								list.remove(item)
								list.append(enemy(state))
								pygame.mixer.Sound.play(sound_shot)
								num_shot = num_shot + 1
								num_total = num_total + 1
								
				if event.button == 3:#按下鼠标右键的事件
					num_bullet = 10#补充子弹
				
				
		for item in list:
			#敌人移动
			if item.direction == 0:
				item.x = item.x + state
			else:
				item.x = item.x - state
			#敌人攻击
			item.rand_attack = random.randrange(0, 50)#1/50的概率会攻击
			if item.rand_attack == 0:
				my_health = my_health - 1
			#敌人移出屏幕后，重新产生敌人
			if item.x + item.width < 0 or item.x > screen_width:
				list.remove(item)
				list.append(enemy(state))
		
		#一直点击鼠标，靶心会抖动
		if pygame.mouse.get_pressed()[0] == 1:
			target_x = random.randrange(mouse_x - 3 ,mouse_x + 3)
			target_y = random.randrange(mouse_y - 3 ,mouse_y + 3)
			target_radius = random.randrange(15, 25)
		
		#添加文字
		screen.blit(pygame.transform.scale(headshot_gold, (100, 100)), (100, 100))#scale是缩放
		message_display(str(num_headshot_gold), 50, white, 250, 150)
		screen.blit(pygame.transform.scale(headshot, (100, 100)), (100, 200))
		message_display(str(num_headshot), 50, white, 250, 250)
		screen.blit(pygame.transform.scale(shot, (150, 150)), (73, 280))
		message_display(str(num_shot), 50, white, 250, 350)
		message_display('The highest point is ' + str(num_highest), 50, white, 250, 50)
		
		#显示敌人
		for item in list:
			item.appear()
		
		#显示我的血量条
		pygame.draw.rect(screen, red, (0, screen_height - 50, my_health * 10, 50))
		message_display(str(my_health), 40, white, 50, screen_height - 60)
		
		#显示子弹
		for i in range(0, num_bullet):
			screen.blit(pygame.transform.scale(bullet, (35, 70)), (350 + i * 50, 100))
		
		#显示靶心
		pygame.draw.circle(screen, green, (target_x, target_y), target_radius, 3)#画出靶心外圆
		pygame.mouse.set_visible(False)#隐藏鼠标
		pygame.draw.circle(screen, green, (target_x, target_y), 3)#画出靶心内圆
		
		#游戏结束
		if my_health <= 0:
			num_highest = num_total
			screen.blit(background,(0,0))
			message_display('Game Over!', 100, bright_green, screen_width/2, screen_height/2)
			pygame.display.update()
			time.sleep(2)
			
			screen.blit(background,(0,0))
			message_display('Your count is ' + str(num_total), 200, bright_green, screen_width/2, screen_height/2)
			pygame.display.update()
			time.sleep(3)
			
			game_loop()
		
		pygame.display.update()#更新Pygame窗口
		
if __name__ == '__main__':
	pygame.mixer.music.play(1)#播放音乐
	game_intro()#进入游戏，进入开始画面