from cards import Card, Minion, Spell
from deck import Deck
from player import Player
from game import Game




fireball = Spell("Fireball",1)
fireball.addDamageOne(6,False)
fireball.addDescription("Deal 6 damage")

flamestrike = Spell("Flamestrike",1)
flamestrike.addDamageEnemyAOE(4,False)
flamestrike.addDescription("Deal 4 damage to all enemy minions")

concecration = Spell("Concecration",2)
concecration.addDamageEnemyAOE(4,True)
concecration.addDescription("Deal 4 damage to all enemy characters")

footman = Minion("Goldshire Footman",1,1,2)
footman.giveTaunt()

selv = Minion("Selvskader",1,1,1)
def selvskad(activePlayer,passivePlayer):
	activePlayer.health = activePlayer.health - 5
selv.setBattlecry(selvskad)




deck1 = Deck("deck 1")
deck1.addCard(Minion("Kort1",1,2,3))
deck1.addCard(Minion("Kort2",2,3,5))
deck1.addCard(fireball)
deck1.addCard(Minion("Kort3",3,4,6))
deck1.addCard(Minion("Kort13",3,1,9))
deck1.addCard(Minion("Kort5",2,3,5))
deck1.addCard(Minion("Kort6",3,4,6))
deck1.addCard(fireball)
deck1.addCard(concecration)
deck1.addCard(Minion("Kort4",1,2,3))
deck1.addCard(flamestrike)
deck1.addCard(footman)
deck1.addCard(Minion("Kort7",1,2,3))
deck1.addCard(Minion("Kort8",1,7,3))
deck1.addCard(Minion("Kort9",1,6,3))
deck1.addCard(Minion("Kort10",1,2,9))
deck1.addCard(Minion("Kort11",1,7,3))
deck1.addCard(Minion("Kort12",1,6,3))
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)
deck1.addCard(selv)


deck2 = Deck("deck 2")
deck2.addCard(Minion("Kort1",1,2,3))
deck2.addCard(Minion("Kort2",2,3,5))
deck2.addCard(fireball)
deck2.addCard(Minion("Kort3",3,4,6))
deck2.addCard(Minion("Kort13",3,1,9))
deck2.addCard(Minion("Kort5",2,3,5))
deck2.addCard(Minion("Kort6",3,4,6))
deck2.addCard(fireball)
deck2.addCard(concecration)
deck2.addCard(Minion("Kort4",1,2,3))
deck2.addCard(flamestrike)
deck2.addCard(footman)
deck2.addCard(Minion("Kort7",1,2,3))
deck2.addCard(Minion("Kort8",1,7,3))
deck2.addCard(Minion("Kort9",1,6,3))
deck2.addCard(Minion("Kort10",1,2,9))
deck2.addCard(Minion("Kort11",1,7,3))
deck2.addCard(Minion("Kort12",1,6,3))
player1 = Player("Player one",deck1)
player2 = Player("Player two",deck2)

game = Game(player1,player2)
game.start()

