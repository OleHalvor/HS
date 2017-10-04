from cards import Card, Minion, Spell
from deck import Deck
from player import Player
from game import Game
import copy




fireball = Spell("Fireball",4)
fireball.addDamageOne(6,False)
fireball.addDescription("Deal 6 damage")

flamestrike = Spell("Flamestrike",7)
flamestrike.addDamageEnemyAOE(4,False)
flamestrike.addDescription("Deal 4 damage to all enemy minions")

concecration = Spell("Concecration",4)
concecration.addDamageEnemyAOE(2,True)
concecration.addDescription("Deal 4 damage to all enemy characters")

footman = Minion("Goldshire Footman",1,1,2)
footman.giveTaunt()

selv = Minion("Selvskader",1,1,1)
def selvskad(activePlayer,passivePlayer):
	activePlayer.health = activePlayer.health - 5
selv.setBattlecry(selvskad)

munk = Minion("Munken",1,1,1)
def skad5(activePlayer,passivePlayer):
	passivePlayer.damageMinionOrHero(5)
munk.setBattlecry(skad5)

bjarne = Minion("Bjarne",2,1,2)
flowerGirl =Minion("FlowerGirl",1,1,3)
yeti = Minion("Yeti",4,4,5)


swipe = Spell("Swipe",4)
swipe.addDamageOne(3,False)
swipe.addDamageEnemyAOE(1,False)
swipe.addDescription("Deal 3 damage to one target, deal 1 damage to all enemies")

darkBomb = Spell("DarkBomb",2)
darkBomb.addDamageOne(3,False)
darkBomb.addDescription("Deal 3 damage to one target")

wildPyro = Minion("Wild Pyromancer",1,3,2)
def wildPyroEffect(game):
	for minion in game.activePlayer.activeMinions:
		minion.damage(1)
	for minion in game.passivePlayer.activeMinions:
		minion.damage(1)
	print("Wild Pyromancer did 1 AOE damage to the board")
wildPyro.setOnSpellOwnRound(wildPyroEffect)


def generalHeal(target,amount):
	target.heal(amount)

superHeal = Spell("SuperHeal",1)
def heal10(game):
	game.activePlayer.heal(10)
superHeal.setEffect(heal10)
superHeal.addDescription("Heals player 10HP")

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
	




deck1 = Deck("deck 1")
deck1.addCard(copy.deepcopy(fireball))
deck1.addCard(fireball)
deck1.addCard(concecration)
deck1.addCard(flamestrike)
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(footman))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(swipe)
deck1.addCard(copy.deepcopy(yeti))
deck1.addCard(copy.deepcopy(bjarne))
deck1.addCard(copy.deepcopy(flowerGirl))
deck1.addCard(swipe)
deck1.addCard(swipe)
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

