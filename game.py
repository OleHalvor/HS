class Game:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.activePlayer = player1
		self.passivePlayer = player2
		self.turnCounter = 0
	def printPassiveHand(self):
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.passivePlayer.getHand()
		for i in range(len(cardsInHand)):
			line0+=" _____  "
			line1+="|     | "
			line2+="|     | "
			line3+="|     | "
			line4+="|_____| "
		print("\n*ENEMY*")
		if (len(cardsInHand)>0):
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)

	def printHand(self):
		# 8 kolonner per minion
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.activePlayer.getHand()
		for i in range(len(cardsInHand)):
			line0+=" _____  "
			line1+="|{}    | ".format(cardsInHand[i].cost)
			line2+="|     | "
			line3+="| {}/{} | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
			line4+="|_____| "
			line5+="   {}    ".format(i)

		if (len(cardsInHand)>0):
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)
		print("*YOU*\n   MANA: {}/{}".format(self.activePlayer.currentMana,self.activePlayer.maxMana))

	def printGameState(self):
		# print("----PASSIVE---")
		print ("-----",self.passivePlayer.getHealth(),"-----")
		player1Minions = self.passivePlayer.getActiveMinions()
		player2Minions = self.activePlayer.getActiveMinions()
		p1MinionStr = ''
		p2MinionStr = ''
		for i in range (len(player1Minions)):
			p1MinionStr = '{} {}/{}'.format(p1MinionStr,player1Minions[i].getAttack(),player1Minions[i].getHealth())
		print(p1MinionStr)
		for i in range (len(player2Minions)):
			p2MinionStr = '{} {}/{}'.format(p2MinionStr,player2Minions[i].getAttack(),player2Minions[i].getHealth())
		print(p2MinionStr)
		print("-----",self.activePlayer.getHealth(),"-----")
		# print("----ACTIVE----")

	def nextTurn(self):
		if self.activePlayer == self.player1:
			self.activePlayer = self.player2
			self.passivePlayer = self.player1
		else:
			self.activePlayer = self.player1
			self.passivePlayer = self.player2
		self.turnCounter += 1
		if self.turnCounter%2==0:
			self.nextRound()
		print (self.activePlayer.getName()+"'s turn")

	def nextRound(self):
		self.passivePlayer.maxMana += 1
		self.passivePlayer.currentMana = self.passivePlayer.maxMana
		self.activePlayer.maxMana+=1
		self.activePlayer.currentMana = self.activePlayer.maxMana

	def mulligan(self):
		pass

	def attackMinion(self,attacker,p2Pos):
		p2minion = self.passivePlayer.getActiveMinions()[int(p2Pos)]
		p2Health = p2minion.getHealth() - attacker.getAttack()
		self.passivePlayer.getActiveMinions()[int(p2Pos)].currentHealth=p2Health
		p1Health = attacker.getHealth() - p2minion.getAttack()
		attacker.currentHealth=p1Health
		print(attacker.getName(),"attacked",p2minion.getName())

	def didAnyoneWin(self):
		aWon = False
		pWon = False
		if self.activePlayer.getHealth() <= 0:
			pWon = True
		if self.passivePlayer.getHealth() <=0:
			aWon = True
		return (aWon,pWon)

	def attackFace(self,attacker):
		self.passivePlayer.reduceHealth(attacker.getAttack())
		print(attacker.name,"has attacked",self.passivePlayer.getName())


	def removeDeadMinions(self):
		count = 0
		for minion in self.activePlayer.activeMinions:
			if minion.currentHealth<=0:
				print(minion.name,"Has died")
				self.activePlayer.activeMinions.pop(count)
			count += 1
		count = 0
		for minion in self.passivePlayer.activeMinions:
			if minion.currentHealth<=0:
				print(minion.name,"Has died")
				self.passivePlayer.activeMinions.pop(count)
			count += 1

	def start(self):
		print("----The game is starting----")
		self.player1.draw(2)
		self.player2.draw(2)
		gameOver = False
		while not gameOver:
			# print(" ROUND:",self.activePlayer.currentMana)
			roundDone = False
			while not (roundDone):
				print("{}'s turn".format(self.activePlayer.getName()))
				if self.activePlayer.getDeck().getRemaining()>0:
					self.activePlayer.draw(1)
				prnt = True
				while True:
					if prnt:
						self.printPassiveHand()
						self.printGameState()
						self.printHand()
					prnt = True
					action = input("Write 'p' to play a card, 'a' to attack, 'e' to end turn, or 'v' to view board: ")
					if action == "p":

						# print ("Your hand consists of: ")
						# self.printHand()
						# for i in range (len(self.activePlayer.hand)):
						# 	print(i,self.activePlayer.hand[i])
						canPlayCard = False
						for card in self.activePlayer.hand:
							# print("card cost and current mana:",card.cost,self.activePlayer.currentMana)
							if card.cost <= self.activePlayer.currentMana:
								canPlayCard = True
						if canPlayCard:
							cardToPlay = input("Which card do you want to play? ('a' to abort) ")
							if cardToPlay != "a":
								self.activePlayer.playCard(cardToPlay)
							else:
								print("Aborting attack")
						else: 
							print("****You don't have enough mana to play any cards****")
							prnt=False
					if action =="v":
						pass
						# self.printGameState()
						# self.printHand()
					if action =="e":
						print ("======== ENDING TURN ========")
						break
					if action =="a":
						attacker = int(input("What index do you want to attack with?: "))
						target = input("Which minion do you want to attack? ('f' for face): ")
						aMin = self.activePlayer.getActiveMinions()[attacker]
						if target =='f':
							self.attackFace(aMin)
						else:
							self.attackMinion(aMin,target)
						self.removeDeadMinions()
						aWon,pWon = self.didAnyoneWin()
						if (aWon or pWon):
							if aWon:
								print("Player:",self.activePlayer.name,"has won the game!")
								gameOver = True
							if pWon:
								print("Player:",self.passivePlayer.name,"has won the game!")
								gameOver = True
							break

					if action =="h":
						for card in self.activePlayer.hand:
							print(card)
				# self.activePlayer.doAction()
				roundDone=True
			self.nextTurn()
