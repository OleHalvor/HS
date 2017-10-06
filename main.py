from cards import Card, Minion, Spell
from deck import Deck
from player import Player
from game import Game
import copy
import random

#This is the main file of the game, i.e. this is the file you run.
#This is also the file where you define cards, decks and players

#This is an example of a basic minion:
#Variable name doesn't matter. 
#The first argument is the name of the card
#The second argument is the mana cost
#The third argument is the attack value
#The fourth argumen is the health value
bjarne = Minion("Bjarne",2,1,2)

#If you wish to add a battlecry this is the way:
munk = Minion("Munken",1,1,1)
def skad5(game,minion):
	game.passivePlayer.damageMinionOrHero(5)
munk.setBattlecry(skad5)
munk.setDescription("Deal 5 damage")
#This creates a minion witch cost 1, has 1 attack and 1 health, and deals 5 damage when played. What you define in the function you place in setBattlecry() will be run when the minion is played. Always take game as argument. this contains all the information about the game state.

#Spells are created similarly to minion, but without attack and health.
#The function you place in setEffect() will be run when the spell is cast.

superHeal = Spell("SuperHeal",1)
def heal10(game):
	game.activePlayer.heal(10)
superHeal.setEffect(heal10)
superHeal.setDescription("Heals player 10HP") #Descriptions are used to inform players about the effects of a card.

bok = Spell("Blessing of kings",4)
bok.setDescription("+4/+4 buff")
def bokEffect(game):
	if len(game.activePlayer.activeMinions)==0:
		print("You have no minions to buff!")
	else:
		if game.activePlayer.AI==False:
			target = int(input("Which minion do you want to buff?"))
			if target < len(game.activePlayer.activeMinions):
				game.activePlayer.activeMinions[int(target)].buff(4,4)
			else:
				print("Invalid target")
		else:
			if (len(game.activePlayer.activeMinions))>0:
				targeT=random.randint(0,len(game.activePlayer.activeMinions)-1)
				# print("AI BOK TARGET",targeT)
				game.activePlayer.activeMinions[targeT].buff(4,4)
bok.setEffect(bokEffect)
bok.setTargetOwnMinions(True)

footman = Minion("Goldshire Footman",1,1,2)
footman.setTaunt(True)

selv = Minion("Selvskader",1,1,1)
def selvskad(game,minion):
	game.activePlayer.health = game.activePlayer.health - 5
selv.setBattlecry(selvskad)

kultFolger = Minion("Kult-følger",2,4,1)
def kultFolgerBC(game,minion):
	friendlyMinions = minion.owner.activeMinions
	if len(friendlyMinions)>1: #needs to count from 1 because he is present himself
		if minion.owner.AI==False:
			target = input("Which minion will you sacrifice?: ")
			minion.owner.activeMinions[int(target)].currentHealth=0
			minion.setCharge(True)
		else:
			target = 0
			minion.owner.activeMinions[int(target)].currentHealth=0
			minion.setCharge(True)
kultFolger.setBattlecry(kultFolgerBC)

stromGjerde = Minion("Strømgjerde",7,2,9)
stromGjerde.setTaunt(True)


fulgeskremsel = Minion("Fulgeskremsel",3,1,5)
def fulgreskremselEffect(game,minion):
	if game.passivePlayer==minion.owner:
		minion.currentAttack = minion.maxAttack + 2
	else:
		minion.currentAttack = minion.maxAttack
fulgeskremsel.setTaunt(True)
fulgeskremsel.setContinousEffect(fulgreskremselEffect)

hermeGaas = Minion("Hermegås",4,0,4)
def hermeGaasEffect(game,minion):
	highestAttack = 0
	minion.currentAttack = 0
	for minionTemp in game.activePlayer.activeMinions:
		if minionTemp.currentAttack > highestAttack:
			highestAttack = minionTemp.currentAttack
	for minionTemp in game.passivePlayer.activeMinions:
		if minionTemp.currentAttack > highestAttack:
			highestAttack = minionTemp.currentAttack
	minion.currentAttack = highestAttack
hermeGaas.setContinousEffect(hermeGaasEffect)
hermeGaas.setDescription("Attack always = attack of strongest minion on board")




flowerGirl =Minion("FlowerGirl",1,1,3)
yeti = Minion("Yeti",4,4,5)


wildPyro = Minion("Wild Pyromancer",2,3,2)
def wildPyroEffect(game):
	for minion in game.activePlayer.activeMinions:
		minion.damage(1)
	for minion in game.passivePlayer.activeMinions:
		minion.damage(1)
	print("Wild Pyromancer did 1 AOE damage to the board")
wildPyro.setOnSpellOwnRound(wildPyroEffect)
wildPyro.setDescription("1 AOE damage when you cast a spell")


juksePave = Minion("Juksepave",2,3,3)
def juksePaveFunc(game,minion):
	# heal = input("Who do you want to heal 5?")
	# if heal=="f":
	# 	pass
	# else:
	# 	pass
	game.titt(game.activePlayer,4)
juksePave.setBattlecry(juksePaveFunc)
juksePave.setDescription("Look at the next 4 cards in the deck")



