import random
import copy
import textwrap
import socket
import time
from cards import Spell, Minion, Card

class Game:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.activePlayer = player1
		self.passivePlayer = player2
		self.turnCounter = 0
		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5005
		self.BUFFER_SIZE = 1024
		# self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.playersConnected = 0
		self.localGame = True
		self.againstAI = True
		self.simulation= False
		self.printing = True
		self.debug = True
		self.isSimulated = False

	def evaluateState(game):
		totalAttackAndHealYourSide = 0 # Høyere er bedre
		totalAttackAndHealEnemySide = 0 # Lavere er bedre
		yourHealth = game.activePlayer.health # Høyere er bedre
		enemyHealth = game.passivePlayer.health # Lavere er bedre
		ownHandLength = len(game.activePlayer.hand)
		# print("own hand",ownHandLength)
		enemyHandLength = len(game.passivePlayer.hand)
		numberOfEnemyMinions = len(game.passivePlayer.activeMinions)
		numberOfFriendlyMinions = len(game.activePlayer.activeMinions)

		for minion in game.activePlayer.activeMinions:
			totalAttackAndHealYourSide += minion.currentAttack + minion.currentHealth
		for minion in game.passivePlayer.activeMinions:
			totalAttackAndHealEnemySide += minion.currentAttack + minion.currentHealth
		
		numberOfFriendlyMinionsScale = numberOfFriendlyMinions / 3
		numberOfEnemyMinionsScale = numberOfFriendlyMinions / 3
		yourHealthScale = yourHealth/30
		enemyHealthScale = enemyHealth/30
		ownHandLengthScale = ownHandLength/4
		enemyHandLengthScale = enemyHandLength/4
		totalAttackAndHealYourSideScale = totalAttackAndHealYourSide / 30
		totalAttackAndHealEnemySideScale = totalAttackAndHealEnemySide / 30
		if yourHealthScale>1: yourHealthScale = 1
		if enemyHealthScale>1: enemyHealthScale = 1
		if ownHandLengthScale>1: ownHandLengthScale = 1
		if enemyHandLengthScale>1: enemyHandLengthScale = 1
		if totalAttackAndHealYourSideScale>1: totalAttackAndHealYourSideScale = 1
		if totalAttackAndHealEnemySideScale>1: totalAttackAndHealEnemySideScale = 1
		if numberOfFriendlyMinionsScale>1: numberOfFriendlyMinionsScale = 1
		if numberOfEnemyMinionsScale>1: numberOfEnemyMinionsScale = 1




		# utility = (enemyHealthScale*((yourHealthScale*-5)+(ownHandLengthScale*-1)+(enemyHandLengthScale)+(totalAttackAndHealYourSide*-1)+(totalAttackAndHealEnemySideScale)))
		utility = (enemyHealthScale * 10) - (yourHealthScale*10) -(numberOfFriendlyMinionsScale*5)+(numberOfEnemyMinionsScale*5)+ (totalAttackAndHealEnemySideScale*5) - (totalAttackAndHealYourSideScale*5) + (enemyHandLengthScale*1) - (ownHandLengthScale*1)

		# 0 utility is optimal state
		return utility

	def generateBestLegalMove(game):
		nyGame = copy.deepcopy(game)
		nyGame2 = copy.deepcopy(game)
		currentUtility = game.evaluateState()
		bestCard = -1
		bestCardUtility = 999999

		for card in range(len(nyGame.activePlayer.hand)):
			tempGame=copy.deepcopy(nyGame)
			tempGame.printing=False
			tempGame.isSimulated=True
			tempGame.playCard(card)
			tempUtility = tempGame.evaluateState()
			if tempUtility < bestCardUtility:
				bestCardUtility = tempUtility
				bestCard = card

		bestAttackMinion = -1
		bestAttackTarget = -1
		bestAttackMinionUtility = 999999

		bestAttackFaceUtility = 999999
		for minion in  range(len(nyGame2.activePlayer.activeMinions)):

			tempMinion = copy.deepcopy(minion)
			tempGame=copy.deepcopy(nyGame2)
			tempGame.printing=False
			tempGame.isSimulated=True
			possibleTargets = tempGame.getPossibleTargetsOfMinion(tempGame.activePlayer.activeMinions[tempMinion])
			for target in possibleTargets[0]:
				tempGame=copy.deepcopy(game)
				tempGame.printing=False
				tempGame.attackMinion(tempGame.activePlayer.activeMinions[tempMinion],target)
				# tempGame.activePlayer.activeMinions[tempMinion].hasAttacked=False
				tempUtility = tempGame.evaluateState()
				if tempUtility < bestAttackMinionUtility:
					bestAttackMinionUtility = tempUtility
					bestAttackMinion = tempMinion
					bestAttackTarget = target
		for minion in  range(len(nyGame2.activePlayer.activeMinions)):
			# print("sjekker value for å gå face for minion",minion)
			tempMinion = copy.deepcopy(minion)
			if possibleTargets[1]: # Face virker ikke
				# print("tester face")
				tempGame=copy.deepcopy(nyGame2)
				tempGame.printing=False
				tempGame.attackFace(tempGame.activePlayer.activeMinions[tempMinion])
				# tempGame.activePlayer.activeMinions[tempMinion].hasAttacked=False
				tempUtility = tempGame.evaluateState()
				# print("angriping med",tempMinion,"gir utility: ",tempUtility)
				if tempUtility < bestAttackFaceUtility:
					bestAttackFaceUtility = tempUtility
					bestAttackMinion = tempMinion
					bestAttackTarget = -1
		bestAttackMinionTarget = [bestAttackMinion,bestAttackTarget]
		time.sleep(0)
		# print("Util: card, attMinion, attFace, current")
		print("utilities:",bestCardUtility,bestAttackMinionUtility,bestAttackFaceUtility,currentUtility)
		if currentUtility <= bestCardUtility and currentUtility <= bestAttackMinionUtility and currentUtility < bestAttackFaceUtility:
			return ("noMoreMoves",-1)
		if bestCardUtility < bestAttackMinionUtility and bestCardUtility < bestAttackFaceUtility:
			return ("bestCard",bestCard)
		elif bestAttackMinionUtility < bestCardUtility and bestAttackMinionUtility < bestAttackFaceUtility:
			return ("bestAttackMinion",bestAttackMinionTarget)
		elif bestAttackFaceUtility < bestCardUtility and bestAttackMinionUtility > bestAttackFaceUtility:
			return ("bestAttackFace",bestAttackMinion)
		if bestCardUtility==999999 and bestCardUtility==999999:
			return("noMoreMoves",-1)
		return("noMoreMoves",-1)

		# #            what to do, which card, which target
		# bestMove = ["playCard",0,1]
		# bestMove = ["attackFace",1]
		# bestMove = ["attackMinion",1,0]


	def customPrint(text):
		if not self.localGame and not self.againstAI:
			self.activePlayer.connection.send(text.encode())
		else:
			print(text)

	def getInput(self,description):
		if not self.localGame:
			addr = self.activePlayer.IP
			conn = self.activePlayer.connection
			message=description
			conn.send(message.encode())
			return conn.recv(1024).decode()
		else:
			return (input(description))

	def startServer(self):
		self.s.bind((self.TCP_IP, self.TCP_PORT))
		self.s.listen(1)
		print("Waiting for clients to connect")

		while 1:
			conn, addr = self.s.accept()
			print("Connection from:",addr)
			if self.playersConnected==0:
				data = conn.recv(1024).decode()
				print("received data:",data)
				# conn.send("Received".encode())
				if data=="Player":
					self.player1.IP=addr
					self.player1.connection = conn
					print("Player 1 is:",addr)
					self.player2.IP=addr
					self.player2.connection = conn
					print("Player 2 is:",addr)
					break
			# elif self.playersConnected==1:
			# 	data = conn.recv(1024).decode()
			# 	print("received data:",data)
			# 	# conn.send("Received".encode())
			# 	if data=="Player":
			# 		self.player2.IP=addr
			# 		self.player2.connection = conn
			# 		print("Player 2 is:",addr)

	def initialize(self,player1,player2):
		self.startServer()
		self.start()

	def printCardDescription(self,cards):
		c = 0
		print("index - cost - name - effects")
		for card in cards:
			print("   {}  -  {}   - {}:  {}".format(c,card.cost,card.name,card.description))
			c+=1

	def printAttackReadyMinions(self):
		print("\nMinions who can attack:\n")
		longestName = 0
		for minion in self.activePlayer.activeMinions:
			if len(minion.name)>longestName:
				longestName = len(minion.name)
		if longestName > 25:
			longestName = 25

		count = 0
		print ("Position - Name - Stats - Effects")
		for minion in self.activePlayer.activeMinions:
			if not minion.hasAttacked and minion.frozenRounds<=0:
				tempName = "{0:<{1}}".format(minion.name,longestName)
				if len(tempName)>longestName-1:
					tempName=tempName[0:longestName]
				tempType = "{0:<6}".format(minion.type)
				print("  {4} - {1} - {5}/{6} - {2}".format(minion.cost,tempName,minion.description,tempType,count,minion.currentAttack,minion.currentHealth))
			count += 1	
		print("")

	def printPlayableCards(self,player):
		print("\nCards you can play:\n")
		longestName = 0
		for card in self.activePlayer.hand:
			if len(card.name)>longestName and card.cost <= self.activePlayer.currentMana:
				longestName = len(card.name)
		if longestName > 25:
			longestName = 25

		count = 0
		tempText = 'Name'
		print ("  # -Cost- {0: <{1}} - Type - Stats - Effects".format(tempText,longestName))
		for card in self.activePlayer.hand:
			if card.cost <= self.activePlayer.currentMana:
				tempName = "{0:<{1}}".format(card.name,longestName)
				if len(tempName)>longestName-1:
					tempName=tempName[0:longestName]
				tempType = "{0:<6}".format(card.type)
				if card.type=="Spell":
					tempType += " - N/A"
					print("  {4} - {0}  - {1} - {3} - {2}".format(card.cost,tempName,card.description,tempType,count))
				else:
					print("  {4} - {0}  - {1} - {3} - {5}/{6} - {2}".format(card.cost,tempName,card.description,tempType,count,card.currentAttack,card.currentHealth))
			count += 1	
		print("")

	def printHandDetails(self,player):
		print("\nYour hand:")
		longestName = 0
		for card in self.activePlayer.hand:
			if len(card.name)>longestName:
				longestName = len(card.name)
		if longestName > 25:
			longestName = 25

		count = 0
		print ("Position - Cost - Name - Type - Stats - Effects")
		for card in self.activePlayer.hand:
			tempName = "{0:<{1}}".format(card.name,longestName)
			if len(tempName)>longestName-1:
				tempName=tempName[0:longestName]
			tempType = "{0:<6}".format(card.type)
			if card.type=="Spell":
				tempType += " - N/A"
				print("  {4} - {0} - {1} - {3} - {2}".format(card.cost,tempName,card.description,tempType,count))
			else:
				print("  {4} - {0} - {1} - {3} - {2}".format(card.cost,tempName,card.description,tempType,count))
			count += 1

	def printDetails(self):
		print("\n === GAME STATE DETAILS === \n")
		print("\nEnemy minions:")
		for minion in self.passivePlayer.activeMinions:
			print("    {} - {} - {}".format(minion.name,minion.currentAttack,minion.currentHealth,minion.description))
		print("\nYour minions:")
		for minion in self.activePlayer.activeMinions:
			print("    {} - {} - {}".format(minion.name,minion.currentAttack,minion.currentHealth,minion.description))
		self.printHandDetails(self.activePlayer)
		print("")

	def printPassiveHand(self):
		line0=''
		line1=''
		line2=''
		line3=''
		line4=''
		line5=''
		# line6=''
		line7=''
		cards =''
		cardsInHand = self.passivePlayer.getHand()
		for i in range(len(cardsInHand)):
			cards += "{} ".format(self.passivePlayer.hand[i].getName())
			# cards +=self.passivePlayer.hand[i].getName()+" "
			line0+=" _______  "
			line1+="|       | "
			line2+="|       | "
			line3+="|       | "
			# line6+="|       | "
			line7+="|       | "
			line4+="|_______| "

		print("\n*{}*".format(self.passivePlayer.getName()))
		if (len(cardsInHand)>0):
			# print(cards	)
			print(line0)
			print(line1)
			print(line2)
			print(line3)
			# print(line6)
			print(line7)
			print(line4)
			print(line5)

	def printHand(self):
		# 8 kolonner per minion
		line00=''
		line0=''
		line1=''
		line10=''
		line11=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.activePlayer.getHand()
		for i in range(len(cardsInHand)):
			line00+="{} - ".format(cardsInHand[i].getName())
			line0+=" _________  "
			line1+="|{}        | ".format(cardsInHand[i].cost)
			tempName = cardsInHand[i].name
			if len(tempName)>9:
				tempName = tempName[0:9]
			line10+="|{0: <9}| ".format(tempName)
			line11+="|         | "
			if (cardsInHand[i].getType()=="Minion"):
				line3+="|   {}/{}   | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
				if (cardsInHand[i].hasTaunt):
					line2+="|  Taunt  | "
				else:
					line2+="|         | "
			elif (cardsInHand[i].getType()=="Spell"):
				line3+="|  SPELL  | "
				# line2+="|         | "
				tempDesc = cardsInHand[i].description
				if len(tempDesc)>9:
					tempDesc=tempDesc[0:9]
				line2+="|{}| ".format(tempDesc)
			line4+="|_________| "
			line5+="    #{}      ".format(i)
		
		if (len(cardsInHand)>0):
			print("MANA: {}/{}".format(self.activePlayer.currentMana,self.activePlayer.maxMana))
			# print(line00)
			print(line0)
			print(line1)
			print(line10)
			print(line11)
			print(line2)
			print(line3)
			print(line4)
			print(line5)
		else:
			print("*{}*\n   MANA: {}/{}".format(self.activePlayer.getName(), self.activePlayer.currentMana,self.activePlayer.maxMana))

	def printPassivePlayerActiveMinion(self):
		align = 5 - len(self.passivePlayer.activeMinions)
		if align<0:
			align = 0
		line00=''
		line0=''
		line1=''
		line10=''
		line11=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.passivePlayer.activeMinions
		for i in range(align):
			line00+="    "
			line0+="    "
			line1+="    "
			line10+="    "
			line11+="    "
			line2+="    "
			line3+="    "
			line4+="    "
			line5+="    "		
		for i in range(len(cardsInHand)):
			line00+="{} - ".format(cardsInHand[i].getName())
			line0+=" _________  "
			hasAttacked = cardsInHand[i].hasAttacked
			frozRounds = cardsInHand[i].frozenRounds
			hasTaunt = cardsInHand[i].hasTaunt

			tempString = cardsInHand[i].getName()
			if len(tempString)>7:
				tempString = tempString[0:5]+".."
			line00+="{}- ".format(tempString)
			if not hasAttacked and frozRounds<=0 :
				line1+="|{}        | ".format(cardsInHand[i].cost)
			elif frozRounds>0:
				line1+="|{}  FROZEN| ".format(cardsInHand[i].cost)
			else:
				line1+="|{}       Z| ".format(cardsInHand[i].cost)
			tempName = cardsInHand[i].name
			if len(tempName)>9:
				tempName = tempName[0:9]
			line10+="|{0: <9}| ".format(tempName)
			line11+="|         | "
			if (cardsInHand[i].getType()=="Minion"):
				line3+="|   {}/{}   | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
				if (cardsInHand[i].hasTaunt):
					line2+="|  Taunt  | "
				else:
					line2+="|         | "
			elif (cardsInHand[i].getType()=="Spell"):
				line3+="|  SPELL  | "
				# line2+="|         | "
				tempDesc = cardsInHand[i].description
				if len(tempDesc)>9:
					tempDesc=tempDesc[0:9]
				line2+="|{}| ".format(tempDesc)
			line4+="|_________| "
			line5+="    #{}      ".format(i)
		
		if (len(cardsInHand)>0):
			# print(line00)
			print(line0)
			print(line1)
			print(line10)
			print(line11)
			print(line2)
			print(line3)
			print(line4)
			print(line5)
		else:
			print ("\nEmpty board side\n")

	def printActivePlayerActiveMinion(self):
		align = 5 - len(self.activePlayer.activeMinions)
		if align<0:
			align = 0
		line00=''
		line0=''
		line1=''
		line10=''
		line11=''
		line2=''
		line3=''
		line4=''
		line5=''
		cardsInHand = self.activePlayer.activeMinions
		for i in range(align):
			line00+="    "
			line0+="    "
			line1+="    "
			line10+="    "
			line11+="    "
			line2+="    "
			line3+="    "
			line4+="    "
			line5+="    "		
		for i in range(len(cardsInHand)):
			line00+="{} - ".format(cardsInHand[i].getName())
			line0+=" _________  "
			hasAttacked = cardsInHand[i].hasAttacked
			frozRounds = cardsInHand[i].frozenRounds
			hasTaunt = cardsInHand[i].hasTaunt

			tempString = cardsInHand[i].getName()
			if len(tempString)>7:
				tempString = tempString[0:5]+".."
			line00+="{}- ".format(tempString)
			if not hasAttacked and frozRounds<=0 :
				line1+="|{}        | ".format(cardsInHand[i].cost)
			elif frozRounds>0:
				line1+="|{}  FROZEN| ".format(cardsInHand[i].cost)
			else:
				line1+="|{}       Z| ".format(cardsInHand[i].cost)
			tempName = cardsInHand[i].name
			if len(tempName)>9:
				tempName = tempName[0:9]
			line10+="|{0: <9}| ".format(tempName)
			line11+="|         | "
			if (cardsInHand[i].getType()=="Minion"):
				line3+="|   {}/{}   | ".format(cardsInHand[i].currentAttack,cardsInHand[i].currentHealth)
				if (cardsInHand[i].hasTaunt):
					line2+="|  Taunt  | "
				else:
					line2+="|         | "
			elif (cardsInHand[i].getType()=="Spell"):
				line3+="|  SPELL  | "
				# line2+="|         | "
				tempDesc = cardsInHand[i].description
				if len(tempDesc)>9:
					tempDesc=tempDesc[0:9]
				line2+="|{}| ".format(tempDesc)
			line4+="|_________| "
			line5+="    #{}      ".format(i)
		
		if (len(cardsInHand)>0):
			# print(line00)
			print(line0)
			print(line1)
			print(line10)
			print(line11)
			print(line2)
			print(line3)
			print(line4)
			print(line5)
		else:
			print ("\nEmpty board side\n")

	def printGameState(self):
		# print("----PASSIVE---")
		print ("Health----------------",self.passivePlayer.getHealth(),"----------------------")
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
		print("================================================")
		self.printActivePlayerActiveMinion()
		print("Health----------------",self.activePlayer.getHealth(),"----------------------")
		# print("----ACTIVE----")

	def getPossibleTargetsOfMinion(self,attacker):
		enemyMinions = self.passivePlayer.activeMinions
		taunts = []
		targets = []
		face = False
		c = 0
		for minion in enemyMinions:
			if minion.hasTaunt:
				taunts.append(c)
			c += 1
		if attacker.onlyAbleToAttackMinions==False and len(taunts)==0:
			targets = range(0,len(enemyMinions))
			face = True
		elif len(taunts)>0:
			targets = taunts
		elif attacker.onlyAbleToAttackMinions and len(taunts)==0:
			targets = range(0,len(enemyMinions))
		elif len(targets)==0:
			targets = []
			face = True

		return targets,face

	def printPossibleTargetsOfMinion(self,attacker):
		enemyMinions = self.passivePlayer.activeMinions
		taunts = []
		targets = []
		face = False
		c = 0
		for minion in enemyMinions:
			if minion.hasTaunt:
				taunts.append(c)
			c += 1
		if attacker.onlyAbleToAttackMinions==False and len(taunts)==0:
			targets = range(0,len(enemyMinions))
			face = True
		elif len(taunts)>0:
			targets = taunts
		elif attacker.onlyAbleToAttackMinions and len(taunts)==0:
			targets = range(0,len(enemyMinions))
		elif len(targets)==0:
			targets = []
			face = True

		print("\nLegal Targets:\n")
		longestName = 0
		for target in targets:
			if len(enemyMinions[target].name)>longestName:
				longestName = len(enemyMinions[target].name)
		if longestName > 25:
			longestName = 25

		count = 0
		print ("Position - Name - Stats - Effects")
		for target in targets:
			tempName = "{0:<{1}}".format(enemyMinions[target].name,longestName)
			if len(tempName)>longestName-1:
				tempName=tempName[0:longestName-1]
			tempType = "{0:<6}".format(enemyMinions[target].type)
			print("  {4} - {1} - {2} - {5}/{6} - {3}".format(enemyMinions[target].cost,tempName,enemyMinions[target].description,tempType,targets[count],enemyMinions[target].currentAttack,enemyMinions[target].currentHealth))
			count += 1
		if face:
			print("  f - FACE")
		print("")

	def nextTurn(self):
		for minion in self.activePlayer.activeMinions:
			minion.roundEnd(self,minion)
			self.removeDeadMinions()
		if self.activePlayer == self.player1:
			self.activePlayer = self.player2
			self.passivePlayer = self.player1
			print("===============",self.activePlayer.name,"'s turn =============")
		else:
			self.activePlayer = self.player1
			self.passivePlayer = self.player2
		self.turnCounter += 1
		if self.turnCounter%2==0:
			self.nextRound()
		self.activateRoundStartMinions()
		# print (self.activePlayer.getName()+"'s turn")
		for minion in self.activePlayer.activeMinions:
			minion.hasAttacked=False
		for minion in self.passivePlayer.activeMinions:
			minion.hasAttacked=False

	def nextRound(self):
		self.passivePlayer.maxMana += 1
		self.passivePlayer.currentMana = self.passivePlayer.maxMana
		self.activePlayer.maxMana+=1
		self.activePlayer.currentMana = self.activePlayer.maxMana

	def activateRoundStartMinions(self):
		for minion in self.activePlayer.activeMinions:
			minion.onRoundStart(self)

	def mulligan(self,player):
		if player.AI==False:
			# print("Your hand:")
			c=0
			for card in player.hand:
				c+=1
			self.printHand()
			remove = str(input("Which cards do you want to remove?: (e.g. '02')"))
			k=0
			for card in remove:
				# print("removing",card)
				tempCard = player.hand.pop(int(card)-k)
				# print(tempCard.name)
				player.deck.cards.append(tempCard)
				k+=1
			player.deck.shuffle()
			for card in remove:
				cardDrawn = player.deck.draw()
				player.hand.append( cardDrawn)
			
			# print("Done with mulligan")
			# for card in player.hand:
			# 	print(card.name)
		else:
			c=0
			k=0
			# for card in player.hand:
			# 	print(" kort:",card.name)
			for card in player.hand:

				if card.cost>6:
					if self.printing:
						print("mulligan",card.name)
					player.deck.cards.append(card)
					print("popper:",player.hand[k])
					player.hand.pop(k)
					c+=1
					break
				k+=1
			# player.deck.shuffle()
			# print(player.hand)
			k=0
			for card in player.hand:
				if card.cost>5:
					# if self.printing:
					# 	print("mulligan",card.name)
					player.deck.cards.append(card)
					# print("popper:",player.hand[k])
					player.hand.pop(k)
					c+=1
					break
				k+=1
			# player.deck.shuffle()
			# print(player.hand)
			k=0
			for card in player.hand:
				if card.cost>4:
					# if self.printing:
					# 	print("mulligan",card.name)
					player.deck.cards.append(card)
					# print("popper:",player.hand[k])
					player.hand.pop(k)
					c+=1
					break
				k+=1
			k=0
			for card in player.hand:
				if card.cost>3:
					# if self.printing:
					# 	print("mulligan",card.name)
					player.deck.cards.append(card)
					# print("popper:",player.hand[k])
					player.hand.pop(k)
					c+=1
					break
				k+=1
			# print(player.hand)
			player.deck.shuffle()
			
			# if player == self.activePlayer:
			# 	self.draw(c,"a")
			# else:
			# 	self.draw(c,"p")
			for count in range(c):
				cardDrawn = player.deck.draw()
				player.hand.append( cardDrawn)
			# if self.printing:
			# 	print("mullied",c,"cards")

		

	def updateContinousEffects(self):
		for minion in self.activePlayer.activeMinions:
			minion.continousEffect(self,minion)
		for minion in self.passivePlayer.activeMinions:
			minion.continousEffect(self,minion)

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
			if minion.hasAttacked==False and minion.frozenRounds<=0:
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
			if self.activePlayer.AI==False:
				print("You don't have enough mana")
			return False

	def playSpell(self,cardPosition):
		spell = self.activePlayer.hand[cardPosition]
		if spell.targetOwnMinions and len(self.activePlayer.activeMinions)==0:
			print("This spell needs a friendly target")
			return False
		spell = self.activePlayer.hand.pop(cardPosition)
		if self.printing:
			print (self.activePlayer.name,"played spell:  ", spell)
		# print (spell.getName(),"Has the effect:",spell.getDescription())
		if spell.damageOne[0]>0:
			if not spell.damageOne[1] and self.activePlayer.AI==False:
				target = input("Which minion do you want to damage? ('f' for face): ")
				if target == "f":
					self.passivePlayer.reduceHealth(spell.damageOne[0])
					if self.printing:
						print(self.activePlayer.getName(),"damaged",self.passivePlayer.getName(),spell.damageOne[0],"damage")	
				else:
					p2minion = self.passivePlayer.getActiveMinions()[int(target)]
					p2Health = p2minion.getHealth() - spell.damageOne[0]
					self.passivePlayer.getActiveMinions()[int(target)].currentHealth=p2Health
					if self.printing:
						print(self.activePlayer.getName(),"damaged",p2minion.getName(),spell.damageOne[0],"damage")
			else:
				self.passivePlayer.reduceHealth(spell.damageOne[0])	
				if self.printing:
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
		self.updateContinousEffects()

	def playMinion(self,cardPosition):
		tempMinion = self.activePlayer.hand.pop(cardPosition)
		if self.printing:
			print (self.activePlayer.name,"played minion: ", tempMinion)
		self.activePlayer.activeMinions.append(tempMinion)
		tempMinion.bc(self,tempMinion)
		self.removeDeadMinions()
		self.updateContinousEffects()

	def summonMinion(self,minion,player): #Summon minion, called from effects in other cards
		newMinion = copy.deepcopy(minion)
		player.activeMinions.append(newMinion)
		newMinion.bc(self,newMinion)
		newMinion.setOwner(player)
		self.removeDeadMinions()
		self.updateContinousEffects()

	def ActivateOnSpellCastMinions(self):
		for minion in self.activePlayer.activeMinions:
			minion.onSpell(self)
			minion.onSpellOwnRound(self,minion)
			# print("spell cast effects activated")
		for minion in self.passivePlayer.activeMinions:
			minion.onSpell(self)

	def draw(self,amount,player):
		if player=="a":
			for i in range (amount):
				cardDrawn = self.activePlayer.deck.draw()
				# print (self.activePlayer.name,"drew a card")
				self.activePlayer.hand.append( cardDrawn)
		if player=="p":
			for i in range (amount):
				cardDrawn = self.passivePlayer.deck.draw()
				# print (self.passivePlayer.name,"drew a card")
				self.passivePlayer.hand.append( cardDrawn)

	def attackMinion(self,attacker,p2Pos):
		if attacker.hasAttacked == False and attacker.frozenRounds<=0:
			pMinions = self.passivePlayer.getActiveMinions()
			taunts = []
			for minion in pMinions:
				if minion.hasTaunt:
					taunts.append(minion)
			p2minion = self.passivePlayer.getActiveMinions()[int(p2Pos)]
			if len(taunts)>0:
				if not p2minion.hasTaunt:
					if self.activePlayer.AI==False:
						print("*You need to target a minion with taunt*")
					return False
			p2Health = p2minion.getHealth() - attacker.getAttack()
			self.passivePlayer.getActiveMinions()[int(p2Pos)].currentHealth=p2Health
			p1Health = attacker.getHealth() - p2minion.getAttack()
			attacker.currentHealth=p1Health
			if self.printing:
				print(attacker.getName(),"attacked",p2minion.getName())
			attacker.attacked()
			self.updateContinousEffects()
			self.removeDeadMinions()
			self.updateContinousEffects()
			attacker.afterAttack(self,attacker)

	def didAnyoneWin(self):
		aWon = False
		pWon = False
		if self.activePlayer.getHealth() <= 0:
			pWon = True
		if self.passivePlayer.getHealth() <=0:
			aWon = True
		return (aWon,pWon)

	def attackFace(self,attacker):
		# if self.printing:
			# print("Inni attackface")
			# print("hasattacked: ",attacker.hasAttacked,"froze:",attacker.frozenRounds)
		if not attacker.hasAttacked and attacker.frozenRounds<=0:
			# if self.printing:
				# print("etter hasattacked og frozen")
			if  attacker.onlyAbleToAttackMinions==False:
				if attacker.currentAttack<=0:
					print("This minion has no attack")
				else:
					pMinions = self.passivePlayer.getActiveMinions()
					taunts = []
					for minion in pMinions:
						if minion.hasTaunt:
							taunts.append(minion)
					if len(taunts)>0:
						if self.activePlayer.AI==False:
							print("You need to attack a minion with taunt")
						return False
					self.passivePlayer.reduceHealth(attacker.getAttack())
					if self.printing:
						print(attacker.name,"has attacked",self.passivePlayer.getName(),"for",attacker.currentAttack,"damage")
					attacker.attacked()
					attacker.afterAttack(self,attacker)
			else:
				print("This minion may only attack minions")
		else:
			if self.activePlayer.AI==False:
				print("that minion has to wait a round to attack")
		self.updateContinousEffects()
		
	def removeDeadMinions(self):
		listOfDeathrattles = []
		killedAny=False
		count = 0
		for minion in self.activePlayer.activeMinions:
			if minion.currentHealth<=0:
				if self.printing:
					print("{}'s minion '{}' has died".format(self.activePlayer.getName(),minion.getName()))
				self.activePlayer.activeMinions.pop(count)
				listOfDeathrattles.append(minion)

				killedAny=True
				break
			count += 1
		count = 0
		for minion in self.passivePlayer.activeMinions:
			if minion.currentHealth<=0:
				if self.printing:
					print("{}'s minion '{}' has died".format(self.passivePlayer.getName(),minion.getName()))
				self.passivePlayer.activeMinions.pop(count)
				listOfDeathrattles.append(minion)
				killedAny=True
				break
			count += 1
		if (killedAny):
			for minion in listOfDeathrattles:
				minion.dr(self,minion)
			self.removeDeadMinions()
		if (killedAny):
			return True
		else:
			return False

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
		self.activePlayer.setGame(self)
		self.passivePlayer.setGame(self)
		self.activePlayer.deck.shuffle()
		self.passivePlayer.deck.shuffle()

		for card in self.activePlayer.deck.cards:
			if card.type=="Minion":
				card.setOwner(self.activePlayer)
		for card in self.passivePlayer.deck.cards:
			if card.type=="Minion":
				card.setOwner(self.passivePlayer)
		coin = Spell("The Coin",0)
		def coinEffect(game):
			game.activePlayer.currentMana += 1
		coin.setEffect(coinEffect)
		self.passivePlayer.hand.append(copy.deepcopy(coin))
		self.draw(3,"a")
		self.draw(4,"p")
		if self.againstAI:
			self.passivePlayer.AI=True
		if self.simulation:
			self.passivePlayer.AI=True
			self.activePlayer.AI=True
			self.activePlayer.printing=False
			self.passivePlayer.printing=False
		self.mulligan(self.activePlayer)
		self.mulligan(self.passivePlayer)

		gameOver = False
		while not gameOver:
			roundDone = False
			while not (roundDone):
				self.updateContinousEffects()
				#New players turn
				for minion in self.activePlayer.activeMinions:
					minion.readyToAttack()
					minion.freezeTick()
				for minion in self.passivePlayer.activeMinions:
					minion.readyToAttack()
					minion.freezeTick()
				if self.activePlayer.AI:
					if self.activePlayer == self.player1:
						self.printPassiveHand()
						self.printGameState()
						self.printHand()
						print(self.evaluateState())
					if self.activePlayer.getDeck().getRemaining()>0:
						self.draw(1,"a")

					self.updateContinousEffects()
					c=0
					while True:
						bestMove = self.generateBestLegalMove()
						# print("bestmove:",bestMove)
						# if  c>=2:
						# 	print("can't do shit")
						# 	break
						# print(bestMove)
						if bestMove[0]=="noMoreMoves":
							break
						if bestMove[0]=="bestCard":
							self.playCard(bestMove[1])
							# print("Spiller beste kort")
						elif bestMove[0]=="bestAttackFace":
							print("attacking face with",self.activePlayer.activeMinions[bestMove[1]].name)
							self.attackFace(self.activePlayer.activeMinions[bestMove[1]])
							# bestMove[1].hasAttacked=True
						elif bestMove[0]=="bestAttackMinion":
							self.attackMinion(self.activePlayer.activeMinions[bestMove[1][0]],bestMove[1][1])
						if self.activePlayer == self.player1 and self.printing:
							self.printPassiveHand()
							self.printGameState()
							self.printHand()
							print(self.evaluateState())
						c+=1
					'''
					if random.randint(0,5)==0:
						print("trolo spill at som kan")
						for i in range (len(self.activePlayer.hand)):
							try:
								self.playCard(i)
								# time.sleep(0.2)
							except:
								pass
						# time.sleep(1)
						for k in range(0,10):
							for i in range (len(self.activePlayer.activeMinions)):
								face = random.randint(0,10)
								if face>2:
									try:
										# print("bot går face")
										self.attackFace(self.activePlayer.activeMinions[i])
										for k in range (len(self.passivePlayer.activeMinions)):
											self.attackMinion(self.activePlayer.activeMinions[i],k)
									except:
										pass
								else:
									try:
										# print("bot går minions")
										for k in range (len(self.passivePlayer.activeMinions)):
											self.attackMinion(self.activePlayer.activeMinions[i],k)
										self.attackFace(self.activePlayer.activeMinions[i])
										 
									except:
										pass
					for i in range (len(self.activePlayer.activeMinions)):
						try:
							# print("bot går face")
							self.attackFace(self.activePlayer.activeMinions[i])
						except:
							pass
							'''
					if self.activePlayer == self.player1 and self.printing:
						self.printPassiveHand()
						self.printGameState()
						self.printHand()		
						print(self.evaluateState())
						time.sleep(5)
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
					# print ("======== YOUR TURN ========")
					self.nextTurn()
					
					# Gjør det heller lett
				else:
					# print("{}'s turn".format(self.activePlayer.getName()))
					if self.activePlayer.getDeck().getRemaining()>0:
						self.draw(1,"a")
					self.updateContinousEffects()
					prnt = True
					while True:
						if prnt:
							self.printPassiveHand()
							self.printGameState()
							self.printHand()
							print(self.evaluateState())
						prnt = True
						if not self.canDoSomething():
							print ("**** You have no more possible actions ****")
						try:
							if self.canAttack() and self.canPlayCard():
								action = self.getInput("Write 'p' to play a card, 'a' to attack or 'e' to end turn: ")
							elif self.canAttack():
								action = self.getInput("Write 'a' to attack or 'e' to end turn: ")
							elif self.canPlayCard():
								action = self.getInput("Write 'p' to play a card or 'e' to end turn: ")
							else:
								action = self.getInput("Write 'e' to end turn: ")
							if action == "p":
								print("\nYou have ** {} ** mana".format(self.activePlayer.currentMana))
								self.printPlayableCards(self.activePlayer)
								canPlayCard = False
								for card in self.activePlayer.hand:
									if card.cost <= self.activePlayer.currentMana:
										canPlayCard = True
								if canPlayCard:
									cardToPlay = input("Which card do you want to play? ('a' to abort) ")

									if cardToPlay != "a" and not cardToPlay=="":
										legalnumbers=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
										if int(cardToPlay) in legalnumbers:
											if int(cardToPlay) < (len(self.activePlayer.hand)):
												if not self.playCard(cardToPlay):
													prnt=False
												else:
													prnt=True
											else:
												prnt=False
												print("You entered a number that was too high")
									else:
										print("Aborting attack")
								else: 
									print("****You don't have enough mana to play any cards****")
									prnt=False
							if action =="quit":
								gameOver = True
								break
							if action =="e":
								# print ("\n\n\n\n\n======== AI's TURN ========")
								break
							if action[0] =="a":

								if len(action)>1 and int(action[1])>=0 and int(action[1])<len(self.activePlayer.activeMinions):
									if len(action)>2 and action[2]=="f":
										self.attackFace(self.activePlayer.activeMinions[int(action[1])])
										print("attacked face")
									elif len(action)>2 and int(action[2])>=0 and int(action[2])<len(self.passivePlayer.activeMinions):
										self.attackMinion(self.activePlayer.activeMinions[int(action[1])],int(action[2]))
										print("attacked minion")
								
								elif self.canAttack():
									self.printAttackReadyMinions()
									attacker = int(input("What index do you want to attack with?: "))
									if attacker >= len(self.activePlayer.activeMinions):
										print("\nThat index was too high")

									else:
										taunts = []
										for minion in self.passivePlayer.activeMinions:
											if minion.hasTaunt:
												taunts.append(minion)
										aMin = self.activePlayer.getActiveMinions()[attacker]
										self.printPossibleTargetsOfMinion(aMin)
										target = input("Which minion do you want to attack? ('f' for face): ")
										print("")
										
										if len(taunts)>0:
											if(target=="f"):
												pass
												# print("You need to target a minion with taunt")
											else:
												if not self.passivePlayer.activeMinions[int(target)].hasTaunt:
													# print("You need to target a minion with taunt")
													print(aMin.name,aMin.hasTaunt,attacker)
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
							elif action =="d":
								self.printDetails()
								prnt=False
						except:
							print("USER ERROR!")
							print("You entered a value that was not good")
							prnt=False
					# self.activePlayer.doAction()
					roundDone=True
			self.nextTurn()

	def titt(self,player,amount):
		if self.activePlayer.AI==False:
			for i in range(amount):
				print(player.deck.cards[-1-i])