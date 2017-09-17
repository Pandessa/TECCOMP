import sys, pygame
import random
import time
from operator import attrgetter

CORTUBARAO = 255
CORPEIXE   = 255
FPS        = 10


NUM_CELULAS = 64
PRETO       = (0, 0, 0)
PASSO       = 21

# Tipos de movimento
ESCAPE    = 1
ALEATORIO = 0
ATAQUE    = 2

DIR   = 1
ESQ   = 2
CIMA  = 3
BAIXO = 4

RASTRO  = (0,0,CORTUBARAO)
RASTROP = (CORPEIXE,0,0)

matrizLogica   = [ [ None for i in range(64) ] for j in range(64) ]
futurosLideres = []

class Presa():
	
	def __init__(self, vida, reproducao, percepcao, lider):

		self.vida 			= vida
		self.reproducao 	= reproducao
		self.percepcao		= percepcao
		self.lider 			= lider

class Predador():

	def __init__(self, vida, reproducao, percepcao, lider):

		self.vida 		= vida
		self.reproducao = reproducao
		self.percepcao	= percepcao
		self.lider 		= lider

class Rastro():

	def __init__(self, presa):
		self.duracao = 10
		self.presa   = presa

class Tela(object):

	def __init__(self):

		#pega tamanho da tela automaticamente
		#self.displayInfo = pygame.display.Info()
		#self.tela = pygame.display.set_mode((self.displayInfo.current_w,self.displayInfo.current_h))

		self.larguraTela = 768
		self.alturaTela = 640

		self.tela = pygame.display.set_mode((self.larguraTela,self.alturaTela))

		#calcula largura e altura ideal da rect do peixe e do tubarao conforme dimensao da tela 
		self.larguraRect = self.larguraTela//NUM_CELULAS
		self.alturaRect = self.alturaTela//NUM_CELULAS

		print("larg x altura")
		print(self.larguraRect)
		print(self.alturaRect)

		#carrega imagem peixe
		self.peixe = pygame.image.load("p.png")

		#carrega imagem peixeLider
		self.peixeLider = pygame.image.load("peixeLider.png")
		self.peixeLider = pygame.transform.scale(self.peixeLider,(self.larguraRect,self.alturaRect))

		#carrega imagem tubaraoLider
		self.tubaraoLider = pygame.image.load("tLider.png")
		self.tubaraoLider = pygame.transform.scale(self.tubaraoLider,(self.larguraRect,self.alturaRect))

		#redimensiona imagem conforme largura/altura definida da rect
		self.peixe = pygame.transform.scale(self.peixe,(self.larguraRect,self.alturaRect))
		
		#carrega imagem tubarao
		self.tubarao = pygame.image.load("t.png")
		#redimensiona imagem conforme largura/altura da tela e numero de celulas desejado
		self.tubarao = pygame.transform.scale(self.tubarao,(self.larguraRect,self.alturaRect))

		pygame.display.set_caption('Presa-predador')

	def blitarJogo(self,matrizLogica):
		for i in range(NUM_CELULAS):
			for j in range(NUM_CELULAS):

				if type(matrizLogica[i][j]) == None or matrizLogica[i][j] is None:

					pygame.draw.rect(self.tela,PRETO,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))
					#print("to no none")

				elif type(matrizLogica[i][j]) == Presa or matrizLogica[i][j] is Presa:

					if(matrizLogica[i][j].lider):
						self.tela.blit(self.peixeLider,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

					else:
						self.tela.blit(self.peixe,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == Predador or matrizLogica[i][j] is Predador:

					if(matrizLogica[i][j].lider):
						self.tela.blit(self.tubaraoLider,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))
					else:
						self.tela.blit(self.tubarao,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) is Rastro and matrizLogica[i][j].presa == False:
					pygame.draw.rect(self.tela,RASTRO,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) is Rastro and matrizLogica[i][j].presa:
					pygame.draw.rect(self.tela,RASTROP,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				

class Game(object):

	def decrementarRastro(self,matrizLogica,i,j):

		global CORPEIXE
		global CORTUBARAO

		if type(matrizLogica[i][j]) == Rastro:
			matrizLogica[i][j].duracao -= 1

			if matrizLogica[i][j].duracao == 0:
				matrizLogica[i][j] = None

			elif matrizLogica[i][j].presa:

				if CORPEIXE >= 50:
					CORPEIXE = CORPEIXE - 50

			elif matrizLogica[i][j].presa == False:
				
				if CORTUBARAO >= 50:
					CORTUBARAO = CORTUBARAO - 50

	def moverAgentes(self,matrizLogica):
		for i in range(NUM_CELULAS):
			for j in range(NUM_CELULAS):

				if type(matrizLogica[i][j]) == Presa or type(matrizLogica[i][j]) == Predador:
					eixo = random.choice('xy')
					sit = random.choice('+-')
					

					if matrizLogica[i][j].lider == True and self.alcance(matrizLogica, i, j) == (ESCAPE,CIMA):
						if i > 0:
							if matrizLogica[i-1][j] is None:

								matrizLogica[i-1][j] = matrizLogica[i][j]
								matrizLogica[i][j]	 = Rastro(True)

						elif i == 0:

							if matrizLogica[NUM_CELULAS-1][j] is None:

								matrizLogica[NUM_CELULAS-1][j] = matrizLogica[i][j]							
								matrizLogica[i][j] = Rastro(True)

					elif matrizLogica[i][j].lider == True and self.alcance(matrizLogica, i, j) == (ESCAPE,BAIXO):
						if i < NUM_CELULAS-1:

							if matrizLogica[i+1][j] is None:

								matrizLogica[i+1][j] = matrizLogica[i][j]
								matrizLogica[i][j] 	 = Rastro(True)

						elif i == NUM_CELULAS - 1:

							if matrizLogica[0][j] is None:

								matrizLogica[0][j] = matrizLogica[NUM_CELULAS-1][j]
								matrizLogica[NUM_CELULAS-1][j] = None #Rastro(True)

					elif matrizLogica[i][j].lider == True and self.alcance(matrizLogica, i, j) == (ESCAPE, ESQ):
						if j > 0:

							if matrizLogica[i][j-1] is None:

								matrizLogica[i][j-1] = matrizLogica[i][j]
								matrizLogica[i][j] 	 = Rastro(True)

						elif j == 0:

							if matrizLogica[i][NUM_CELULAS-1] is None:

								matrizLogica[i][NUM_CELULAS-1] = matrizLogica[i][j]
								matrizLogica[i][j] = Rastro(True)

					elif matrizLogica[i][j].lider == True and self.alcance(matrizLogica, i, j) == (ESCAPE, DIR):
						if j < NUM_CELULAS-1:

							if matrizLogica[i][j+1] is None:

								matrizLogica[i][j+1] = matrizLogica[i][j]
								matrizLogica[i][j] 	 = Rastro(True)

						elif  j == NUM_CELULAS-1:

							if matrizLogica[i][0] is None:
								
								matrizLogica[i][0] = matrizLogica[i][NUM_CELULAS-1]
								matrizLogica[i][NUM_CELULAS-1] = Rastro(True)



 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  TUBARÃO  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


					elif self.alcance(matrizLogica, i, j) == (ATAQUE,CIMA):
						
						if i > 0:

							tipo 		= type(matrizLogica[i-1][j]) # TALVEZ NAO PRECISE DO TIPO
							elemento 	= matrizLogica[i-1][j]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO

							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i-1][j] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j]	 = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None


						elif i == 0:

							elemento 	= matrizLogica[NUM_CELULAS-1][j] # PRA FICAR MAIS EFICIENTE E
																	     # NAO PRECISAR ACESSAR A MATRIZ DE NOVO

							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[NUM_CELULAS-1][j] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j]	 = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None

					elif self.alcance(matrizLogica, i, j) == (ATAQUE,BAIXO):
						if i < NUM_CELULAS-1:

							elemento 	= matrizLogica[i+1][j]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i+1][j] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j]	 = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None

						elif i == NUM_CELULAS - 1:

							elemento 	= matrizLogica[0][j]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[0][j] = matrizLogica[NUM_CELULAS-1][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[NUM_CELULAS-1][j] = Rastro(False)
								else: 
									matrizLogica[NUM_CELULAS-1][j]	 = None
								

					elif self.alcance(matrizLogica, i, j) == (ATAQUE, ESQ):
						if j > 0:

							elemento 	= matrizLogica[i][j-1]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i][j-1] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j] = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None

						elif j == 0:

							elemento 	= matrizLogica[i][NUM_CELULAS-1] # PRA FICAR MAIS EFICIENTE E
																	     # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i][NUM_CELULAS-1] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j] = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None

					elif self.alcance(matrizLogica, i, j) == (ATAQUE, DIR):
						if j < NUM_CELULAS-1:

							elemento 	= matrizLogica[i][j+1]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i][j+1] = matrizLogica[i][j]

								if matrizLogica[i][j].lider == True:
									matrizLogica[i][j] = Rastro(False)
								else: 
									matrizLogica[i][j]	 = None

						elif  j == NUM_CELULAS-1:

							elemento 	= matrizLogica[i][0]		 # PRA FICAR MAIS EFICIENTE E
																	 # NAO PRECISAR ACESSAR A MATRIZ DE NOVO
							if type(elemento) is None or type(elemento) is Presa:

								# SE O LIDER MORRER, SUBSTITUI ELE

								if type(elemento) is Presa and elemento.lider:

									print("VOU TROCAR DE LIDER")
									for peixe in futurosLideres:
										if peixe is elemento:
											futurosLideres.remove(elemento)

									if len(futurosLideres) > 0:
										futurosLideres[0].lider = True
										print("TROQUEI DE LIDER")

								matrizLogica[i][0] 			   = matrizLogica[i][NUM_CELULAS-1]

								if matrizLogica[i][j].lider == True:
									matrizLogica[NUM_CELULAS-1][j] = Rastro(False)
								else: 
									matrizLogica[NUM_CELULAS-1][j]	 = None

					else:
						#print("NÃO TO ESCAPANDO DE NGM")

						colisao(matrizLogica,i,j)

						if (type(matrizLogica[i][j]) is Presa or type(matrizLogica[i][j]) is Predador) and matrizLogica[i][j].lider:
							self.andar(matrizLogica, eixo, sit, i, j)

						elif (type(matrizLogica[i][j]) is Presa or type(matrizLogica[i][j]) is Predador) and matrizLogica[i][j].lider == False:
							if self.seguir(matrizLogica,i,j) == False:
								self.andar(matrizLogica, eixo, sit, i, j)
								
									
								
									

				# DECREMENTA O RASTRO 

				elif type(matrizLogica[i][j]) is Rastro:
					self.decrementarRastro(matrizLogica,i,j)


	def alcance(self,matrizLogica,i,j):

		l = i 
		c = j

		if type(matrizLogica[l][c]) is Presa:

			agente 	= type(matrizLogica[l][c])
			perc 	= matrizLogica[l][c].percepcao

		else:

			agente 	= type(matrizLogica[l][c])
			perc 	= matrizLogica[l][c].percepcao

		itCol = 0
		itLin = 0

		#itera colunas para a direita
		while c < NUM_CELULAS -1 and itCol < perc:

			if c != j:

				if type(matrizLogica[l][c]) is Predador and agente is Presa:
					return ESCAPE,ESQ
				elif type(matrizLogica[l][c]) is Presa and agente is Predador:
					return ATAQUE,DIR
				else:
					c+=1
					itCol+=1
			else:
				c+=1
					

		itCol = 0
		c = j

		#itera colunas para a esquerda
		while c > 0 and itCol < perc:
			if c != j:
				if type(matrizLogica[l][c]) is Predador and agente is Presa:
					return ESCAPE,DIR
				elif type(matrizLogica[l][c]) is Presa and agente is Predador:
					return ATAQUE,ESQ
				else:
					c-=1
					itCol+=1
			else:
				c-=1


		#itera linha para baixo
		while l < NUM_CELULAS -1 and itLin < perc:

			if l != i:
				if type(matrizLogica[l][c]) is Predador and agente is Presa:
					return ESCAPE,CIMA
				elif type(matrizLogica[l][c]) is Presa and agente is Predador:
					return ATAQUE,BAIXO
				else:
					l+=1
					itLin+=1
			else:
				l+=1

		itLin = 0
		l = i

		#itera linha para cima
		while l > 0 and itLin < perc:
			if l != i:
				if type(matrizLogica[l][c]) is Predador and agente is Presa:
					return ESCAPE,BAIXO
				elif type(matrizLogica[l][c]) is Presa and agente is Predador:
					return ATAQUE,CIMA
				else:
					l-=1
					itLin+=1
			else:
				l-=1

		return ALEATORIO
	
	def andar(self, matrizLogica, eixo, sit, i, j):

		# SE TEM UMA CÉLULA VAZIA, ADICIONO UM RASTRO. SE JÁ TIVER UM RASTRO, LIMPO A CÉLULA. 
	
		if eixo == 'x' and sit == '+':
					
			if  j < NUM_CELULAS - 1:
				if matrizLogica[i][j+1] is None: 
					matrizLogica[i][j+1] = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif matrizLogica[i][j+1] is Rastro:
					matrizLogica[i][j+1] = None

			elif  j == NUM_CELULAS-1:

				if matrizLogica[i][0] is None:
					matrizLogica[i][0] 			   = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][NUM_CELULAS-1] = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif matrizLogica[i][0] is Rastro:
					matrizLogica[i][0] 			   = None

		elif eixo == 'x' and sit == '-':
			
			if j > 0:
				if matrizLogica[i][j-1] is None: 
					matrizLogica[i][j-1] = matrizLogica[i][j]

					# ESPECIFICA DE QUEM É O RASTRO DEIXADO

					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif matrizLogica[i][j-1] is Rastro:
					matrizLogica[i][j-1] = None
					#matrizLogica[i][j] 	 = None

			elif j == 0:
				if matrizLogica[i][NUM_CELULAS-1] is None:
					matrizLogica[i][NUM_CELULAS-1] = matrizLogica[i][j]

					# ESPECIFICA DE QUEM É O RASTRO DEIXADO


					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 			   = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 		   = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif matrizLogica[i][NUM_CELULAS-1] is Rastro:
					matrizLogica[i][NUM_CELULAS-1] = None


		elif eixo == 'y' and sit == '+':
		
			if  i < NUM_CELULAS - 1:	
				if matrizLogica[i+1][j] is None: 
					matrizLogica[i+1][j] = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				if matrizLogica[i+1][j] is Rastro:
					matrizLogica[i+1][j] = None

			elif i == NUM_CELULAS - 1:
				if matrizLogica[0][j] is None:
					matrizLogica[0][j] = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif matrizLogica[0][j] is Rastro:
					matrizLogica[0][j] = None

		elif eixo == 'y' and sit == '-':
	

			if i > 0:
				if matrizLogica[i-1][j] is None: 
					matrizLogica[i-1][j] = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(True)
					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif type(matrizLogica[i-1][j]) is Rastro:
					matrizLogica[i-1][j] = None


			elif i == 0:
				if matrizLogica[NUM_CELULAS-1][j] is None:
					matrizLogica[NUM_CELULAS-1][j] = matrizLogica[i][j]
					if type(matrizLogica[i][j]) is Presa and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 			   = Rastro(True)

					elif type(matrizLogica[i][j]) is Predador and matrizLogica[i][j].lider == True:
						matrizLogica[i][j] 	 	      = Rastro(False)
					else:
						matrizLogica[i][j] = None

				elif type(matrizLogica[NUM_CELULAS-1][j]) is Rastro:
					matrizLogica[NUM_CELULAS-1][j] = None


	def seguir(self,matrizLogica,i,j):


		l = i 
		c = j

		#if type(matrizLogica[l][c]) is Presa or type(matrizLogica[l][c]) is Predador:

		agente 	= type(matrizLogica[l][c])
		perc 	= matrizLogica[l][c].percepcao

		'''else:

			agente 	= type(matrizLogica[l][c])
			perc 	= matrizLogica[l][c].percepcao'''

		itCol = 0
		itLin = 0

		#itera colunas para a direita
		while c < NUM_CELULAS -1 and itCol < perc:

			if c != j:

				if type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa  and agente is Presa:
					
					if matrizLogica[i][j+1] is None:
						matrizLogica[i][j+1] = matrizLogica[i][j]
						matrizLogica[i][j] = None

						#print("wl 1.1")
						return True
					else:
						return False

				elif type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa == False and agente is Predador:
					
					if matrizLogica[i][j+1] is None:
						matrizLogica[i][j+1] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 1.2")
						return True
					else:
						return False
				else:
					c+=1
					itCol+=1
			else:
				c+=1
					

		itCol = 0
		c = j

		#itera colunas para a esquerda
		while c > 0 and itCol < perc:
			if c != j:
				if type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa  and agente is Presa:
					
					if matrizLogica[i][j-1] is None:
						matrizLogica[i][j-1] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						return True
					else:
						return False
				elif type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa == False and agente is Predador:
					
					if matrizLogica[i][j-1] is None:
						matrizLogica[i][j-1] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 2.2")
						return True

					else:
						return False
				else:
					c-=1
					itCol+=1
			else:
				c-=1


		#itera linha para baixo
		while l < NUM_CELULAS -1 and itLin < perc:

			if l != i:
				if type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa  and agente is Presa:
					
					if matrizLogica[i+1][j] is None:
						matrizLogica[i+1][j] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 3.1")
						return True
					else:
						return False
				elif type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa == False and agente is Predador:
					if matrizLogica[i+1][j] is None:
						matrizLogica[i+1][j] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 3.2")
						return True
					else:
						return False
				else:
					l+=1
					itLin+=1
			else:
				l+=1

		itLin = 0
		l = i

		#itera linha para cima
		while l > 0 and itLin < perc:
			if l != i:
				if type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa  and agente is Presa:
					
					if matrizLogica[i-1][j] is None:
						matrizLogica[i-1][j] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 4.1")
						return True
					else:
						return False
				
				elif type(matrizLogica[l][c]) is Rastro and matrizLogica[l][c].presa == False and agente is Predador:
					if matrizLogica[i-1][j] is None:
						matrizLogica[i-1][j] = matrizLogica[i][j]
						matrizLogica[i][j] = None
						#print("wl 4.2")
						return True
					else:
						return False
				else:
					l-=1
					itLin+=1
			else:
				l-=1

		return False	

