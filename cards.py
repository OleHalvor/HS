class Card:

	def __init__(self, name, type, cost):
		self.type = type
		self.cost = cost
		self.name = name

	def getType(self):
		return self.type

	def getCost(self):
		return self.cost

	def getName(self):
		return self.name

	def __str__(self):
		return self.name

class Minion(Card):
	def __init__(self, name, cost, attack, health):
		Card.__init__(self,name,"Minion",cost)
		self.defalutHealth = health
		self.defaultAttack = attack
		self.currentHealth = health
		self.currentAttack = attack
		self.hasAttacked = True
		self.frozenRounds = 0
		self.hasCharge = False
		self.hasTaunt = False
		def start(activePlayer,passivePlayer):
			pass
		self.onRoundStart = start

	def giveTaunt(self):
		self.hasTaunt = True

	def attacked(self):
		self.hasAttacked = True

	def readyToAttack(self):
		self.hasAttacked = False

	def freeze(self,rounds):
		self.frozenRounds += rounds

	def freezeTick(self):
		self.frozenRounds = self.frozenRounds -1
		if self.frozenRounds <0:
			self.frozenRounds = 0

	def unFreeze(self):
		self.frozenRounds = 0

	def getHealth(self):
		return self.currentHealth

	def getAttack(self):
		return self.currentAttack

	def damage(self,damage):
		self.currentHealth = self.currentHealth - damage

	def setHealth(self,newHealth):
		self.health = newHealth

class Spell(Card):
	def __init__(self,name,cost):
		Card.__init__(self,name,"Spell",cost)
		self.damageOne=[0,False] # first value is damage, second is if the target is random
		self.damageEnemyAOE=[0,False] #First value is damage, second is if the spell also hits face
		self.description = ''


	def addDamageOne(self,amount,rng):
		self.damageOne=[amount,rng]

	def addDamageEnemyAOE(self,amount,face):
		self.damageEnemyAOE=[amount,face]

	def addDescription(self,desc):
		self.description = desc

	def getDescription(self):
		return self.description



'''
Alle spell efects kan ha argumentet RNG for å velge om det er random target innenfor de mulige
Fireball = Spell("fireball",4)
fireball.addDamageOne(4,False)

Flamestrike = Spell("pyroblast",7)
Flamestrike.addEnemyAOE(4,False)

swipe = Spell("Swipe",4)
swipe.addDirectDamage(4,False)
swipe.addEnemyAOE(1,False)



# deck = []
Damage
	Minion
	minions
	face
	minion or face
heal
	Minion
	face
	minion or face
Freeze

eksempler:
Skad 4 på hva du vil
Skad 4 på alle fientlige minions
skad 4 på alle minions
skad 4 på alle fientlige minions og fiendes face
skad 4 på alle minion of faces

Skad 4 på én og 2 på de ved siden av

damageOneMinion(damage,position)
damageMultipleMinions(d1,m1,d2,m2,d3,m2)
damageAllEnemyMinions(damage)
DamageFace(damage)
Draw()


'''
