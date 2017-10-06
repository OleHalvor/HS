class Card:

	def __init__(self, name, type, cost):
		self.type = type
		self.cost = cost
		self.name = name
		self.description = ''


	def setDescription(self,desc):
		self.description = desc

	def getDescription(self):
		return self.description

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
		self.maxHealth = health
		self.maxAttack = attack
		self.hasAttacked = True
		self.frozenRounds = 0
		self.hasCharge = False
		self.hasTaunt = False
		self.onlyAbleToAttackMinions = False

		self.setDescription("")


		def contEffectF(game,minion):
			pass
		self.continousEffect = contEffectF

		def deathRattleF(game,minion):
			pass
		self.dr = deathRattleF
		def start(game):
			pass
		self.onRoundStart = start
		def battleCryF(game,minion):
			pass
		self.bc = battleCryF
		def onSpellCastF(game):
			pass
		self.onSpell = onSpellCastF
		def onSpellCastOwnRound(game,minion):
			pass
		self.onSpellOwnRound = onSpellCastOwnRound
		self.owner = None

		def afterAttackFunc(game,minion):
			pass
		self.afterAttack = afterAttackFunc

	def setAfterAttack(self,action):
		self.afterAttack = action

	def setOnlyAbleToAttackMinions(self,value):
		self.onlyAbleToAttackMinions=value

	def setCharge(self,value):
		self.hasCharge=value
		if value == True:
			self.hasAttacked = False

	def setContinousEffect(self,action):
		self.continousEffect = action

	def setDeathRattle(self,action):
		self.dr = action

	def buff(self,attack,health):
		self.maxHealth += health
		self.maxAttack += attack
		self.currentHealth += health
		self.currentAttack += attack

	def heal(self,amount):
		print(self.name,"was healed for",amount)
		self.currentHealth = self.currentHealth + amount
		if self.currentHealth > self.maxHealth:
			self.currentHealth = self.maxHealth

	def setOwner(self,player):
		self.owner = player

	def setOnSpellOwnRound(self,action):
		self.onSpellOwnRound = action

	def setOnSpellCast(self,action):
		self.onSpell = action

	def setBattlecry(self,action):
		self.bc = action

	def setTaunt(self,value):
		self.hasTaunt = value
		if value == True:
			self.description = "Taunt -" + self.description

	def attacked(self):
		self.hasAttacked = True

	def readyToAttack(self):
		self.hasAttacked = False

	def freeze(self,rounds):
		self.frozenRounds += rounds+1
		print(self.name,"has been frozen")
		

	def freezeTick(self):
		if self.frozenRounds == 1:
			print("{}'s {} is no longer frozen".format(self.owner.name, self.name))
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
		print(self.name,"received",damage,"damage")

	def setHealth(self,newHealth):
		self.health = newHealth

class Spell(Card):
	def __init__(self,name,cost):
		Card.__init__(self,name,"Spell",cost)
		self.damageOne=[0,False] # first value is damage, second is if the target is random
		self.damageEnemyAOE=[0,False] #First value is damage, second is if the spell also hits face
		def spellEffect(game):
			pass
		self.effect = spellEffect
		self.targetEnemyMinions = False
		self.targetOwnMinions = False

	def setEffect(self,effect):
		self.effect = effect

	def addDamageOne(self,amount,rng):
		self.damageOne=[amount,rng]

	def addDamageEnemyAOE(self,amount,face):
		self.damageEnemyAOE=[amount,face]

	def setTargetOwnMinions(self,value):
		self.targetOwnMinions = value




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
