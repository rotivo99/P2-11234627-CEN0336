#!/usr/bin/env python3

total = 0 #Variável para armazenar o total da soma das notas
contador_notas = 0 #Variável para armazenar o número de notas somadas.

while contador_notas < 10: #Enquanto o número de notas for menor que 10...
	try: #Tentar
		user_input = int(input('Insira a nota: ')) #Pedido para o usuário inserir os valores dele. Entra como string, mas para fazer operações, precisa estar com int().
		if int(user_input) <= 10 and int(user_input) >= 0: #Se o input for menor ou igual a 10 e maior ou igual a 0...
			contador_notas += 1 #Acrescentar 1 ao contador_notas.
			total += int(user_input) #E o valor inserido ao total.
		else: #Caso contrário...
			print('O número inserido precisa ser positivo e menor ou igual a 10.') #Enviar essa mensagem ao usuário.
			continue #Continuar pedindo por números.
	except ValueError: #Exceto se der esse erro.
		print('O dado inserido necessita ser um valor numérico inteiro.') #Enviar essa mensagem ao usuário.
		continue #Continuar pedindo por mais números ao usário.
media = total/10 #Calculando a média.
print(media) #Mostrando a média obtida na tela.
