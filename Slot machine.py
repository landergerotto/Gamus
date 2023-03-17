import random
from time import sleep

#ERROS para validações
class Erro_Negacao_Usuario(Exception):
    pass

class Saque_Imediato(Exception):
    pass

#função que pega o depósito para o jogo
def depositar():
    while True:
        try:
            quantidade = int(input(RESET+"\n\nQuanto você gostaria de depositar?\n> "))
            if quantidade > 0:
                break
            else:
                print("\n\nA quantidade depositada deve ser maior que 0 R$")
        except ValueError:
            print(YELLOW + "\n\nInsira um número, por favor")
    return quantidade

#função que pega em qnts linhas o usuário quer apostar
def aposta_numero_de_linhas ():
    while True:
        try:
            linhas = int(input(RESET+"\n\nEm quais linhas voce gostaria de apostar? (1 - " + str(Max_Linha) + ")\n(Por exemplo, ao digitar 2, você apostará nas 2 primeiras linhas) \n> "))
            if 1 <= linhas <= Max_Linha:
                break
            else:
                print("\n\nDigite um valor válido de linhas, por favor")
        except ValueError:
            print(YELLOW + "\n\nInsira um número, por favor")
    return linhas

#função que pega o valor da aposta    
def valor_aposta ():
    while True:
        try:
            aposta = int(input(RESET+"\n\nQuanto voce gostaria de APOSTAR em CADA LINHA?\n> "))
            if Aposta_Min <= aposta <= Aposta_Max:
                break
            else:
                print(f"\n\nA quantidade depositada deve ser entre {Aposta_Min}R$ e {Aposta_Max}R$!")
        except ValueError:
            print(YELLOW + "\n\nInsira um número, por favor")
    return aposta

#printa a roleta
def print_Roleta (roleta):
    print('\n'*2)
    for i in range(len(roleta)):
        print (RESET + '                                  |', end='')
        for j in range (len(roleta[i])):
            if roleta[i][j] == '7':
                sleep(0.5)
                print(GREEN + '  7', end= '')
            elif roleta[i][j] == '1':
                sleep(0.5)
                print(WHITE + '  1', end= '')
            elif roleta[i][j] == '4':
                sleep(0.5)
                print(CYAN + '  4', end= '')
            elif roleta[i][j] == '6':
                sleep(0.5)
                print(YELLOW + '  6', end= '')
            else:
                print(RESET + '   ', end= '')
            print (RESET + '  |',  end='')
        print('')
        
#coloca numeros aleatorios dentro da roleta
def gira_Roleta(roleta):
    for i in range (len(roleta)):
        for j in range (len(roleta[i])):
            roleta[i][j] = random.choice(simbolos_roleta)
    return roleta

#verifica a pontuação
def verifica_ganhos(roleta, linhas, valor_apostado, valor_numero):
    ganho = 0
    for i in range (linhas):
        numero = roleta[i][0]
        for j in range(len(roleta[i])):
            verifica_numero = roleta[i][j]
            if numero != verifica_numero:
                break
        else:
            print(GREEN +'\n\n                                        JACKPOT!!\n')
            ganho += valor_numero[numero] * valor_apostado
    return ganho

#Valor de cada numero
valor_numero = {'7' : 5,
                '6' : 2.5,
                '4' : 1.5,
                '1' : 1}

#ROLETA
roleta = [['6', '6', '1'],
          ['1', '4', '6'],
          ['1', '1', '1']]

#cores
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

#variáveis fixas
Max_Linha = 3
Aposta_Max = 1000
Aposta_Min = 1
simbolos_roleta = ['1', '4', '6', '7']