dataVirus = Minion("Datavirus",2,2,2)
def frysTreFiender(game,minion):
	numberOfEnemies = len(game.passivePlayer.activeMinions)
	if numberOfEnemies == 0:
		pass
	elif numberOfEnemies ==1:
		game.passivePlayer.activeMinions[0].freeze(1)
	elif numberOfEnemies == 2:
		game.passivePlayer.activeMinions[0].freeze(1)
		game.passivePlayer.activeMinions[1].freeze(1)
	elif numberOfEnemies == 3:
		game.passivePlayer.activeMinions[0].freeze(1)
		game.passivePlayer.activeMinions[1].freeze(1)
		game.passivePlayer.activeMinions[2].freeze(1)
	else:
		toBeFrozen = numberOfEnemies.pop(random.randint(numberOfEnemies-1))
		toBeFrozen2 = numberOfEnemies.pop(random.randint(numberOfEnemies-2))
		toBeFrozen3 = numberOfEnemies.pop(random.randint(numberOfEnemies-3))
		game.passivePlayer.activeMinions[toBeFrozen].freeze(1)
		game.passivePlayer.activeMinions[toBeFrozen2].freeze(1)
		game.passivePlayer.activeMinions[toBeFrozen3].freeze(1)
dataVirus.setBattlecry(frysTreFiender)
dataVirus.setDescription("Freezes three random enemy minions")


#The following spells use the old way of defining spells, will be removed
fireball = Spell("Fireball",4)
fireball.addDamageOne(6,False)
fireball.setDescription("Deal 6 damage")

flamestrike = Spell("Flamestrike",7)
flamestrike.addDamageEnemyAOE(4,False)
flamestrike.setDescription("Deal 4 damage to all enemy minions")

concecration = Spell("Concecration",4)
concecration.addDamageEnemyAOE(2,True)
concecration.setDescription("Deal 2 damage to all enemy characters")

swipe = Spell("Swipe",4)
swipe.addDamageOne(3,False)
swipe.addDamageEnemyAOE(1,False)
swipe.setDescription("Deal 3 damage to one target, deal 1 damage to all enemies")

darkBomb = Spell("DarkBomb",2)
darkBomb.addDamageOne(3,False)
darkBomb.setDescription("Deal 3 damage to one target")



frostbolt = Spell("FrostBolt",2)
frostbolt.setDescription("Deal 3 damage and freeze target")
def frostBoltEffect(game):
	if game.activePlayer.AI==False:
		target = input("Choose target ('f' for face): ")
		if target =='f':
			game.passivePlayer.reduceHealth(3)
		else:
			game.passivePlayer.activeMinions[int(target)].damage(3)
			game.passivePlayer.activeMinions[int(target)].freeze(1)
	else:
		targetMinions = game.passivePlayer.activeMinions
		if len(targetMinions)>0:
			target = targetMinions[random.randint(0,len(targetMinions)-1)]
			target.damage(3)
			target.freeze(1)
			# print("Frostbolt hit target",target.name)
		else:
			# print("Frostbolt hit face")
			game.passivePlayer.reduceHealth(3)
frostbolt.setEffect(frostBoltEffect)


coin = Spell("The Coin",0)
def coinEffect(game):
	game.activePlayer.currentMana += 1
coin.setEffect(coinEffect)



def boomBotFunc(game,minion):
	damage = random.randint(1,4)
	#Random 4 damage
	if minion.owner == game.activePlayer:
		player = 1
	else:
		player = 0
	if player==1:
		possibleTargets = game.passivePlayer.activeMinions
		target = random.randint(0,len(possibleTargets))
		if target == len(possibleTargets):
			game.passivePlayer.reduceHealth(damage)
			print("Boombot died and did",damage,"to",game.passivePlayer.name)
		else:
			game.passivePlayer.activeMinions[target].damage(damage)
			print("Boombot died and did",damage,"to",game.passivePlayer.activeMinions[target].name)
	elif player==0:
		possibleTargets = game.activePlayer.activeMinions
		target = random.randint(0,len(possibleTargets))
		if target == len(possibleTargets):
			game.activePlayer.reduceHealth(damage)
			print("Boombot died and did",damage,"to",game.activePlayer.name)
		else:
			game.activePlayer.activeMinions[target].damage(damage)
			print("Boombot died and did",damage,"to",game.activePlayer.activeMinions[target].name)

# Star med boombots uten DR
drBoom = Minion("Dr. Boom",7,7,7)
def boomFunc(game,minion): #Deathrattle
	print("Dr boom spawned two boombots for",minion.owner)
	boomBot0 = Minion("BoomBot",1,1,1)
	boomBot1 = Minion("BoomBot",1,1,1)
	boomBot0.setDeathRattle(boomBotFunc)
	boomBot1.setDeathRattle(boomBotFunc)
	game.summonMinion(boomBot0,minion.owner)
	game.summonMinion(boomBot1,minion.owner)
drBoom.setBattlecry(boomFunc)





#copy.deepcopy no longer needed

deck1 = Deck("deck 1")
deck1.addCard(frostbolt)
deck1.addCard(copy.deepcopy(fireball))
deck1.addCard(copy.deepcopy(concecration))
deck1.addCard(copy.deepcopy(flamestrike))
deck1.addCard(copy.deepcopy(dataVirus))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(copy.deepcopy(swipe))
deck1.addCard(copy.deepcopy(yeti))
deck1.addCard(copy.deepcopy(yeti))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(copy.deepcopy(flowerGirl))
deck1.addCard(copy.deepcopy(swipe))
deck1.addCard(copy.deepcopy(wildPyro))
deck1.addCard(copy.deepcopy(darkBomb))
deck1.addCard(copy.deepcopy(munk))
deck1.addCard(copy.deepcopy(superHeal))
deck1.addCard(copy.deepcopy(bok))
deck1.addCard(juksePave)
deck1.addCard(drBoom)
deck1.addCard(hermeGaas)
deck1.addCard(kultFolger)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)
deck1.addCard(fulgeskremsel)







deck2 = copy.deepcopy(deck1)


player1 = Player("Player one",deck1)
player2 = Player("Player two",deck2)
player2.AI=True

game = Game(player1,player2)
game.start()
# game.initialize(player1,player2)

