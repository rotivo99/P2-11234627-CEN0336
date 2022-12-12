#!/usr/bin/env python3

import os, sys, re, time
from Bio.Seq import Seq

start = time.process_time()

multifasta_file = sys.argv[1] #Pedindo para o usuário o arquivo que será processado.

if os.path.exists(multifasta_file): #Se o arquivo existir...
    print('File found. Continuing...') #Avise o usuário que tudo certo.
    with open(multifasta_file, 'r') as sys_read, open('ORF.fna', 'w') as nucleotide_write, open('ORF.faa', 'w') as peptide_write:
        nucleotide_dictionary = {} #Criando um dicionário para as sequências de nucleotídeos.
        for line in sys_read: #Para cada linha no arquivo inserido pelo usuário...
            if line.startswith('>'): #Se ela começar com >
                new_line = line.rstrip().split(' ').pop(0).replace('>', '') #Vai quebrar elas nos espaços para conseguir retirar o primeiro item com o pop e retirar o > para colocar no dicionário depois.
                nucleotide_dictionary[new_line] = {} #Criando um dicionário dentro de um dicionário, sendo que a chave para esse segundo dicionário vai ser a sequência produzida na linha anterior.
                full_sequence_line = '' #Criando uma string para armazenar as sequências depois. É importante que ela fique aqui, porque eu quero que toda vez que uma nova sequência com > for encontrada, que ela zere para não misturar sequências diferentes.
            else: #Caso a linha não começe com >
                full_sequence_line += ''.join(line.rstrip()) #Vamos juntar as linhas de uma mesma tag que tá separada em várias linhas.
                for ORF1_search in re.finditer(r'(([ATGC]{3})+)', full_sequence_line, re.I): #Para cada leitura aberta no primeiro frame.
                    ORF1_sequence = full_sequence_line[ORF1_search.start(1):ORF1_search.end(1)] #Isolando a sequência.
                    nucleotide_dictionary[new_line]['ORF1'] = ORF1_sequence #Colocando ela no dicionário.
                    ORF1_reverse_complement = ORF1_sequence.replace('A', 't').replace('T', 'a').replace('C',  'g').replace('G', 'c').upper() #Criando a sequência complementar.
                    nucleotide_dictionary[new_line]['ORF1_rc'] = ORF1_reverse_complement #Colocando ela no dicionário.
                for ORF2_search in re.finditer(r'\w(([ATGC]{3})+)', full_sequence_line, re.I): #Segunda fase aberta de leitura.
                    ORF2_sequence = full_sequence_line[ORF2_search.start(1):ORF2_search.end(1)]
                    nucleotide_dictionary[new_line]['ORF2'] = ORF2_sequence
                    ORF2_reverse_complement = ORF2_sequence.replace('A', 't').replace('T', 'a').replace('C',  'g').replace('G', 'c').upper()
                    nucleotide_dictionary[new_line]['ORF2_rc'] = ORF2_reverse_complement
                for ORF3_search in re.finditer(r'\w{2}(([ATGC]{3})+)', full_sequence_line, re.I): #Terceira fase aberta de leitura.
                    ORF3_sequence = full_sequence_line[ORF3_search.start(1):ORF3_search.end(1)]
                    nucleotide_dictionary[new_line]['ORF3'] = ORF3_sequence
                    ORF3_reverse_complement = ORF3_sequence.replace('A', 't').replace('T', 'a').replace('C',  'g').replace('G', 'c').upper()
                    nucleotide_dictionary[new_line]['ORF3_rc'] = ORF3_reverse_complement
        protein_dictionary = {} #Criando um dicionário para as proteínas.
        peptide_exception_dictionary = {} #Criando um dicionário para as sequências de proteínas inválidas.
        nucleotide_exception_dictionary = {} #Criando um dicionário para as sequências de nucleotídeos que não codam para nada.
        for gene_tag, ORF_dict in nucleotide_dictionary.items(): #Abrindo os itens do dicionário externo de nucleotídeos.
            protein_dictionary[gene_tag] = {} #Criando um dicionário dentro do dicionário de proteínas.
            for ORF_key, ORF_seq in ORF_dict.items(): #Abrindo os itens do dicionário interno de nucleotídeos.
                ORF_coding_region = Seq(ORF_seq) #Para o BioPython funcionar, a sequência tem que estar envolvida por Seq().
                ORF_protein = str(ORF_coding_region.translate()) #Traduzindo e transformando o resultado obtido em string.
                try: #Tentar
                    CDS_regex = re.search(r'M.+\*', ORF_protein) #Encontrar uma região válida na proteína inteira traduzida.
                    coding_sequence = ORF_protein[CDS_regex.start():CDS_regex.end()] #Separando a região válida.
                    protein_dictionary[gene_tag][ORF_key] = coding_sequence #Colocando no dicionário de proteínas.
                    peptide_write.write(f'>{gene_tag}_frame{ORF_key[3:7]}_{CDS_regex.start()+1}_{CDS_regex.end()}\n') #Criando tag para arquivo contendo as proteínas.
                    peptide_write.write(f'{coding_sequence}\n') #Sequência de proteínas.
                    nucleotide_write.write(f'>{gene_tag}_frame{ORF_key[3:7]}_{CDS_regex.start()*3-2}_{CDS_regex.end()*3}\n') #Criango tag para arquivo contendo os nucleotídeos.
                    nucleotide_write.write(f'{nucleotide_dictionary[gene_tag][ORF_key]}\n') #Sequência de nucleotídeos.
                except AttributeError: #Se der esse erro.
                    peptide_exception_dictionary[f'{gene_tag}_frame{ORF_key[3:7]}'] = ORF_protein #Armazenar os valores com problemas no dicionário de peptídeos inválidos.
                    nucleotide_exception_dictionary[f'{gene_tag}_frame{ORF_key[3:7]}'] = ORF_seq #Armazenar os valores com problemas no dicionário de nucleotídeos inválidos.
        print('Do you want to save invalid sequences in your files?') #Perguntando ao usuário se ele quer salvar os valores inválidos no arquivo final.
        user_exception_input = input('Answer with Yes or No: ').lower().capitalize() #Capturando o input e corrigindo para ficar do jeito certo.
        while user_exception_input != 'Yes' or user_exception_input != 'No': #Enquanto o input for diferente de sim ou não, esse bloco abaixo vai rodar...
            if user_exception_input == 'Yes': #Se o input for sim.
                if peptide_exception_dictionary != {} and nucleotide_exception_dictionary != {}: #Se os dicionários com as exceções não estiverem vazios...
                    peptide_write.write('\nThe following invalid aminoacid sequences were found in your file:\n') #Isso e...
                    nucleotide_write.write('\nThe following invalid nucleotide sequences were found in your file:\n') #isso vai ser acrescentado.
                else: #Caso contrário...
                    peptide_write.write('\nNo invalid aminoacid sequences were found.\n') #Isso e...
                    nucleotide_write.write('\nNo invalid nucleotide sequences were found.\n') #isso vai ser acrescentado.
                for exception_tag, exception_value in peptide_exception_dictionary.items(): #Abrindo os itens do dicionário de peptídeos.
                    peptide_write.write(f'>{exception_tag}\n')
                    peptide_write.write(f'{exception_value}\n')
                for nucleotide_exception_tag, nucleotide_exception_value in nucleotide_exception_dictionary.items(): #Abrindo os itens do dicionário de nucleotídeos.
                    nucleotide_write.write(f'>{nucleotide_exception_tag}\n')
                    nucleotide_write.write(f'{nucleotide_exception_value}\n')
                print('Output files \'ORF.fna\' and \'ORF.faa\' were generated.') #Mensagem para o usuário avisando sobre os arquivos gerados.
                end = time.process_time()
                time = end - start
                print('CPU Execution time:', time, 'seconds.')
                break
            elif user_exception_input == 'No': #Se o input for não.
                print('Output files \'ORF.fna\' and \'ORF.faa\' were generated.') #Mensagem para o usuário avisando sobre os arquivos gerados.
                end = time.process_time()
                time = end - start
                print('CPU Execution time:', time, 'seconds.')
                break
            else: #Se ele digitar qualquer outra coisa.
                print('The answer must be either Yes or No.') #Imprima uma mensagem avisando que ele deve inserir sim ou não apenas.
                user_exception_input = input('Answer with Yes or No: ').lower().capitalize() #Se o usuário escrever qualquer coisa além de sim ou não, ele tem mais chances de corrigir o erro ao invés de ter que rodar todo o programa novamente.
else: #Caso o arquivo inserido pelo usuário não seja encontrado...
    print('File not found. Enter a valid name.') #Um aviso é entregue a ele pedindo um arquivo válido.
