import pygame
from random import randint
from random import choice
import time
pygame.init()


class player:

	def __init__(self, root, w, h, x, y):
		self.w = w
		self.h = h
		self.x = x
		self.y = y
		self.root = root
		self.speed = 10
		self.health = 100
		self.bulits = []
		self.t1 = time.time()

	def Update(self, Enimes):

		pygame.draw.circle(self.root, (0, 255, 0), (self.x, self.y) , 20)
		keys =  pygame.key.get_pressed()

		# Player Max Health:
		if self.health > 100:
			self.health = 100

		# Player Max Position:
		if self.x > self.w+50 :
			self.x = -50
		if self.x < -50 :
			self.x = self.w+50
		if self.y > self.h+50:
			self.y = -50
		if self.y < -50:
			self.y = self.h+50

		# Player Inputs:
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.x += self.speed
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.x -= self.speed
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.y += self.speed
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.y -= self.speed

		# Update Player Bulits:
		for i, (bulit, ene) in enumerate(zip(self.bulits, Enimes)):
			bulit.Update(ene, Enimes, self.bulits, i)

		self.bulits = self.bulits[0:len(Enimes)]


class Bulit():

	def __init__(self, root, w, h, x, y):
		self.speed = 5
		self.root = root
		self.x = x
		self.y = y

	def Update(self, ENE, Enimes, bulits, I):
		pygame.draw.circle(self.root, (0, 0, 255), (self.x, self.y), 5)

		# Move The Loot To Player Position:

		self.x+= round((ENE.x-self.x)/abs(ENE.x-self.x)*self.speed) if (ENE.x-self.x) else 0
		self.y+= round((ENE.y-self.y)/abs(ENE.y-self.y)*self.speed) if (ENE.y-self.y) else 0

		# Check if The Loot in Player Position:

		if self.x in range(ENE.x-5, ENE.x+5, 1) and self.y in range(ENE.y-5, ENE.y+5, 1):
				Enimes.pop(I)
				bulits.pop(I)


class Loot:

	def __init__(self, root, w, h, Type):
		self.Freeze = False
		self.speed = 5
		self.Type = Type
		self.root = root
		self.w = w
		self.h = h

		# Random Start Position :

		randside = randint(0 ,3)
		if randside == 0:
			self.x = randint(0, w)
			self.y = -50
		elif randside == 1:
			self.x = w+50
			self.y = randint(0, h)
		elif randside == 2:
			self.x = randint(0, w)
			self.y = h+50
		elif randside == 3:
			self.x = -50
			self.y = randint(0, h)


	def Update_Loot_Plus(self, playerOB, i, Loots):

		pygame.draw.circle(self.root, (255, 255, 0), (self.x, self.y) , 7)

		# Move The Loot To Player Position:

		self.x += round(self.speed*(playerOB.x-self.x)/self.w)
		self.y += round(self.speed*(playerOB.y-self.y)/self.h)

		# Check if The Loot in Player Position:

		if self.x in range(playerOB.x-25, playerOB.x+25, 1) and self.y in range(playerOB.y-25, playerOB.y+25, 1):
			Loots.pop(i)
			playerOB.health+=10
			



	def Update_Loot_Attack(self, playerOB, i ,Loots, Enimes):

		pygame.draw.circle(self.root, (0, 100, 230), (self.x, self.y), 7)
		
		# Move The Loot To Player Position:

		self.x += round(self.speed*(playerOB.x-self.x)/self.w)
		self.y += round(self.speed*(playerOB.y-self.y)/self.h)

		# Check if The Loot in Player Position:

		if self.x in range(playerOB.x-25, playerOB.x+25, 1) and self.y in range(playerOB.y-25, playerOB.y+25, 1):
			Loots.pop(i)
			for ene in Enimes:
				playerOB.bulits.append(Bulit(self.root, self.w, self.h, playerOB.x+choice((25, -25)), playerOB.y+choice((25, -25))))


	def Update_Freeze_Loot(self, playerOB, i ,Loots):

		pygame.draw.circle(self.root, (0, 255, 255), (self.x, self.y), 10)

		# Move The Loot To Player Position:

		self.x += round(self.speed*(playerOB.x-self.x)/self.w)
		self.y += round(self.speed*(playerOB.y-self.y)/self.h)

		# Check if The Loot in Player Position:

		if self.x in range(playerOB.x-25, playerOB.x+25, 1) and self.y in range(playerOB.y-25, playerOB.y+25, 1):
			Loots.pop(i)
			self.Freeze = True
			





