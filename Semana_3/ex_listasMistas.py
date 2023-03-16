from lark import Lark
from lark.tree import pydot__tree_to_png
from lark import Transformer
from lark import Discard

class MyTransformer(Transformer):
    # variáveis de controlo do "agora" e "fim"
    fim_antes_de_agora = False
    cont_agora = 0
    pelo_menos_um_numero = True
    # variáveis resultados das operações
    numero_de_elemento = 0
    quantidade_de_cada_elemento = {}
    soma_entre_agora_e_fim = 0

    def start(self, items):
        if self.fim_antes_de_agora == True or self.cont_agora > 0:
            print("Lista inválida")
        else:
            print("Lista válida")
            print("Número de elementos: ", self.numero_de_elemento)
            elemento, quantidade =  self.get_elemento_que_mais_se_repete()
            print("Elemento '", elemento, "' é o que mais se repete: ", quantidade, " vezes") 
            print("Soma dos números entre 'agora' e 'fim': ", self.soma_entre_agora_e_fim)
        return Discard

    def elementos(self, elementos):
        return Discard
    
    def elemento(self, elemento):
        # Incrementar número total de elementos da lista
        self.numero_de_elemento = self.numero_de_elemento + 1

        # Incrementar contador de quantas vezes o elemento se repete na lista
        if elemento[0] not in self.quantidade_de_cada_elemento:
            self.quantidade_de_cada_elemento[elemento[0]] = 1
        else:
            self.quantidade_de_cada_elemento[elemento[0]] = self.quantidade_de_cada_elemento[elemento[0]] + 1
        return Discard
    
    def NUMERO(self, numero):
        # Caso estiver entre um "agora" e "fim" devo somar o valor a variável
        # que armazena a soma de elementos entre "agora" e "fim" 
        if self.cont_agora > 0:
            self.soma_entre_agora_e_fim = self.soma_entre_agora_e_fim + int(numero)
            self.pelo_menos_um_numero = True
        return int(numero)
    
    def PALAVRA(self, palavra):
        if palavra == "fim":
            # Caso detectar "fim" antes de um "agora" ou não houver pelo
            # menos um número entre o "agora" e "fim"
            if self.cont_agora == 0 or self.pelo_menos_um_numero == False:
                self.fim_antes_de_agora = True 
            else:
                self.cont_agora = self.cont_agora - 1 
        elif palavra == "agora":
            self.cont_agora = self.cont_agora + 1
            self.pelo_menos_um_numero = False
        
        return palavra
    
    def VIR(self, vir):
        return Discard
    
    def get_elemento_que_mais_se_repete(self):
        max = (0, 0) 
        for elemento, quantidade in self.quantidade_de_cada_elemento.items():
            if quantidade > max[1]:
                max = (elemento,quantidade) 
        return max

## GIC
grammar = '''
//Regras Sintaticas
start: PE elementos PD
elementos : elemento (VIR elemento)*
elemento: NUMERO | PALAVRA
//Regras Lexicográficas
NUMERO:"0".."9"+
PALAVRA: WORD
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%import common.WORD
%ignore WS
'''

frase = "[aa,agora,17,fim,agora,1,5,b,5,fim,1,5,ola,1,agora,15,aa,aa,aa,fim,4,aaaaaa]"
p = Lark(grammar)

parse_tree = p.parse(frase)
#print(parse_tree.pretty())

MyTransformer().transform(parse_tree)