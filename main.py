from cards import Card, Minion, Spell
from deck import Deck
from player import Player
from game import Game
import copy

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
def skad5(game):
	game.passivePlayer.damageMinionOrHero(5)
munk.setBattlecry(skad5)
munk.addDescription("Deal 5 damage")
#This creates a minion witch cost 1, has 1 attack and 1 health, and deals 5 damage when played. What you define in the function you place in setBattlecry() will be run when the minion is played. Always take game as argument. this contains all the information about the game state.

#Spells are created similarly to minion, but without attack and health.
#The function you place in setEffect() will be run when the spell is cast.

superHeal = Spell("SuperHeal",1)
def heal10(game):
	game.activePlayer.heal(10)
superHeal.setEffect(heal10)
superHeal.addDescription("Heals player 10HP") #Descriptions are used to inform players about the effects of a card.

bok = Spell("Blessing of kings",4)
bok.addDescription("+4/+4 buff")
def bokEffect(game):
	if len(game.activePlayer.activeMinions)==0:
		print("You have no minions to buff!")
	elif game.activePlayer.AI==False:
		target = int(input("Which minion do you want to buff?"))
		if target < len(game.activePlayer.activeMinions):
			game.activePlayer.activeMinions[int(target)].buff(4,4)
		else:
			print("Invalid target")
	else:
		if (len(game.activePlayer.activeMinions))>0:
			game.activePlayer.activeMinions[randint(0,len(game.activePlayer.activeMinions))]
bok.setEffect(bokEffect)

footman = Minion("Goldshire Footman",1,1,2)
footman.giveTaunt()

selv = Minion("Selvskader",1,1,1)
def selvskad(game):
	game.activePlayer.health = game.activePlayer.health - 5
selv.setBattlecry(selvskad)




flowerGirl =Minion("FlowerGirl",1,1,3)
yeti = Minion("Yeti",4,4,5)


wildPyro = Minion("Wild Pyromancer",1,3,2)
def wildPyroEffect(game):
	for minion in game.activePlayer.activeMinions:
		minion.damage(1)
	for minion in game.passivePlayer.activeMinions:
		minion.damage(1)
	print("Wild Pyromancer did 1 AOE damage to the board")
wildPyro.setOnSpellOwnRound(wildPyroEffect)


	
dataVirus = Minion("Datavirus",2,2,2)
def frysTreFiender(game):
	numberOfEnemies = len(game.passivePlayer.activeMinions)
	if numberOfEnemies == 0:
		pass
	elif numberOfEnemies ==1:
		game.passivePlayer.activeMinions[0].freeze(2)
	elif numberOfEnemies == 2:
		game.passivePlayer.activeMinions[0].freeze(2)
		game.passivePlayer.activeMinions[1].freeze(2)
	elif numberOfEnemies == 3:
		game.passivePlayer.activeMinions[0].freeze(2)
		game.passivePlayer.activeMinions[1].freeze(2)
		game.passivePlayer.activeMinions[2].freeze(2)
	else:
		toBeFrozen = numberOfEnemies.pop(randint(numberOfEnemies-1))
		toBeFrozen2 = numberOfEnemies.pop(randint(numberOfEnemies-2))
		toBeFrozen3 = numberOfEnemies.pop(randint(numberOfEnemies-3))
		game.passivePlayer.activeMinions[toBeFrozen].freeze(2)
		game.passivePlayer.activeMinions[toBeFrozen2].freeze(2)
		game.passivePlayer.activeMinions[toBeFrozen3].freeze(2)
dataVirus.setBattlecry(frysTreFiender)
dataVirus.addDescription("Freezes three random enemy minions")


#The following spells use the old way of defining spells, will be removed
fireball = Spell("Fireball",4)
fireball.addDamageOne(6,False)
fireball.addDescription("Deal 6 damage")

flamestrike = Spell("Flamestrike",7)
flamestrike.addDamageEnemyAOE(4,False)
flamestrike.addDescription("Deal 4 damage to all enemy minions")

concecration = Spell("Concecration",4)
concecration.addDamageEnemyAOE(2,True)
concecration.addDescription("Deal 2 damage to all enemy characters")

swipe = Spell("Swipe",4)
swipe.addDamageOne(3,False)
swipe.addDamageEnemyAOE(1,False)
swipe.addDescription("Deal 3 damage to one target, deal 1 damage to all enemies")

darkBomb = Spell("DarkBomb",2)
darkBomb.addDamageOne(3,False)
darkBomb.addDescription("Deal 3 damage to one target")



frostbolt = Spell("FrostBolt",2)
frostbolt.addDescription("Deal 3 damage and freeze target")
def frostBoltEffect(game):
	if game.activePlayer.AI==False:
		target = input("Choose target ('f' for face): ")
		if target =='f':
			game.passivePlayer.reduceHealth(3)
		else:
			game.passivePlayer.activeMinions[int(target)].damage(3)
			game.passivePlayer.activeMinions[int(target)].freeze(2)
	else:
		targetMinions = game.passivePlayer.activeMinions
		if len(targetMinions)>0:
			target = targetMinions[randint(0,len(targetMinions))]
			target.damage(3)
			target.freeze(2)
			print("Frostbolt hit target",target.name)
		else:
			print("Frostbolt hit face")
			game.passivePlayer.reduceHealth(3)
frostbolt.setEffect(frostBoltEffect)






#copy.deepcopy no longer needed

deck1 = Deck("deck 1")
deck1.addCard(frostbolt)
deck1.addCard(frostbolt)
deck1.addCard(frostbolt)
deck1.addCard(frostbolt)
deck1.addCard(copy.deepcopy(fireball))
deck1.addCard(copy.deepcopy(fireball))
deck1.addCard(copy.deepcopy(concecration))
deck1.addCard(copy.deepcopy(flamestrike))
deck1.addCard(copy.deepcopy(dataVirus))
deck1.addCard(copy.deepcopy(dataVirus))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(copy.deepcopy(swipe))
deck1.addCard(copy.deepcopy(yeti))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(copy.deepcopy(flowerGirl))
deck1.addCard(copy.deepcopy(swipe))
deck1.addCard(copy.deepcopy(swipe))
deck1.addCard(copy.deepcopy(wildPyro))
deck1.addCard(copy.deepcopy(wildPyro))
deck1.addCard(copy.deepcopy(darkBomb))
deck1.addCard(copy.deepcopy(darkBomb))
deck1.addCard(copy.deepcopy(munk))
deck1.addCard(copy.deepcopy(munk))
deck1.addCard(copy.deepcopy(superHeal))
deck1.addCard(copy.deepcopy(superHeal))
deck1.addCard(copy.deepcopy(bok))
deck1.addCard(copy.deepcopy(bok))





deck2 = copy.deepcopy(deck1)


player1 = Player("Player one",deck1)
player2 = Player("Player two",deck2)
player2.AI=True

game = Game(player1,player2)
game.start()

