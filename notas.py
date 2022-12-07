#!/usr/bin/env python3

total = 0 #Defina TOTAL com zero.
contador_notas = 0 #Defina CONTADOR NOTAS como zero.

while contador_notas <= 10: #While CONTADOR NOTAS é menor ou igual a dez.
    user_input = input('Insira a nota: ') #Entre (input) a seguinte nota.
    total += user_input #Some a nota ao TOTAL.
media = total/10 #Defina a média da disciplina como o TOTAL dividido por dez (TOTAL/10).
print(media) #Imprima na tela a média da disciplina.
