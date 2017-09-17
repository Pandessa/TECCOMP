class pessoa ():
	def __init__(self, nome):
		self.nome = nome


p1 = pessoa("Fulano")
p2 = pessoa("Ciclano")

vetor = []
matriz = [ [ 0 for i in range(5) ] for j in range(5) ]


i = 2
j = 2

'''for linha in range(i,j+3):
	for coluna in range(j,i+2):
		print("[",linha,"]","[",coluna,"]","=", matriz[linha][coluna])
'''

for obj in vetor:
	print("deu pau?")