# # # # # # NOVA FUNÇÃO # # # # # # #

def colisao(matrizLogica,i,j):

# SEMPRE PASSO O CARA DA PONTA DIREITA PRA FUNÇÃO REPRODUZIR

	if type(matrizLogica[i][j]) is Presa or type(matrizLogica[i][j]) is Predador:

		# VERIFICO A COLUNA A DIREITA
		if  j+1 < NUM_CELULAS:
			if type(matrizLogica[i][j]) is type(matrizLogica[i][j+1]):

				return(reproduzir(i,j+1, matrizLogica[i][j], matrizLogica[i][j+1], type(matrizLogica[i][j])))

		# VERIFICO A LINHA DE CIMA
		elif i+1 < NUM_CELULAS:
			if type(matrizLogica[i][j]) is type(matrizLogica[i+1][j]):

				return(reproduzir(i+1,j, matrizLogica[i][j], matrizLogica[i+1][j],type(matrizLogica[i][j])))

		# VERIFICO A LINHA DE BAIXO
		elif i-1 >= 0:
			if type(matrizLogica[i][j]) is type(matrizLogica[i-1][j]):

				return(reproduzir(i,j,matrizLogica[i][j], matrizLogica[i-1][j],type(matrizLogica[i][j])))

		# VERIFICO A COLUNA A ESQUERDA
		elif j-1 >= 0:
			if type(matrizLogica[i][j]) is type(matrizLogica[i][j-1]):

				return(reproduzir(i,j,matrizLogica[i][j],matrizLogica[i][j-1],type(matrizLogica[i][j])))

		else:
			return False


