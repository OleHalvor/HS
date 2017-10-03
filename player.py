class Player:

	def __init__(self,name,deck):
		self.name = name
		self.maxHealth = 20
		self.health = 20
		self.deck = deck
		self.hand = []
		self.activeMinions = []
		self.maxMana = 1
		self.currentMana = 1

	def updateActiveHealth(self,minionPosition,newHealth):
		self.activeMinions[int(minionPosition)].setHealth(newHealth)

	def heal(self,amount):
		self.health += amount
		if self.health > self.maxHealth:
			self.health = self.maxHealth



	def getHand(self):
		return self.hand

	def getHealth(self):
		return self.health

	def changeDeck(self,newDeck):
		self.deck = newDeck

	def reduceHealth(self,damage):
		self.health = self.health - damage

	def getActiveMinions(self):
		return self.activeMinions

	def doAction(self):
		pass




	def attack(self,minion,target):
		pass



	def getDeck(self):
		return self.deck

	def __str__(self):
		return self.name

	def getName(self):
		return self.name
