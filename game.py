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
		print("\n*{}*".format(self.passivePlayer.getName()))
		if (len(cardsInHand)>0):
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)

	def printHand(self):
		# 8 kolonner per minion
		line00=''
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.activePlayer.getHand()
		for i in range(len(cardsInHand)):
			line00+="{} {} - ".format(i,cardsInHand[i].getName())
			line0+=" _____  "
			line1+="|{}    | ".format(cardsInHand[i].cost)
			line2+="|     | "
			if (cardsInHand[i].getType()=="Minion"):
				line3+="| {}/{} | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
			elif (cardsInHand[i].getType()=="Spell"):
				line3+="|     | "
			line4+="|_____| "
			line5+="   {}    ".format(i)

		if (len(cardsInHand)>0):
			print(line00)
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)
		print("*{}*\n   MANA: {}/{}".format(self.activePlayer.getName(), self.activePlayer.currentMana,self.activePlayer.maxMana))

	def printActivePlayerActiveMinion(self):
		# 8 kolonner per minion
		line00=''
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		activeM = self.activePlayer.activeMinions
		for i in range(len(activeM)):
			line00+="{} {} - ".format(i,activeM[i].getName())
			line0+=" _____  "
			line1+="|{}    | ".format(activeM[i].cost)
			line2+="|     | "
			if (activeM[i].getType()=="Minion"):
				line3+="| {}/{} | ".format(activeM[i].currentAttack,activeM[i].currentHealth)
			elif (activeM[i].getType()=="Spell"):
				line3+="|     | "
			line4+="|_____| "
			line5+="   {}    ".format(i)

		if (len(activeM)>0):
			print(line00)
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)


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

	def canDoSomething(self):
		for card in self.activePlayer.hand:
			if card.cost <= self.activePlayer.currentMana:
				return True
		for minion in self.activePlayer.activeMinions:
			if minion.hasAttacked==False and minion.frozenRounds>=0:
				return True
		return False

	def playCard(self,cardPosition):

		card = self.activePlayer.hand[int(cardPosition)]
		if (card.cost <= self.activePlayer.currentMana):
			self.activePlayer.currentMana = self.activePlayer.currentMana - card.cost
			if (card.getType()=="Minion"):
				self.playMinion(int(cardPosition))
			else:
				self.playSpell(int(cardPosition))
			return True
		else:
			print("You don't have enough mana")
			return False

	def playSpell(self,cardPosition):
		spell = self.activePlayer.hand.pop(cardPosition)
		print (self.activePlayer.name," played spell: ", spell)
		print (spell.getName(),"Has the effect:",spell.getDescription())
		if spell.damageOne[0]>0:
			if not spell.damageOne[1]:
				target = input("Which minion do you want to damage? ('f' for face): ")
				if target == "f":
					self.passivePlayer.reduceHealth(spell.damageOne[0])
					print(self.activePlayer.getName(),"damaged",self.passivePlayer.getName(),spell.damageOne[0],"damage")	
				else:
					p2minion = self.passivePlayer.getActiveMinions()[int(target)]
					p2Health = p2minion.getHealth() - spell.damageOne[0]
					self.passivePlayer.getActiveMinions()[int(target)].currentHealth=p2Health
					print(self.activePlayer.getName(),"damaged",p2minion.getName(),spell.damageOne[0],"damage")	
		if spell.damageEnemyAOE[0]>0:
			if spell.damageEnemyAOE[1]:
				#Spell hits enemy minions and face
				for minion in self.passivePlayer.activeMinions:
					minion.damage(spell.damageEnemyAOE[0])
				self.passivePlayer.reduceHealth(spell.damageEnemyAOE[0])
			else:
				#Spell hits enemy minions
				for minion in self.passivePlayer.activeMinions:
					minion.damage(spell.damageEnemyAOE[0])
		self.removeDeadMinions()

	def playMinion(self,cardPosition):
		tempMinion = self.activePlayer.hand.pop(cardPosition)
		print (self.activePlayer.name," played minion: ", tempMinion)
		self.activePlayer.activeMinions.append(tempMinion)

	def draw(self,amount,player):
		if player=="a":
			for i in range (amount):
				cardDrawn = self.activePlayer.deck.draw()
				print (self.activePlayer.name,"drew a card")
				self.activePlayer.hand.append( cardDrawn)
		if player=="p":
			for i in range (amount):
				cardDrawn = self.passivePlayer.deck.draw()
				print (self.passivePlayer.name,"drew a card")
				self.passivePlayer.hand.append( cardDrawn)

	def attackMinion(self,attacker,p2Pos):
		p2minion = self.passivePlayer.getActiveMinions()[int(p2Pos)]
		p2Health = p2minion.getHealth() - attacker.getAttack()
		self.passivePlayer.getActiveMinions()[int(p2Pos)].currentHealth=p2Health
		p1Health = attacker.getHealth() - p2minion.getAttack()
		attacker.currentHealth=p1Health
		print(attacker.getName(),"attacked",p2minion.getName())
		attacker.attacked()

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
		attacker.attacked()

	def removeDeadMinions(self):
		killedAny=False
		count = 0
		for minion in self.activePlayer.activeMinions:
			if minion.currentHealth<=0:
				print("{}'s minion '{}' has died".format(self.activePlayer.getName(),minion.getName()))
				self.activePlayer.activeMinions.pop(count)
				killedAny=True
			count += 1
		count = 0
		for minion in self.passivePlayer.activeMinions:
			if minion.currentHealth<=0:
				print("{}'s minion '{}' has died".format(self.passivePlayer.getName(),minion.getName()))
				self.passivePlayer.activeMinions.pop(count)
				killedAny=True
			count += 1
		if (killedAny):
			self.removeDeadMinions()


	def start(self):
		print("----The game is starting----")
		self.draw(2,"a")
		self.draw(2,"p")
		gameOver = False
		while not gameOver:
			# print(" ROUND:",self.activePlayer.currentMana)
			roundDone = False
			while not (roundDone):
				#New players turn
				for minion in self.activePlayer.activeMinions:
					minion.readyToAttack()
					minion.freezeTick()
				print("{}'s turn".format(self.activePlayer.getName()))
				if self.activePlayer.getDeck().getRemaining()>0:
					self.draw(1,"a")
				prnt = True
				while True:
					if prnt:
						self.printPassiveHand()
						self.printGameState()
						self.printHand()
					prnt = True
					if not self.canDoSomething():
						print ("**** You have no more possible actions ****")
				# try:
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
								if not self.playCard(cardToPlay):
									prnt=False
								else:
									prnt=True
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
						if aMin.hasAttacked:
							print("\n****You have already attacked with this minion****\n")
							prnt=False
						elif aMin.frozenRounds > 0:
							print("\n****This minion is frozen****\n")
							prnt=False
						elif target =='f':
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
				# except:
				# 	print("USER ERROR!")
				# 	print("You entered a value that was not good")
				# 	prnt=False
				# self.activePlayer.doAction()
				roundDone=True
			self.nextTurn()
