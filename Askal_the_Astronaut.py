import pyglet
#shortens pyglet.window.key and pyglet.window.FPSDisplay into key and FPSDisplay only
from pyglet.window import key, FPSDisplay
#shortens pyglet.sprite.Sprite into Sprite only
from pyglet.sprite import Sprite
#imports the Objects.py module
from Objects import Objects
from random import randint

#preloads the images for easier usage
def preload_image(image):	
	img = pyglet.image.load("sprites/"+image)
	return img
#open the high score file
def load(file):
	file_to_be_opened = open(file)
	hscore = file_to_be_opened.read()
	return hscore

#saves the high score file
def save(file, score):
	file_to_be_saved = open(file,"w")
	file_to_be_saved.write(str(score))


class Window(pyglet.window.Window):
	#automatically called when Window class is called
	def __init__(self,*args,**kwargs):
		#super function can call parent classes that can be mentioned in *args and **kwargs
		super().__init__(*args,**kwargs)
		self.set_location(50,30)
		self.frame_rate = 1/60
		self.fps = FPSDisplay(self)
		self.fps.label.font_size = 25
		self.fps.label.x = 1050
		self.fps.label.y = 650

		#player's speed is initially 0 or False
		self.right = False
		self.left = False

		#sets player
		player_sprite = Sprite(preload_image("Askal.png"))
		self.player = Objects(500, 100, player_sprite)
		self.player_speed = 200
		self.player_present = False
		self.player_life = 3
		self.player_lives = True

		self.background_list = []
		self.background_image = preload_image("space.jpg")
		#creates an initial 2 copies of the background image
		for i in range(2):
			self.background_list.append(Objects(0,i*1200,Sprite(self.background_image)))
		#moves the image downwards
		for bg in self.background_list:
			bg.velocityy = -150
		self.counter = 1

		#for drawing the sprites and objects in one call
		self.batch = pyglet.graphics.Batch()
		self.pre_batch = pyglet.graphics.Batch()
		self.asteroid_list = []
		self.orbs_list = []

		#asteroids
		self.asteroid1 = preload_image("asteroid1.png")
		self.asteroid1_order = pyglet.image.ImageGrid(self.asteroid1,8,8,item_width=128,item_height=128)
		self.asteroid1_anim = pyglet.image.Animation.from_image_sequence(self.asteroid1_order[0:],0.1,loop=True)
		self.asteroid1_spawner = 5
		
		self.asteroid2 = preload_image("asteroid2.png")
		self.asteroid2_order = pyglet.image.ImageGrid(self.asteroid2,4,5,item_width=72,item_height=72)
		self.asteroid2_anim = pyglet.image.Animation.from_image_sequence(self.asteroid2_order[0:],0.1,loop=True)
		self.asteroid2_spawner = 5

		self.asteroid3 = pyglet.image.load("Sprites/asteroid3.png")
		self.asteroid3_order = pyglet.image.ImageGrid(self.asteroid3,1,5,item_width=250,item_height=136)
		self.asteroid3_anim = pyglet.image.Animation.from_image_sequence(self.asteroid3_order[0:],0.2,loop=True)
		self.asteroid3_spawner = 5

		self.asteroid4 = pyglet.image.load("Sprites/asteroid4.png")
		self.asteroid4_order = pyglet.image.ImageGrid(self.asteroid4,1,5,item_width=250,item_height=136)
		self.asteroid4_anim = pyglet.image.Animation.from_image_sequence(self.asteroid4_order[0:],0.2,loop=True)
		self.asteroid4_spawner = 5

		self.asteroid5 = []
		for i in range(8):
			img = pyglet.resource.image("Sprites/asteroid5-"+str(i+1)+".png")
			self.asteroid5.append(img)
		self.asteroid5_anim = pyglet.image.Animation.from_image_sequence(self.asteroid5,0.2,True)
		self.asteroid5_spawner = 5
		
		
		
		#orbs and superpower
		self.superpower = True

		#Adds +5 points to the score
		self.orbs1 = preload_image("orbs1.png")
		self.orbs1_order = pyglet.image.ImageGrid(self.orbs1,4,5,item_width=50,item_height=50)
		self.orbs1_anim = pyglet.image.Animation.from_image_sequence(self.orbs1_order[0:],0.1,loop=True)
		self.orbs1_spawner = 10
		self.additional = 0

		#Doubles the base score for a definite point threshold
		self.orbs2 = preload_image("orbs2.png")
		self.orbs2_order = pyglet.image.ImageGrid(self.orbs2,4,5,item_width=50,item_height=50)
		self.orbs2_anim = pyglet.image.Animation.from_image_sequence(self.orbs2_order[0:],0.1,loop=True)
		self.orbs2_spawner = 30
		self.orbs2_press = False
		self.orbs2_effect = False
		
		#Destroys all asteroids on the screen
		self.orbs3 = preload_image("orbs3.png")
		self.orbs3_order = pyglet.image.ImageGrid(self.orbs3,4,5,item_width=50,item_height=50)
		self.orbs3_anim = pyglet.image.Animation.from_image_sequence(self.orbs3_order[0:],0.1,loop=True)
		self.orbs3_spawner = 50
		self.orbs3_press = False
		
		#Gives two extra lives
		self.orbs4 = preload_image("orbs4.png")
		self.orbs4_order = pyglet.image.ImageGrid(self.orbs4,4,5,item_width=50,item_height=50)
		self.orbs4_anim = pyglet.image.Animation.from_image_sequence(self.orbs4_order[0:],0.1,loop=True)
		self.orbs4_spawner = 75
		self.orbs4_press = False
		
		#Player becomes invulnerable for a definite period
		self.orbs5 = preload_image("orbs5.png")
		self.orbs5_order = pyglet.image.ImageGrid(self.orbs5,4,5,item_width=50,item_height=50)
		self.orbs5_anim = pyglet.image.Animation.from_image_sequence(self.orbs5_order[0:],0.1,loop=True)
		self.orbs5_spawner = 110
		self.orbs5_press = False
		self.orbs5_effect = False
		self.orbs5_multiplier = 0
		self.invulnerable = 0
		


		#creates a label for the score text
		self.scorelabel = pyglet.text.Label("Score:", x=960 , y=550, batch=self.batch)
		self.scorelabel.font_size = 18

		#creates a label to show current score
		self.curr_score = pyglet.text.Label(str(0), x=1035, y=550, batch=self.batch)
		self.curr_score.color = (150, 200, 250, 150)
		self.curr_score.font_size = 18
		self.score = 0
		
		#creates a label for the high score text
		self.hscore_text = pyglet.text.Label("High Score:", x=900, y=500, batch=self.batch)
		self.hscore_text.font_size = 18

		#creates a label to show high score
		self.hscore = load("highscore.txt")
		self.hscore_num = pyglet.text.Label(self.hscore, x=1035, y=500)
		self.hscore_num.color = (255,100,100,100)
		self.hscore_num.font_size = 18

		#creates a label to show lives left text
		self.lives_left_label = pyglet.text.Label("Lives Left:", x=915, y=450, batch=self.batch)
		self.lives_left_label.font_size = 18

		#creates a label to show lives left
		self.lives_left_num = pyglet.text.Label(str(3), x=1035, y=450)
		self.lives_left_num.color = (200,200,200,200)
		self.lives_left_num.font_size = 18

		#creates a label to show superpower availability
		self.superpower_label = pyglet.text.Label("[1] Superpower:", x=830, y = 225, batch=self.batch)
		self.superpower_label.font_size = 16
		self.superpower_label.color = (100,100,100,250)

		#creates a label to show actual truth value of superpower
		self.superpower_bool = pyglet.text.Label(str(True), x=1045, y=225, batch=self.batch)
		self.superpower_bool.font_size = 16
		self.superpower_bool.color = (0,150,255,200)

		#creates a label to show duration of orbs2 effect
		self.orbs2_effect_label = pyglet.text.Label("[2] Double Score:       points left", x=830, y = 200, batch=self.batch)
		self.orbs2_effect_label.font_size = 16
		self.orbs2_effect_label.color = (100,100,100,250)

		#creates a label to show actual duration of orbs2 effect
		self.orbs2_effect_num = pyglet.text.Label(str(0), x=1000, y=200, batch=self.batch)
		self.orbs2_effect_num.font_size = 16
		self.orbs2_effect_num.color = (0,150,255,200)

		#creates a label to show orbs3 availability
		self.orbs3_effect_label = pyglet.text.Label("[3] Destroy Asteroids:", x=830, y = 175, batch=self.batch)
		self.orbs3_effect_label.font_size = 16
		self.orbs3_effect_label.color = (100,100,100,250)

		#creates a label to show actual truth value of orbs3
		self.orbs3_effect_bool = pyglet.text.Label(str(False), x=1045, y=175, batch=self.batch)
		self.orbs3_effect_bool.font_size = 16
		self.orbs3_effect_bool.color = (0,150,255,200)

		#creates a label to show orbs4 availability
		self.orbs4_effect_label = pyglet.text.Label("[4] +2 Extra Lives:", x=830, y = 150, batch=self.batch)
		self.orbs4_effect_label.font_size = 16
		self.orbs4_effect_label.color = (100,100,100,250)

		#creates a label to show actual truth value of orbs4
		self.orbs4_effect_bool = pyglet.text.Label(str(False), x=1045, y=150, batch=self.batch)
		self.orbs4_effect_bool.font_size = 16
		self.orbs4_effect_bool.color = (0,150,255,200)

		#creates a label to show duration of orbs5 effect
		self.orbs5_effect_label = pyglet.text.Label("[5] Invulnerablity:      seconds left", x=830, y = 125, batch=self.batch)
		self.orbs5_effect_label.font_size = 16
		self.orbs5_effect_label.color = (100,100,100,250)

		#creates a label to show actual duration of orbs5 effect
		self.orbs5_effect_num = pyglet.text.Label(str(0), x=995, y=125, batch=self.batch)
		self.orbs5_effect_num.font_size = 16
		self.orbs5_effect_num.color = (0,150,255,200)

		#creates a label to show the title of the game
		self.askal = pyglet.text.Label("Askal the Astronaut", x=590, y=600, batch=self.pre_batch)
		self.askal.anchor_x = "center"
		self.askal.anchor_y = "center"
		self.askal.font_name = "Calibri"
		self.askal.font_size = 40

		#creates a label to show the character to be palyed
		self.pre_player = Sprite(preload_image("Askal.png"), x=530,y=460, batch=self.pre_batch)

		#creates a label when the game is not yet starting
		self.pre = pyglet.text.Label("Press 'space' to start", x=575, y=400, batch=self.pre_batch)
		self.pre.anchor_x = "center"
		self.pre.anchor_y = "center"
		self.pre.font_name = "Arial"
		self.pre.font_size = 50

		#creates an animation for orbs while not yet starting
		self.pre_orb1 = Sprite(self.orbs1_anim, x=170,y=300, batch=self.pre_batch)
		self.pre_orb2 = Sprite(self.orbs2_anim, x=370,y=300, batch=self.pre_batch)
		self.pre_orb3 = Sprite(self.orbs3_anim, x=570,y=300, batch=self.pre_batch)
		self.pre_orb4 = Sprite(self.orbs4_anim, x=770,y=300, batch=self.pre_batch)
		self.pre_orb5 = Sprite(self.orbs5_anim, x=970,y=300, batch=self.pre_batch)
		self.orbs1_label = pyglet.text.Label("+5 Points!", x=155, y=275, batch=self.pre_batch)
		self.orbs2_label = pyglet.text.Label("Double Scoring!", x=340, y=275, batch=self.pre_batch)
		self.orbs3_label = pyglet.text.Label("Destroy Asteroids!", x=530, y=275, batch=self.pre_batch)
		self.orbs4_label = pyglet.text.Label("Two Extra Lives!", x=740, y=275, batch=self.pre_batch)
		self.orbs5_label = pyglet.text.Label("Invulnerability!", x=945, y=275, batch=self.pre_batch)

		#creates a label for superpower while not yet starting
		self.superpowerpre_label1 = pyglet.text.Label("|Superpower|", x=575, y=200,batch=self.pre_batch)
		self.superpowerpre_label1.anchor_x = "center"
		self.superpowerpre_label1.anchor_y = "center"
		self.superpowerpre_label1.font_name = "Arial"
		self.superpowerpre_label1.font_size = 25
		self.pre_orb1_1 = Sprite(self.orbs1_anim, x=455,y=120, batch=self.pre_batch)
		self.pre_orb2_1 = Sprite(self.orbs2_anim, x=505,y=120, batch=self.pre_batch)
		self.pre_orb3_1 = Sprite(self.orbs3_anim, x=555,y=120, batch=self.pre_batch)
		self.pre_orb4_1 = Sprite(self.orbs4_anim, x=605,y=120, batch=self.pre_batch)
		self.pre_orb5_1 = Sprite(self.orbs5_anim, x=655,y=120, batch=self.pre_batch)
		self.superpowerpre_label2 = pyglet.text.Label("Activate all 5 simultaneously!", x=575, y=110,batch=self.pre_batch)
		self.superpowerpre_label2.anchor_x = "center"
		self.superpowerpre_label2.anchor_y = "center"
		self.superpowerpre_label2.font_name = "Arial"
		self.superpowerpre_label2.font_size = 15


		#creates a label when the superpower is used
		self.superpower_label_used = pyglet.text.Label("SUPERPOWER USED!", x=575, y=400)
		self.superpower_label_used.anchor_x = "center"
		self.superpower_label_used.anchor_y = "center"
		self.superpower_label_used.font_name = "Helvetica"
		self.superpower_label_used.font_size = 50
		self.superpower_label_used.color = (100,255,150,150)
		self.superpower_activated = False
		self.superpower_activated_counter = 1

		#creates a label when the game is over
		self.game_over_label = pyglet.text.Label("Game Over!", x=575 , y=450)
		self.game_over_label.anchor_x = "center"
		self.game_over_label.anchor_y = "center"
		self.game_over_label.font_name = "Arial"
		self.game_over_label.font_size = 60

		#creates a label for reloading the game
		self.reload_label = pyglet.text.Label("Press 'enter' to reload", x=575, y=250)
		self.reload_label.anchor_x = "center"
		self.reload_label.anchor_y = "center"
		self.reload_label.font_name = "Arial"
		self.reload_label.font_size = 50

		#game is initially not yet starting
		self.start = False
		self.respawn = True
		self.reloading = False

		#loads the media files
		self.screen_shake_sound = pyglet.media.load("asteroidsound.wav", streaming=False)
		self.orb_acquired_sound = pyglet.media.load("orbsound.wav", streaming=False)
		self.destroy_asteroids_sound = pyglet.media.load("destroyasteroids.wav", streaming=False)



	#draws the objects and sprites into the window
	def on_draw(self):
		self.clear()
		for bg in self.background_list:
			bg.draw()
		if self.player_present:
			self.player.draw()
		if self.start:
			self.batch.draw()
			self.hscore_num.draw()
			self.lives_left_num.draw()
		else: 
			self.pre_batch.draw()
		if not self.player_lives:
			self.game_over_label.draw()
			self.reload_label.draw()
		if self.superpower_activated:
			self.superpower_label_used.draw()
		self.fps.draw()

	#performs actions when keys are pressed
	def on_key_press(self, symbol, modifiers):
		if symbol == key.RIGHT:
			self.right = True
		if symbol == key.LEFT:
			self.left = True
		if symbol == key.ESCAPE:
			#exits the application
			pyglet.app.exit()
		if symbol == key.SPACE and self.respawn:
			self.player_present = True
			self.start = True
			self.respawn = False
		if symbol == key.ENTER and self.reloading:
			self.reload()
			self.lives_left_num.text = str(3)
			self.superpower_bool.text = str(True)
			self.orbs2_effect_num.text = str(0)
			self.orbs3_effect_bool.text = str(False)
			self.orbs4_effect_bool.text = str(False)
			self.orbs5_effect_num.text = str(0)
			self.reloading = False
		if symbol == key._1 and self.superpower and not self.orbs2_press and not self.orbs2_effect and not self.orbs3_press and not self.orbs4_press and not self.orbs5_press and not self.orbs5_effect and self.player_lives:
			self.superpower_activated = True
			self.duration = 50
			self.future = int(self.score) + 50
			self.orbs2_effect = True

			for obj in self.asteroid_list:
				obj.batch = None
			self.asteroid_list.clear()
			self.destroy_asteroids_sound.play()
			self.screen_shake()

			self.player_life += 2
			self.lives_left_num.text = str(int(self.player_life))
			self.orbs4_effect_bool.text = str(False)

			self.orbs5_multiplier += 1
			self.invulnerable = 10*self.orbs5_multiplier
			self.orbs5_effect = True

			self.superpower_bool.text = str(False)
			self.superpower = False
			self.superpower_bool
		if symbol == key._2 and self.orbs2_press and self.player_lives:
			self.future = int(self.score) + 50
			self.orbs2_effect = True
			self.orbs2_press = False
		if symbol == key._3 and self.orbs3_press and self.player_lives:
			for obj in self.asteroid_list:
				obj.batch = None
			self.asteroid_list.clear()
			self.destroy_asteroids_sound.play()
			self.screen_shake()
			self.orbs3_effect_bool.text = str(False)
			self.orbs3_press = False
		if symbol == key._4 and self.orbs4_press and self.player_lives:
			self.player_life += 2
			self.lives_left_num.text = str(int(self.player_life))
			self.orbs4_effect_bool.text = str(False)
			self.orbs4_press = False
		if symbol == key._5 and self.orbs5_press and self.player_lives:
			self.orbs5_effect = True
			self.orbs5_press = False

	#stops the player when keys are release
	def on_key_release(self, symbol, modifiers):
		if symbol == key.RIGHT:
			self.right = False
		if symbol == key.LEFT:
			self.left = False

	#updates the position of the player
	def update_player(self,dt):
		self.player.update(dt)
		#player only allowed to move until the maximum dimensions of the screen
		if self.right and self.player.positionx < (1160-self.player.width):
			self.player.positionx += self.player_speed*dt
		if self.left and self.player.positionx > 0:
			self.player.positionx -= self.player_speed*dt

	#continuously creates and appends a new "space.jpg" image when the previous image leaves the screen
	def update_background(self,dt):
		for bg in self.background_list:
			bg.update(dt)
			if bg.positiony <= -1300:
				self.background_list.remove(bg)
				self.background_list.append(Objects(0,1000,Sprite(self.background_image)))
			bg.velocityy = -150

	#moves the "space.jpg" image to imitate a shaking screen
	def screen_shake(self):
		self.background_list[0].positionx = 10
		self.background_list[1].positionx = 10
		self.background_list[0].positionx = -10
		self.background_list[1].positionx = -10

	#returns the image to its original position
	def screen_back(self,dt):
		self.counter -= 0.2
		if self.counter <= 0:
			self.background_list[0].positionx = 0
			self.background_list[1].positionx = 0
			self.counter = 1

	#called when spawning the asteroids
	def asteroid_1(self,velocity):
		self.asteroid_list.append(Sprite(self.asteroid1_anim, x=randint(0,1160-128), y=800, batch=self.batch))
		self.asteroid_list[-1].speed = velocity

	def asteroid_2(self,velocity):
		self.asteroid_list.append(Sprite(self.asteroid2_anim, x=randint(0,1160-72), y=800, batch=self.batch))
		self.asteroid_list[-1].speed = velocity

	def asteroid_3(self,velocity):
		self.asteroid_list.append(Sprite(self.asteroid3_anim, x=randint(0,1160-250),y=800, batch=self.batch))
		self.asteroid_list[-1].speed = velocity

	def asteroid_4(self,velocity):
		self.asteroid_list.append(Sprite(self.asteroid4_anim, x=randint(0,1160-250),y=800, batch=self.batch))
		self.asteroid_list[-1].speed = velocity

	def asteroid_5(self,velocity):
		self.asteroid_list.append(Sprite(self.asteroid5_anim, x=randint(0,1160-220),y=800, batch=self.batch))
		self.asteroid_list[-1].speed = velocity

	#called when spawning the orbs
	def orbs_1(self,velocity):
		self.orbs_list.append(Sprite(self.orbs1_anim, x=randint(0,1160-50),y=750, batch=self.batch))
		self.orbs_list[-1].speed = velocity
		self.orbs_list[-1].type = 1

	def orbs_2(self,velocity):
		self.orbs_list.append(Sprite(self.orbs2_anim, x=randint(0,1160-50),y=750, batch=self.batch))
		self.orbs_list[-1].speed = velocity
		self.orbs_list[-1].type = 2

	def orbs_3(self,velocity):
		self.orbs_list.append(Sprite(self.orbs3_anim, x=randint(0,1160-50),y=750, batch=self.batch))
		self.orbs_list[-1].speed = velocity
		self.orbs_list[-1].type = 3

	def orbs_4(self,velocity):
		self.orbs_list.append(Sprite(self.orbs4_anim, x=randint(0,1160-50),y=750, batch=self.batch))
		self.orbs_list[-1].speed = velocity
		self.orbs_list[-1].type = 4

	def orbs_5(self,velocity):
		self.orbs_list.append(Sprite(self.orbs5_anim, x=randint(0,1160-50),y=750, batch=self.batch))
		self.orbs_list[-1].speed = velocity
		self.orbs_list[-1].type = 5

	#creates a new asteroid every time asteroid_spawner hits 0
	def asteroid_spawn(self,dt):
		if self.player_present:
			self.asteroid1_spawner -=0.05
			self.asteroid2_spawner -=0.05
			self.asteroid3_spawner -=0.05
			self.asteroid4_spawner -=0.05
			self.asteroid5_spawner -=0.05

			#increases the number of asteroids spawned every 20 points scored
			if int(self.score) <= 200:
				self.difficulty = (int(self.score) // 20)*50

			if int(self.score) % 1 == 0 and self.asteroid1_spawner <=0:
				for i in range(0,self.difficulty+50,50):
					self.asteroid_1(200+i)
				self.asteroid1_spawner = 5

			if int(self.score) % 5 == 0 and self.asteroid2_spawner <=0:
				for i in range(0,self.difficulty+50,50):
					self.asteroid_2(350+i)
				self.asteroid2_spawner = 3

			if int(self.score) % 11 == 0 and self.asteroid3_spawner <=0:
				for i in range(0,self.difficulty+50,100):
					self.asteroid_3(300+i/2)
				self.asteroid3_spawner = 10

			if int(self.score) % 23 == 0 and self.asteroid4_spawner<=0:
				for i in range(0,self.difficulty+50,100):
					self.asteroid_4(400+i/2)
				self.asteroid4_spawner = 15

			if int(self.score) % 49 == 0 and self.asteroid5_spawner <=0:
				for i in range(0,self.difficulty+50,200):
					self.asteroid_5(250)
				self.asteroid5_spawner = 20

			

	#updates the position of the asteroids
	def update_asteroid(self,asteroid_list,dt):
		for asteroid in self.asteroid_list:
			asteroid.y -= asteroid.speed*dt
			if asteroid.y <= -200:
				asteroid_list.remove(asteroid)

	#creates a new orb every time orbs_spawner hits 0
	def orbs_spawn(self,dt):
		if self.player_present:
			self.orbs1_spawner -= 0.05
			self.orbs2_spawner -= 0.05
			self.orbs3_spawner -= 0.05
			self.orbs4_spawner -= 0.05
			self.orbs5_spawner -= 0.05
			if int(self.score) % 10 == 0:
				if self.orbs1_spawner <= 0:
					self.orbs_1(350)
					self.orbs1_spawner = 10
			if int(self.score) % 110 == 0 and not self.orbs5_press and not self.orbs5_effect:
				if self.orbs5_spawner <= 0:
					self.orbs_5(350)
					self.orbs5_spawner = 110
			elif int(self.score) % 75 == 0 and not self.orbs4_press:
				if self.orbs4_spawner <= 0:
					self.orbs_4(350)
					self.orbs4_spawner = 75
			elif int(self.score) % 50 == 0 and not self.orbs3_press:
				if self.orbs3_spawner <= 0:
					self.orbs_3(350)
					self.orbs3_spawner = 50
			elif int(self.score) % 30 == 0 and not self.orbs2_press and not self.orbs2_effect:
				if self.orbs2_spawner <= 0:
					self.orbs_2(350)
					self.orbs2_spawner = 30

	#updates the position of the orbs
	def update_orbs(self,orbs_list,dt):
		for orb in self.orbs_list:
			orb.y -= orb.speed*dt
			if orb.y <= -200:
				orbs_list.remove(orb)

	#evaluates if the player hits an object
	def object_hit(self,player,item_list,score,dt):
		#loops to find the object that hits the player
		for item in item_list:
			#for orbs
			if item.width <= 50:
				if item.x < (self.player.positionx + self.player.width-20) and (item.x + item.width-20) > self.player.positionx and item.y < (self.player.positiony + self.player.height-20) and (item.y + item.height-20) > self.player.positiony:
					if item.type == 1:
						self.score += 5
						if self.orbs2_effect:
							self.additional = 5

					elif item.type == 2:
						self.duration = 50
						self.orbs2_effect_num.text = str(self.duration)
						self.orbs2_press = True
						

					elif item.type == 3:
						self.orbs3_effect_bool.text = str(True)
						self.orbs3_press = True

					elif item.type == 4:
						self.orbs4_effect_bool.text = str(True)
						self.orbs4_press = True

					elif item.type == 5:
						self.orbs5_multiplier += 1
						self.invulnerable = 10*self.orbs5_multiplier
						self.orbs5_effect_num.text = str(self.invulnerable)
						self.orbs5_press = True
						
					#plays a sound when an orb is acquired and delete the orb
					self.orb_acquired_sound.play()
					item_list.remove(item)
					item.delete()

			#for asteroids
			elif item.width > 50:
				#includes asteroid1, asteroid2
				if 50 < item.width <= 150:
					if item.x < (self.player.positionx + self.player.width-55) and (item.x + item.width-50) > self.player.positionx and item.y < (self.player.positiony + self.player.height-50) and (item.y + item.height-50) > self.player.positiony:
						self.object_hit_asteroid(self.player,self.asteroid_list,item,dt)

				#includes asteroid3, asteroid4, asteroid5
				elif 150 < item.width <= 300:
					if item.x < (self.player.positionx + self.player.width-85) and (item.x + item.width-80) > self.player.positionx and item.y < (self.player.positiony + self.player.height-80) and (item.y + item.height-80) > self.player.positiony:
						self.object_hit_asteroid(self.player,self.asteroid_list,item,dt)

	#when the player hits an object
	def object_hit_asteroid(self,player,item_list,item,dt):
		self.player_life -= 1
		self.lives_left_num.text = str(int(self.player_life))
		item_list.remove(item)
		item.delete()
		self.screen_shake_sound.play()
		self.screen_shake()
		self.screen_back(dt)
		if self.player_life <= 0:
			self.player_present = False
			self.game_over()

	#called when the player loses his/her last life
	def game_over(self):
		self.player_lives = False
		self.reloading = True
		if int(self.score) > int(self.hscore):
			save("highscore.txt", int(self.score))

	#resets all variables back to their original state
	def reload(self):
		self.score = 0
		self.player_life = 3
		self.counter = 1
		self.asteroid1_spawner = 5
		self.asteroid2_spawner = 5
		self.asteroid3_spawner = 5
		self.asteroid4_spawner = 5
		self.asteroid5_spawner = 5
		self.superpower = True
		self.superpower_activated = False
		self.superpower_activated_counter = 1
		self.orbs1_spawner = 10
		self.orbs2_spawner = 30
		self.orbs3_spawner = 50
		self.orbs4_spawner = 75
		self.orbs5_spawner = 110
		self.orbs2_press = False
		self.orbs3_press = False
		self.orbs4_press = False
		self.orbs5_press = False
		self.orbs2_effect = False
		self.orbs5_effect = False
		self.orbs5_multiplier = 0
		self.additional = 0
		self.invulnerable = 0
		self.player_present = True
		self.start = True
		self.player_lives = True

		self.player.positionx = 500
		self.player.positiony = 100

		#deletes all the elements of the asteroid and orbs list
		for obj in self.asteroid_list:
			obj.batch = None
		for obj in self.orbs_list:
			obj.batch = None
		self.asteroid_list.clear()
		self.orbs_list.clear()

	#score increases wrt time
	def update_score(self,multiplier,dt):
		if self.player_present:
			#when orbs5 is activated
			if self.invulnerable > 0 and self.orbs5_effect:
				self.invulnerable -= dt
				self.orbs5_effect_num.text = str(int(self.invulnerable))
			else:
				self.orbs5_effect = False

			#when orbs2 is not activated
			if multiplier == 1:
				self.score+= (multiplier*dt)
				self.curr_score.text = str(int(self.score))

			#when orbs2 is activated
			if multiplier == 2:
				self.score+= (multiplier*dt)
				if self.additional == 0:
					self.duration -= (multiplier*dt)
				else:
					self.duration -= self.additional
					self.additional = 0
				self.orbs2_effect_num.text = str(int(self.duration))
				self.curr_score.text = str(int(self.score))
				if int(self.score) >= self.future:
					self.orbs2_effect = False
					self.update(dt)
			
			#saves the high score	
			if int(self.score) > int(self.hscore):
				save("highscore.txt", int(self.score))
				self.hscore = load("highscore.txt")
				self.hscore_num = pyglet.text.Label(self.hscore, x=1035, y=500)
				self.hscore_num.color = (255,100,100,100)
				self.hscore_num.font_size = 18
				self.hscore_num.draw()
		
	#updates the objects/sprites wrt time
	def update(self,dt):
		self.update_player(dt)
		self.update_asteroid(self.asteroid_list,dt)
		self.update_orbs(self.orbs_list,dt)
		#continuously checks if the player is in contact with an object
		if not self.orbs5_effect:
			for obj in self.asteroid_list:
				self.object_hit(self.player,self.asteroid_list,self.score,dt)
		for obj in self.orbs_list:
			self.object_hit(self.player,self.orbs_list,self.score,dt)
		self.asteroid_spawn(dt)
		self.orbs_spawn(dt)
		self.update_background(dt)
		if not self.orbs2_effect:
			self.update_score(1,dt)
		else:
			self.update_score(2,dt)
		self.screen_back(dt)
		#for counting down to when the "SUPERPOWER ACTIVATED!" will be present
		if self.superpower_activated:
			self.superpower_activated_counter -= dt
			if self.superpower_activated_counter <= 0:
				self.superpower_activated = False


window = Window(1160, 690, "Askal the Astronaut", resizable=False)
pyglet.clock.schedule_interval(window.update, window.frame_rate)
pyglet.app.run()
