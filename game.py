import random
import copy
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
			if (cardsInHand[i].getType()=="Minion"):
				line3+="| {}/{} | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
				if (cardsInHand[i].hasTaunt):
					line2+="|Taunt| "
				else:
					line2+="|     | "
			elif (cardsInHand[i].getType()=="Spell"):
				line3+="|SPELL| "
				line2+="|     | "
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

	def printPassivePlayerActiveMinion(self):
		# 8 kolonner per minion
		line00=''
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		activeM = self.passivePlayer.activeMinions

		if len(activeM)<=0:
			print("\nEmpty board side\n")

		for i in range(len(activeM)):
			hasAttacked = activeM[i].hasAttacked
			frozRounds = activeM[i].frozenRounds
			hasTaunt = activeM[i].hasTaunt
			line0+=" _____  "
			if not hasAttacked and frozRounds<=0 :
				line1+="|{}    | ".format(activeM[i].cost)
			elif frozRounds>0:
				line1+="|{}   F| ".format(activeM[i].cost)
			else:
				line1+="|{}   Z| ".format(activeM[i].cost)
			if hasTaunt:
				line2+="|Taunt| "
			else:
				line2+="|     | "
			if (activeM[i].getType()=="Minion"):
				line3+="| {}/{} | ".format(activeM[i].currentAttack,activeM[i].currentHealth)
			elif (activeM[i].getType()=="Spell"):
				line3+="|SPELL| "
			line4+="|_____| "
			line5+="   {}    ".format(i)

		if (len(activeM)>0):
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)

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
		if len(activeM)<=0:
			print("\nEmpty board side\n")
		for i in range(len(activeM)):
			hasAttacked = activeM[i].hasAttacked
			frozRounds = activeM[i].frozenRounds
			hasTaunt = activeM[i].hasTaunt
			line0+=" _____  "
			if not hasAttacked and frozRounds<=0 :
				line1+="|{}    | ".format(activeM[i].cost)
			elif frozRounds>0:
				line1+="|{}   F| ".format(activeM[i].cost)
			else:
				line1+="|{}   Z| ".format(activeM[i].cost)
			if hasTaunt:
				line2+="|Taunt| "
			else:
				line2+="|     | "
			if (activeM[i].getType()=="Minion"):
				line3+="| {}/{} | ".format(activeM[i].currentAttack,activeM[i].currentHealth)
			elif (activeM[i].getType()=="Spell"):
				line3+="|SPELL| "
			line4+="|_____| "
			line5+="   {}    ".format(i)

		if (len(activeM)>0):
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			print(line4)
			print(line5)

	def printGameState(self):
		# print("----PASSIVE---")
		print ("-------------",self.passivePlayer.getHealth(),"-------------")
		player1Minions = self.passivePlayer.getActiveMinions()
		player2Minions = self.activePlayer.getActiveMinions()
		p1MinionStr = ''
		p2MinionStr = ''
		# for i in range (len(player1Minions)):
		# 	p1MinionStr = '{} {}/{}'.format(p1MinionStr,player1Minions[i].getAttack(),player1Minions[i].getHealth())
		# print(p1MinionStr)
		# for i in range (len(player2Minions)):
		# 	p2MinionStr = '{} {}/{}'.format(p2MinionStr,player2Minions[i].getAttack(),player2Minions[i].getHealth())
		# print(p2MinionStr)
		self.printPassivePlayerActiveMinion()
		self.printActivePlayerActiveMinion()
		print("-------------",self.activePlayer.getHealth(),"-------------")
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
		self.activateRoundStartMinions()
		print (self.activePlayer.getName()+"'s turn")

	def nextRound(self):
		self.passivePlayer.maxMana += 1
		self.passivePlayer.currentMana = self.passivePlayer.maxMana
		self.activePlayer.maxMana+=1
		self.activePlayer.currentMana = self.activePlayer.maxMana

	def activateRoundStartMinions(self):
		for minion in self.activePlayer.activeMinions:
			minion.onRoundStart(self.activePlayer,self.passivePlayer)

	def mulligan(self):
		pass

	def canDoSomething(self):
		if self.canPlayCard():
			return True
		if self.canAttack():
			return True
		return False

	def canPlayCard(self):
		for card in self.activePlayer.hand:
			if card.cost <= self.activePlayer.currentMana:
				return True

	def canAttack(self):
		for minion in self.activePlayer.activeMinions:
			if minion.hasAttacked==False and minion.frozenRounds>=0:
				return True

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
			if not spell.damageOne[1] and self.activePlayer.AI==False:
				target = input("Which minion do you want to damage? ('f' for face): ")
				if target == "f":
					self.passivePlayer.reduceHealth(spell.damageOne[0])
					print(self.activePlayer.getName(),"damaged",self.passivePlayer.getName(),spell.damageOne[0],"damage")	
				else:
					p2minion = self.passivePlayer.getActiveMinions()[int(target)]
					p2Health = p2minion.getHealth() - spell.damageOne[0]
					self.passivePlayer.getActiveMinions()[int(target)].currentHealth=p2Health
					print(self.activePlayer.getName(),"damaged",p2minion.getName(),spell.damageOne[0],"damage")
			else:
				self.passivePlayer.reduceHealth(spell.damageOne[0])	
				print(self.activePlayer.getName(),"damaged",self.passivePlayer.getName(),spell.damageOne[0],"damage")	
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
		spell.effect(self)
		self.ActivateOnSpellCastMinions()
		self.removeDeadMinions()

	def playMinion(self,cardPosition):
		tempMinion = self.activePlayer.hand.pop(cardPosition)
		print (self.activePlayer.name," played minion: ", tempMinion)
		self.activePlayer.activeMinions.append(tempMinion)
		tempMinion.bc(self.activePlayer,self.passivePlayer)

	def ActivateOnSpellCastMinions(self):
		for minion in self.activePlayer.activeMinions:
			minion.onSpell(self)
			minion.onSpellOwnRound(self)
			# print("spell cast effects activated")
		for minion in self.passivePlayer.activeMinions:
			minion.onSpell(self)

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
		pMinions = self.passivePlayer.getActiveMinions()
		taunts = []
		for minion in pMinions:
			if minion.hasTaunt:
				taunts.append(minion)
		p2minion = self.passivePlayer.getActiveMinions()[int(p2Pos)]
		if len(taunts)>0:
			if not p2minion.hasTaunt:
				print("*You need to target a minion with taunt*")
				return False
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
		if not attacker.hasAttacked:
			pMinions = self.passivePlayer.getActiveMinions()
			taunts = []
			for minion in pMinions:
				if minion.hasTaunt:
					taunts.append(minion)
			if len(taunts)>0:
				print("You need to attack a minion with taunt")
				return False
			self.passivePlayer.reduceHealth(attacker.getAttack())
			print(attacker.name,"has attacked",self.passivePlayer.getName())
			attacker.attacked()
		else:
			print("that minion has to wait a round to attack")

	def removeDeadMinions(self):
		killedAny=False
		count = 0
		for minion in self.activePlayer.activeMinions:
			if minion.currentHealth<=0:
				print("{}'s minion '{}' has died".format(self.activePlayer.getName(),minion.getName()))
				self.activePlayer.activeMinions.pop(count)
				killedAny=True
				break
			count += 1
		count = 0
		for minion in self.passivePlayer.activeMinions:
			if minion.currentHealth<=0:
				print("{}'s minion '{}' has died".format(self.passivePlayer.getName(),minion.getName()))
				self.passivePlayer.activeMinions.pop(count)
				killedAny=True
				break
			count += 1
		if (killedAny):
			self.removeDeadMinions()

	def getAvailableMoves(self):
		cards = []
		minions = []
		count = 0
		countminion = 0
		for card in self.activePlayer.hand:
			if card.type=="Minion":
				if self.activePlayer.currentMana >= card.cost:
					cards.append(count)
			elif card.type=="Spell":
				pass
			else:
				print ("not minion or spell?")
			count += 1
		return cards



	def start(self):
		print("----The game is starting----")
		self.activePlayer.deck.shuffle()
		self.passivePlayer.deck.shuffle()
		for card in self.activePlayer.deck.cards:
			if card.type=="Minion":
				card.setOwner(self.activePlayer)
		for card in self.passivePlayer.deck.cards:
			if card.type=="Minion":
				card.setOwner(self.passivePlayer)
		self.draw(2,"a")
		self.draw(2,"p")
		gameOver = False
		while not gameOver:
			roundDone = False
			while not (roundDone):
				#New players turn
				if self.activePlayer == self.player2:
				# if 1==2:
					for minion in self.activePlayer.activeMinions:
						minion.readyToAttack()
						minion.freezeTick()
					# print("{}'s turn".format(self.activePlayer.getName()))
					if self.activePlayer.getDeck().getRemaining()>0:
						self.draw(1,"a")
					self.printPassiveHand()
					self.printGameState()
					self.printHand()

					#BOT STUFF
					# moves = self.getAvailableMoves()
					# scores = []
					# for move in moves:
					# 	tempActivePlayer = copy.deepcopy(self.activePlayer)
					# 	tempPassivePlayer = copy.deepcopy(self.passivePlayer)
					# 	print("Tring card:",move)
					# 	self.playCard(move)


					# 	if (tempPassivePlayer.health<=0):
					# 		scores.append(999999999)
					# 	formula = ((len(tempActivePlayer.activeMinions) / 7)*5+((tempPassivePlayer.health/20)*-10))
					# 	scores.append(formula)
					# maxScore = -9999
					# BestMove = -1
					# count = 0
					# for score in scores:
					# 	print("Score: ",score)
					# 	if score > maxScore:
					# 		maxScore = score
					# 		BestMove = count
					# 	count += 1
					# print("Best move is:",BestMove)
					for i in range (len(self.activePlayer.hand)):
						try:
							self.playCard(i)
						except:
							pass
					for i in range (len(self.activePlayer.activeMinions)):
						try:
							# print("bot prøver face")
							self.attackFace(self.activePlayer.activeMinions[i])
						except:
							print("Fikk error")
							pass
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

					self.nextTurn()
					

					# Gjør det heller lett
					
				else:
					for minion in self.activePlayer.activeMinions:
						minion.readyToAttack()
						minion.freezeTick()
					# print("{}'s turn".format(self.activePlayer.getName()))
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
						if self.canAttack() and self.canPlayCard():
							action = input("Write 'p' to play a card, 'a' to attack or 'e' to end turn: ")
						elif self.canAttack():
							action = input("Write 'a' to attack or 'e' to end turn: ")
						elif self.canPlayCard():
							action = input("Write 'p' to play a card or 'e' to end turn: ")
						else:
							action = input("Write 'e' to end turn: ")
						if action == "p":
							canPlayCard = False
							for card in self.activePlayer.hand:
								if card.cost <= self.activePlayer.currentMana:
									canPlayCard = True
							if canPlayCard:
								cardToPlay = input("Which card do you want to play? ('a' to abort) ")
								if cardToPlay != "a" and not cardToPlay=="":
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
						if action =="e":
							print ("======== ENDING TURN ========")
							break
						if action =="a":
							attacker = int(input("What index do you want to attack with?: "))
							if attacker >= len(self.activePlayer.activeMinions):
								print("\nThat index was too high")

							else:
								taunts = []
								for minion in self.passivePlayer.activeMinions:
									if minion.hasTaunt:
										taunts.append(minion)
								target = input("Which minion do you want to attack? ('f' for face): ")
								print("")
								aMin = self.activePlayer.getActiveMinions()[attacker]
								if len(taunts)>0:
										if not aMin.hasTaunt:
											print("You need to target a minion with taunt")
										else:
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
								else:
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