######### CODIGO PRICIPAL #########
####### APOSTA PROFISSIONAL #######
cache = depositar()
while True:
    try:
        #verifica se o usuario nao zerou, se zerou, ele perde instantaneamente
        if cache <= 0:
            raise KeyboardInterrupt
        linhas = aposta_numero_de_linhas ()
        #verificacao se o total da aposta nao eh superior ao cache(valor depositado)
        while True:
            aposta = valor_aposta()
            total_aposta = aposta * linhas
            if total_aposta > cache:
                print(RED + f'\n\nVoce nao possui fundos o suficiente para realizar essa aposta\natualmente você está apostando em {linhas} linhas\nO valor do seu saldo é de: {cache}R$')
                print(RESET + '(\nVocê poderá cancelar a operação depois)')
            else:
                break
        #Confirmacao do usuario em relacao a aposta
        while True:
            confirma = input(GREEN + f'\n\nSaldo = {cache}R$\nTotal da aposta = {total_aposta}R$\nSaldo mínimo após a aposta = {cache - total_aposta}R$\nVoce confirma a aposta de {aposta}R$ em {linhas} linhas?\n\n(Digite sim ou não)\n> ').upper()
            if confirma == 'SIM' or confirma == 'S' or confirma == 'SI':
                break
            elif confirma == 'NÃO' or confirma == 'NAO' or confirma == 'NA' or confirma == 'NÃ' or confirma == 'N':
                raise Erro_Negacao_Usuario
        #subtracao de cache, girada da roleta, se ganhar soma o cache
        cache = cache - total_aposta
        roleta = gira_Roleta(roleta)
        print_Roleta(roleta)
        ganhos = verifica_ganhos(roleta, linhas, total_aposta, valor_numero)
        cache += ganhos
        print(GREEN + f'Você ganhou {ganhos}R$')
        print(f'\n\nSeu saldo é de: {cache}R$')
        while True:
            continuar = input(RESET + '\n\nVocê deseja continuar jogando? (Digite sim ou não)\n> ').upper()
            if continuar == 'SIM' or continuar == 'S':
                print('\n'*30)
                print(GREEN + f'\n\nSeu saldo é de: {cache}R$')
                break
            elif continuar == 'NÃO' or continuar == 'NAO' or continuar =='NÃ' or continuar == 'NA' or continuar == 'N':
                print('\n'*30)
                raise KeyboardInterrupt
            else:
                print('\n\nDigite uma resposta válida, por favor')
    
    ### Possiveis Erros ### 

    #aq pode acontecer mt coisa pro usuario querer cancelar, normalmente sera problema na aposta, ou no cache, ou querer sacar, ou aumentar o saldo       
    except Erro_Negacao_Usuario:
        print('\n'*30)
        print(YELLOW +'\n\nConfirmacao negada')
        while True:
            resposta = input(RESET + f'\n\nDeseja alterar o valor depositado? (Você terá a opção de sacar)\nSeu saldo é de: {cache}R$\n\n(Digite sim ou não)\n> ').upper()
            if resposta == 'SIM' or resposta == 'S' or resposta == 'SI':
                resposta2 = int(input(RESET + '\n\nDigite 1 -> Sacar o seu saldo\nDigite 2 -> Depositar em cima do seu saldo\n> '))
                while resposta2 < 1 or resposta2 > 2:
                    print(YELLOW + '\n\nDigite 1 ou 2 por favor!')
                    resposta2 = int(input(RESET + '\n\nDigite 1 -> Sacar o seu saldo\nDigite 2 -> Depositar em cima do seu saldo\n> '))
                #faz um loop para depositar mais grana
                if resposta2 == 2:
                    while True:
                        try:
                            valor = int(input(RESET+"\n\nQuanto voce gostaria de depositar a mais?\n> "))
                            if valor > 0:
                                break
                            else:
                                print("\n\nA quantidade depositada deve ser maior que 0 R$")
                        except ValueError:
                            print(YELLOW + "\n\nInsira um numero, por favor")
                    cache += valor
                #saca o valor dentro da maquina e acaba o jogo qnd voltar pra funcao principal
                elif resposta2 == 1:
                    sleep(1)
                    print(GREEN + f'\n\nSacando {cache}R$')
                    for i in range (3):
                        print(RESET + '. ', end='')
                        sleep(0.75)
                    cache = 0
                    break
            elif resposta == 'NÃO' or resposta == 'NAO' or resposta == 'NÃ' or resposta == 'NA' or resposta == 'N':
                break
            
    #caso o cassino seja interrompido, ele vai parar aq, se o saldo for 0 ele acaba o jogo, se ele for maior 1 0 ele saca o que estava na maquina           
    except KeyboardInterrupt:
        if cache <= 0:
            print(WHITE +'\n\nFinalizando o jogo')
            for i in range (3):
                print('. ', end='')
                sleep(1)
            print(MAGENTA + '\n\n\nOBRIGADO POR JOGAR!!')
            break
        else:
            sleep(1)
            print(GREEN + f'\n\nSacando {cache}R$')
            for i in range (3):
                print(RESET + '. ', end='')
                sleep(0.75)
            print(RESET + f'\n\n{cache}R$ sacado com sucesso')
            print(WHITE +'\n\nFinalizando o jogo')
            for i in range (3):
                print('. ', end='')
                sleep(0.75)
            print(MAGENTA + '\n\n\nOBRIGADO POR JOGAR!!')
            break
