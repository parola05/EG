# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática)
#  + [-4,-2][1,2][3,5][7,10][12,14][15,19]
#  - [19,15][12,6][-1,-3]
#  - [1000,200][30,12]
# ------------------------------------------------------------
import sys
import ply.yacc as yacc
from intervalos_lex import tokens

# Retorna True se os intervalos de valores seguem o sentido proposto e se não se intercetam
def semanticaCorrecta(intervalos,sentido):
    ultimoDir = -1

    if sentido == -1:
        for intervalo in intervalos:
            if intervalo["esq"] < intervalo["dir"] or intervalo["esq"] > ultimoDir:
                return False
            ultimoDir = intervalo["dir"]
        return True
    else:
        for intervalo in intervalos:
            if intervalo["esq"] > intervalo["dir"] or intervalo["esq"] < ultimoDir:
                return False
            ultimoDir = intervalo["dir"]
        return True

# Retorna a amplitude de um intervalo
# EX:
# [1,4] -> 3
# [-2,-8] -> 5
# [7,1] -> 6
# [-5, -1] -> 4
# [-5, 2] -> 7
# [4, -5] -> 9
def amplitude(intervalo):
    if (intervalo["esq"] < 0 and intervalo["dir"] < 0):
        return abs(abs(intervalo["esq"]) - abs(intervalo["dir"]))
    else:
        return abs(intervalo["esq"] - intervalo["dir"])

# Retorna o número de intervalos
def numeroDeIntervalos(intervalos):
    return len(intervalos)

# Retorna o comprimento de cada intervalo (Lsup-Linf)
def comprimentoIntervalos(intervalos):
    comprimentos = []
    for intervalo in intervalos:
        comprimentos.append(amplitude(intervalo))
    return comprimentos

# Retorna o intervalo mais longo e o mais curto
def extremos(intervalos):
    if len(intervalos) > 0:
        compIntervalos = comprimentoIntervalos(intervalos)
        intervaloMaisLongo = (0,compIntervalos[0])
        intervaloMaisCurto = (0,compIntervalos[0])

        i = 0
        for comprimento in compIntervalos:
            if (comprimento > intervaloMaisLongo[1]):
                intervaloMaisLongo = (i,comprimento)
            if (comprimento < intervaloMaisCurto[1]):
                intervaloMaisCurto = (i,comprimento)
            i = i +1
        
        return (intervaloMaisLongo[0],intervaloMaisCurto[0]) 

# Retorna a amplitude da sequência, considerando-a como a diferença (em valor absoluto) 
# entre o limite superior do último intervalo e o limite inferior do 1º intervalo
def amplitudeTotal(intervalos):
    return amplitude({"esq":intervalos[0]["esq"], "dir" :intervalos[-1]["dir"]})

# The set of syntatic rules
def p_sequencia(p):
    "sequencia : sentido intervalos"
    if not semanticaCorrecta(parser.intervalos,parser.sentido):
        print("Frase semanticamente incorrecta")
    print("\nNúmero de intervalos:",numeroDeIntervalos(parser.intervalos))
    print("Comprimento de cada intervalo:")
    i = 0
    compIntervalos = comprimentoIntervalos(parser.intervalos)
    for comprimento in compIntervalos:
        print(i,"-) Intervalo [",parser.intervalos[i]["esq"],",",parser.intervalos[i]["dir"],"] -> ", comprimento)
        i = i + 1
        
    intervaloMaisLongo, intervaloMaisCurto = extremos(parser.intervalos)
    print("Intervalo mais longo: [",parser.intervalos[intervaloMaisLongo]["esq"],",",parser.intervalos[intervaloMaisLongo]["dir"],"]")
    print("Intervalo mais curto: [",parser.intervalos[intervaloMaisCurto]["esq"],",",parser.intervalos[intervaloMaisCurto]["dir"],"]")

    print("Amplitude total: ", amplitudeTotal(parser.intervalos),"\n")

def p_sentidoA(p):
    "sentido : '+'"
    parser.sentido = 1

def p_sentidoD(p):
    "sentido : '-'"
    parser.sentido = -1

def p_intervalos_intervalo(p):
    "intervalos : intervalo"

def p_intervalos_intervalos(p):
    "intervalos : intervalos intervalo"

def p_intervalo(p):
    "intervalo : '[' NUM ',' NUM ']'"
    parser.intervalos.append({"esq":int(p[2]),"dir":int(p[4])})

# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()
parser.intervalos = [] # exemplo: [{1,2},{3,5}]
parser.sentido = -1 # -1 se negativo, 1 caso contrário

# Start parsing the input text
for line in sys.stdin:
    parser.success = True
    parser.flag = True
    parser.last = 0
    parser.intervalos = []
    parser.parse(line)