class Enime:

	def __init__(self, root, w, h):
		
		self.speed = 5
		self.root = root
		self.w = w
		self.h = h

		# Random Start Position :

		randside = randint(0 ,3)
		if randside == 0:
			self.x = randint(0, w)
			self.y = -50
		elif randside == 1:
			self.x = w+50
			self.y = randint(0, h)
		elif randside == 2:
			self.x = randint(0, w)
			self.y = h+50
		elif randside == 3:
			self.x = -50
			self.y = randint(0, h)


	def Update(self, playerOB, i, Enimes, Freeze):

		pygame.draw.circle(self.root, (255, 0, 0), (self.x, self.y) , 5)

		if not Freeze:
			# Move The Loot To Player Position:
			self.x += round((self.speed)*((playerOB.x-self.x)/abs(playerOB.x-self.x))) if (playerOB.x-self.x)!= 0  else 0
			self.y += round((self.speed)*((playerOB.y-self.y)/abs(playerOB.y-self.y))) if (playerOB.y-self.y)!= 0  else 0

		# Check if The Loot in Player Position:

		if self.x in range(playerOB.x-25, playerOB.x+25, 1) and self.y in range(playerOB.y-25, playerOB.y+25, 1):
			Enimes.pop(i)
			playerOB.health-=5



w = 500
h = 500

root = pygame.display.set_mode( (w, h) )
pygame.display.set_caption('VIRUS GAME')
font = pygame.font.SysFont("comicsansms", 19)
clock = pygame.time.Clock()


def Game():

	playerOB = player(root, w, h, w//2, h//2)
	Freeze = False
	Enimes = []
	Loots = []
	EnimesTime = time.time()
	FreezeTime = time.time()
	StartTime  = time.time()

	# Main Loop:

	while True:

		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				return

		# Freeze Time :
		if Freeze and (time.time()-FreezeTime) > 2:
			Freeze = False

		# Update The Enimes:
		for i, ene in enumerate(Enimes):
			ene.Update(playerOB, i, Enimes, Freeze)

		# Update The loots :
		for i, loot in enumerate(Loots):

			if loot.Type == 'A':
				loot.Update_Loot_Attack(playerOB, i ,Loots, Enimes)

			elif loot.Type == 'P':
				loot.Update_Loot_Plus(playerOB, i, Loots)

			else:
				loot.Update_Freeze_Loot(playerOB, i ,Loots)
				Freeze = loot.Freeze if not Freeze else True
				if not Freeze:
					FreezeTime = time.time()

		# Update The Player:
		playerOB.Update(Enimes)

		# Create Enimes :
		if randint(0,100) == 0:
			Enimes.extend([Enime(root, w, h) for _ in range(randint(0,int(time.time()-StartTime)//20+1))])
			EnimesTime = time.time()

		# Create Loots :
		if randint(0, 160) == 10:
			Loots.extend([Loot(root, w, h, 'P') for _ in range((int(time.time()-StartTime)//60+1))])
		if randint(0, 200) == 10:
			Loots.extend([Loot(root, w, h, 'A') for _ in range((int(time.time()-StartTime)//60+1))])
		if randint(0, 300) == 10:
			Loots.extend([Loot(root, w, h, 'F') for _ in range((int(time.time()-StartTime)//100+1))])

		# Draw Health Bar :
		pygame.draw.rect(root, (255, 255, 255), (int((95/500)*w), int((470/500)*h), int((300/500)*w), int((16/500)*h)))
		pygame.draw.rect(root, (0, 255, 0), (int((95/500)*w), int((470/500)*h), int(playerOB.health/100*int((300/500)*w)), int((16/500)*h)))

		# Blit The Score:
		root.blit(font.render(str(playerOB.health), True, (0, 0, 0)), (int((236/500)*w), int((463/500)*h)))
		root.blit(font.render('Score : '+str(int(time.time()-StartTime)), True, (255, 255, 255)), ((w//2)-30, 30))
		pygame.display.update()

		root.fill((0, 0, 0))
		clock.tick(60)

		if playerOB.health <= 0:
			break
		

	Game()

Game()
pygame.quit()
