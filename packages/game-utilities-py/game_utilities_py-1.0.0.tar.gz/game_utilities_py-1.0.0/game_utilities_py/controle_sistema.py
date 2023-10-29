import json
from os import path
from time import sleep
from colorama import Fore, Back, init

init()

global escolhas
escolhas = 0
global inventario
inventario = []


default_lista = []

def verificarSistemaContas():
    if path.exists('reg.json') == False:
        with open('reg.json','w') as arquivo:
            json.dump(default_lista, arquivo)
    try:
        with open('reg.json','r') as a:
            b = json.load(a)
    except json.JSONDecodeError:
        with open('reg.json','w') as arquivo:
            json.dump(default_lista, arquivo)


def controle_registrar(usuario:str, senha:str):
    verificarSistemaContas()
    try:
        cadastro = {'usuario':usuario,'senha':senha, 'save':escolhas, 'inventario':inventario}

        with open('reg.json','r') as arquivo:
            registros = json.load(arquivo)

        registros.append(cadastro)   

        with open('reg.json','w') as arquivo:
            json.dump(registros, arquivo)                
    except:
        return False, "Algo Deu Errado Em 'controle_registrar()'"

def controle_logar(usuario:str,senha:str):
    verificarSistemaContas()
    try:
        with open('reg.json','r') as arquivo:
            registros = json.load(arquivo)
        
        for i in range(len(registros)):
            users = registros[i]['usuario']
            senhas = registros[i]['senha']

            if (usuario == users) and (senha == senhas):
                print(f"Bem Vindo De Volta {usuario}")
                global id_certo
                id_certo = i
                break
        else:
            print("Usuário Não Encontrado")
    except:
        return False, "Algo Deu Errado Em 'controle_logar()'"

def controle_salvarMomento():
    verificarSistemaContas()
    global id_certo
    try:
        with open('reg.json','r') as arquivo:
            registros = json.load(arquivo)
        escolhas = registros[id_certo]['save']
        escolhas +=1
        registros[id_certo]['save'] = escolhas

        with open('reg.json','w') as arquivo:
            json.dump(registros, arquivo)
    except:
        return False, "Algo Deu Errado Em 'controle_salvarMomento()'"

def controle_carregarMomento():
    verificarSistemaContas()
    try:
        global id_certo

        with open('reg.json','r') as arquivo:
            registros = json.load(arquivo)
        escolhas = registros[id_certo]['save']

        return escolhas
    except:
        return False, "Algo Deu Errado Em 'controle_carregarMomento()'"

def controle_salvarInventario(item:str):
    verificarSistemaContas()
    global id_certo

    try:
        with open('reg.json','r') as arquivo:
            registros = json.load(arquivo)
        inventario = registros[id_certo]['inventario']
        inventario.append(item)
        registros[id_certo]['inventario'] = inventario

        with open('reg.json','w') as arquivo:
            json.dump(registros, arquivo)
    except:
        return False, "Algo Deu Errado Em 'controle_salvarInventario()'"

def controle_carregarInventario():
    verificarSistemaContas()
    global id_certo
    try:
        with open('reg.json','r') as arquivo:
            registro = json.load(arquivo)
            inventario = registro[id_certo]['inventario']
            return inventario
    except:
        return False, "Algo Deu Errado Em 'controle_carregarInventario()'"
def controle_verificarCores(cor_texto:str='branco',cor_background:str='preto'):
    cor_texto = cor_texto.lower()
    cor_background = cor_background.lower()

    if cor_texto == 'vermelho':
        cor_txt = Fore.RED
    elif cor_texto == 'amarelo':
        cor_txt = Fore.YELLOW
    elif cor_texto == 'verde':
        cor_txt = Fore.GREEN
    elif cor_texto == 'preto':
        cor_txt = Fore.BLACK
    elif cor_texto == 'branco':
        cor_txt = Fore.WHITE
    elif cor_texto == 'azul':
        cor_txt = Fore.BLUE
    elif cor_texto == 'azul claro':
        cor_txt = Fore.LIGHTBLUE_EX
    elif cor_texto == 'roxo':
        cor_txt = Fore.MAGENTA
    elif cor_texto == 'cinza':
        cor_txt = Fore.LIGHTBLACK_EX
    else:
        cor_txt = Fore.WHITE
    
    if cor_background == 'vermelho':
        cor_bg = Back.RED
    elif cor_background == 'amarelo':
        cor_bg = Back.YELLOW
    elif cor_background == 'verde':
        cor_bg = Back.GREEN
    elif cor_background == 'preto':
        cor_bg = Back.BLACK
    elif cor_background == 'branco':
        cor_bg = Back.WHITE
    elif cor_background == 'azul':
        cor_bg = Back.BLUE
    elif cor_background == 'azul claro':
        cor_bg = Back.LIGHTBLUE_EX
    elif cor_background == 'roxo':
        cor_bg = Back.MAGENTA
    elif cor_background == 'cinza':
        cor_bg = Back.LIGHTBLACK_EX
    else:
        cor_bg = Back.BLACK

    return cor_txt, cor_bg

print(controle_logar('abc',2))