# VERIFICAR SE DUAS POSIÇÕES À DIREITA, EMBAIXO E EM CIMA ESTÃO LIVRES
# VERIFICAR BORDAS
# FAZER FUNÇÃO PRA VER SE 2 PEIXES ESTÃO UM AO LADO DO OUTRO PARA REPRODUZIR ("COLISÃO")
def reproduzir(i,j,agente1, agente2, tipoFilhote):

	maduro = 2
	global matrizLogica
	count  = 1
	linha  = i
	coluna = j
	retorno = False
	global futurosLideres

	if agente1.reproducao >= maduro and agente2.reproducao >= maduro:

		# VERIFICO 2 COLUNAS A DIREITA

		while count <= 2 and coluna+1 < NUM_CELULAS-1:
			coluna+=1
			if matrizLogica[i][coluna] is None:

				if tipoFilhote is Presa:

					# ADICIONO FILHOTE NA LISTA DE FUTUROS LÍDERES E DEPOIS A ORDENO

					matrizLogica[i][coluna] = Presa(random.randint(1,5),random.randint(1,3),10,False)
					futurosLideres.append(matrizLogica[i][coluna])
					futurosLideres = sorted(futurosLideres, key=attrgetter('vida'), reverse=True)

					#print("REPRODUZI PEIXE")
					return True


				elif tipoFilhote is Predador:
					matrizLogica[i][coluna] = Predador(random.randint(1,5),random.randint(1,3),50,False)

					#print("REPRODUZI PREDADOR")
					return True
						
			else:
				count=+1

		count  = 1
		coluna = j
		linha  = i

		# VERIFICO 2 LINHAS ABAIXO

		count  = 1
		coluna = j
		linha  = i

		while count <= 2 and linha+1 < NUM_CELULAS-1:
			linha+=1
			if matrizLogica[linha][j] is None:

				if tipoFilhote is Presa:

					matrizLogica[linha][j] = Presa(random.randint(1,5),random.randint(1,3),10,False)
					futurosLideres.append(matrizLogica[linha][j])
					futurosLideres = sorted(futurosLideres, key=attrgetter('vida'), reverse=True)

					#print("REPRODUZI PEIXE")
					return True

				elif tipoFilhote is Predador:
					matrizLogica[linha][j] = Predador(random.randint(1,5),random.randint(1,3),50,False)
					
					#print("REPRODUZI PREDADOR")
					return True
			else:
				count+=1

		# VERIFICO 2 LINHAS ACIMA

		count  = 1
		coluna = j
		linha  = i

		while count <= 2 and linha-1 > 0:
			linha-=1
			if matrizLogica[linha][j] is None:

				if tipoFilhote is Presa:

					matrizLogica[linha][j] = Presa(random.randint(1,5),random.randint(1,3),10,False)
					futurosLideres.append(matrizLogica[linha][j])
					futurosLideres = sorted(futurosLideres, key=attrgetter('vida'), reverse=True)

					#print("REPRODUZI PEIXE")
					return True

				elif tipoFilhote is Predador:
					matrizLogica[linha][j] = Predador(random.randint(1,5),random.randint(1,3),50,False)

					#print("REPRODUZI PREDADOR")
					return True
			else:
				count+=1

	return False

