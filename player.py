import copy
import random
class Player:

	def __init__(self,name,deck):
		self.name = name
		self.maxHealth = 15
		self.health = 15
		self.deck = deck
		self.hand = []
		self.activeMinions = []
		self.maxMana = 1
		self.currentMana = 1
		self.AI=False
		self.IP='127.0.0.1'
		self.connection = ''


	def setIpAndPort(ip,port):
		self.IP = ip 
		self.PORT = port

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

	def damageMinionOrHero(self,amount):
		# If nettverk: få target fra nett
		if not self.AI: #A bit counter intuitive as of now. not self.AI actually means self = AI...
			if len(self.activeMinions)<=0:
				index ="f"
				
			else:
				index = random.randint(0,len(self.activeMinions)-1)
				
		else:
			index = input("Hvilken minion vil du skade? ('f' for face): ")
		if index=="f":
			self.health = self.health - amount
			print("Something did",amount,"damage to face")
		else:
			self.activeMinions[int(index)].damage(amount)
			print("Something did",amount,"damage to minion #",index)

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
