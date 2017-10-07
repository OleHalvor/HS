import random
import copy
class Deck:

	def __init__(self,name):
		self.name = name
		self.cards = []
		self.owner = None

	def setOwner(self,owner):
		self.owner = owner

	def addCard(self,card):
		self.cards.append(copy.deepcopy(card))

	def getRemaining(self):
		return len(self.cards)

	def draw(self):
		return self.cards.pop()

	def shuffle(self):
		if self.owner.game.printing:
			print(self.name,"has been shuffled")
		random.shuffle(self.cards)
		


# from cards import Card, Minion

# minDeck = Deck("SuperDeck")

# # minDeck.addCard(Minion("Gunnar",7,8,9))
# # minDeck.addCard(Minion("Rolf",7,8,9))
# # minDeck.addCard(Minion("Bjarne",2,1,3))


# # print ( minDeck.draw())
# # print ( minDeck.draw())