def inicializaMatriz():

	#matriz logica
	arquivo = open('mapa2.txt','r')
	conteudoArquivo = arquivo.read()
	linhas = conteudoArquivo.split('\n')
	
	
	#print(matrizLogica)
	liderPeixe = None
	liderTubarao = None
	posLider = [-1,-1]
	posTub	 = [-1,-1]
	global futurosLideres

	for i,linha in enumerate(linhas):

		splitEspaco = linha.split(' ')

		for j,coluna in enumerate(splitEspaco):

			if coluna == '1':

				matrizLogica[i][j] = Presa(random.randint(1,5),random.randint(1,3),10,False)
				futurosLideres.append(matrizLogica[i][j])
				#print("Vida peixe [", i,"]","[",j,"]","=",matrizLogica[i][j].vida)

				if posLider[0] == -1 and posLider[1] == -1:

					#liderPeixe = matrizLogica[i][j]
					posLider[0] = i
					posLider[1] = j
					matrizLogica[i][j].lider = True
					

				elif matrizLogica[posLider[0]][posLider[1]].vida < matrizLogica[i][j].vida:

					#liderPeixe = matrizLogica[i][j]
					matrizLogica[posLider[0]][posLider[1]].lider = False
					posLider[0] = i
					posLider[1] = j
					matrizLogica[i][j].lider = True

			elif coluna == '2':

				matrizLogica[i][j] = Predador(random.randint(1,5),random.randint(1,3),50, False)
				
				if posTub[0] == -1 and posTub[1] == -1:

					#liderPeixe = matrizLogica[i][j]
					posTub[0] = i
					posTub[1] = j
					matrizLogica[i][j].lider = True

				elif matrizLogica[posTub[0]][posTub[1]].vida < matrizLogica[i][j].vida:

					#liderPeixe = matrizLogica[i][j]
					matrizLogica[posTub[0]][posTub[1]].lider = False
					posTub[0] = i
					posTub[1] = j
					matrizLogica[i][j].lider = True

		# ORDENA LIDERES PELA IDADE (DECRESCENTE)
		futurosLideres = sorted(futurosLideres, key=attrgetter('vida'), reverse=True)
	
	print("Posicao do peixe lider = [",posLider[0],"]","[",posLider[1],"]")
	print("Peixe Lider:", matrizLogica[posLider[0]][posLider[1]].lider)
	print("Peixe Lider - vida:", matrizLogica[posLider[0]][posLider[1]].vida)
	print("Peixe Lider - Percepcao:", matrizLogica[posLider[0]][posLider[1]].percepcao)
	print("Lider atual", futurosLideres[0].vida, futurosLideres[0].lider)
	print("Futuro Lider", futurosLideres[1].vida, futurosLideres[1].lider)


def main():

	inicializaMatriz()

	#inicilizando pygame
	pygame.init()

	#criando tela
	t1 = Tela()
	g1 = Game()

	last_time = time.time()
	
	loop = 1
	while(loop):

		

		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				loop = 0

		new_time = time.time()

		sleep_time = ((1000.0 / FPS) - (new_time - last_time)) / 1000.0

		if sleep_time > 0:
			time.sleep(sleep_time)
		last_time = new_time	

		g1.moverAgentes(matrizLogica)
		t1.blitarJogo(matrizLogica)
		pygame.display.update()
	pygame.quit()
	quit()
	

if __name__ == '__main__':
	main()