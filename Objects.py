import pyglet


class Objects:
	def __init__(self, positionx, positiony, sprite=None):

		#provides attributes to the Objects class
		self.positionx = positionx
		self.positiony = positiony
		self.velocityx = 0
		self.velocityy = 0
		#sets the sprite attributes only if the sprite is visible
		if sprite is not None:
			self.sprite = sprite
			self.sprite.x = self.positionx
			self.sprite.y = self.positiony
			self.width = self.sprite.width
			self.height = self.sprite.height
	
	#defines a draw method for the objects to be used in the main file
	#when calling sprites, only uses self.[object].draw instead of self.[object].sprite.draw
	def draw(self):
		self.sprite.draw()

	#defines an update method for the objects
	def update(self,dt):
		#updates the object's position wrt time
		self.positionx += self.velocityx*dt
		self.positiony += self.velocityy*dt
		#sets the sprites position wrt the position of the object
		self.sprite.x = self.positionx
		self.sprite.y = self.positiony