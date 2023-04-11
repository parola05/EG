from lark import Discard
from lark import Lark,Token,Tree
from datetime import date
from lark.visitors import Interpreter
from lark import Transformer

"""
1-) Transforme a seguinte GIC em notação lark :

T  = { '[', ']', STRING, DATA, FICH }
         P = {
         p1: album  : capa "[" pags "]" ccapa
         p2: capa   : titulo autor DATA
         p3: titulo : STRING
         p4: autor  : STRING
         p5: ccapa  : fecho DATA
         p6: fecho  : STRING
         p7: pags   : pag+
         p8: pag    : sep | folha
         p9: sep    : titulos
         p10: folha : foto+
         p11: foto  : FICH legenda
         p12: legenda : STRING

Considere a seguinte frase exemplo válida         

           "Um passeio pelo Geres" 
        Joaozinho 
        03-04-2000 
        [ 
          "Cascata do tahiti"
          img1
          "Vista da cascata."

          "A aldeia de Soajo"
          img2 
          "casa da aldeia."
        ] 
        "Dedicado à família" 
        03-05-2000
"""

grammar = '''
start: capa "[" pags "]" ccapa
capa: titulo autor data
pags:pag+
pag:sep | folha
sep:titulo
folha:foto+
foto:ficheiro legenda
ficheiro:WORDWNUMBER
legenda:QUOTEDWORD
ccapa:fecho data
fecho:QUOTEDWORD
titulo:QUOTEDWORD
autor:WORD
data:DATA
DATA:DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT DIGIT DIGIT
QUOTEDWORD: /"[a-zA-Z][a-zA-Z. ]+"/
WORDWNUMBER: /[a-zA-Z0-9][a-zA-Z0-9 ]+/
%import common.WS
%import common.WORD
%import common.DIGIT
%ignore WS
'''

frase = """
        "Um passeio pelo Geres" 
        Joaozinho 
        03-04-2000 
        [ 
          "Cascata do tahiti"
          img1
          "Vista da cascata."
          "A aldeia de Soajo"
          img2 
          "casa da aldeia."
        ] 
        "Dedicado a familia" 
        03-05-2000
"""
p = Lark(grammar,start="start")
parse_tree = p.parse(frase)
#print(parse_tree.pretty())

"""
2-) Imprimir o album para latex, considerando :

    a-) que o titulo deverá ser um \title ;
    b-) que o autor deverá ser um \author ;
    c-) cada página deverá ser um \title e terminar com o \newpage ;
    d-) uma foto devera usar o nome do ficheiro para renderizar e a legenda como \caption.Exemplo :
        \begin{figure}[h!]
        \centering
        \includegraphics[width=0.3\textwidth]{frog.jpg}
        \caption{\label{fig:frog}Vista da cascata.}
        \end{figure}
"""

class MyInterpreter(Interpreter):
    def __init__(self) -> None:
        super().__init__()
        self.latex = ""

    def start(self,production):
        #start: capa "[" pags "]" ccapa
        self.visit(production.children[0]) # visit capa
        self.visit(production.children[1]) # visit pags
        return self.latex

    def capa(self,production): 
        #capa: titulo autor data
        titulo = self.visit(production.children[0]) # get title
        autor = self.visit(production.children[1]) # get author
        self.latex += f"""\\title{{{titulo}}}
\\author{{{autor}}}"""

    def pags(self,production):
        #pags: pag+
        for pag in production.children:
            self.visit(pag)

    def pag(self,production):
        #pag:sep | folha
        self.visit(production.children[0]) # visit sep or folha
        self.latex += f"""
\\newpage"""

    def sep(self,production):
        #sep:titulo
        titulo = self.visit(production.children[0]) # get title
        self.latex += f"""
\\section{{{titulo}}}"""

    def folha(self,production):
        #folha:foto+
        for foto in production.children:
            self.visit(foto)

    def foto(self,production):
        #foto:ficheiro legenda
        ficheiro = self.visit(production.children[0])
        legenda = self.visit(production.children[1])
        self.latex += f"""
\\begin{{figure}}[h!]
\\centering
\\includegraphics[width=0.3\\textwidth]{{{ficheiro}}}
\\caption{{\\label{{fig:{ficheiro}}}{legenda}}}
\\end{{figure}}"""

    def ficheiro(self,production):
        #ficheiro:WORDWNUMBER
        return production.children[0].value

    def legenda(self,production):
        #legenda:QUOTEDWORD
        return production.children[0].value
    
    def ccapa(self,production):
        #ccapa:fecho data
        pass 

    def fecho(self,production):
        #fecho:QUOTEDWORD
        pass 

    def titulo(self,production):
        #titulo:QUOTEDWORD
        return production.children[0].value

    def autor(self,production):
        #autor:WORD
        return production.children[0].value

    def data(self,production):
        #data:DATA
        pass 

    def DATA(self,production):
        #DATA:DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT DIGIT DIGIT
        pass 

#latex = MyInterpreter().visit(parse_tree)
#print(latex)

class MyTransformer(Transformer):
    def __init__(self) -> None:
        super().__init__()
        self.latex = ""

    def start(self,production):
        #start: capa "[" pags "]" ccapa
        return self.latex

    def capa(self,production): 
        #capa: titulo autor data
        self.latex += f"""\\title{{{production[0]}}}
\\author{{{production[1]}}}"""

    def pags(self,production):
        #pags: pag+
        pass

    def pag(self,production):
        #pag:sep | folha
        self.latex += f"""
\\newpage"""

    def sep(self,production):
        #sep:titulo
        titulo = production[0]
        self.latex += f"""
\\section{{{titulo}}}"""

    def folha(self,production):
        #folha:foto+
        pass

    def foto(self,production):
        #foto:ficheiro legenda

        ficheiro = production[0]
        legenda = production[1]
        
        self.latex += f"""
\\begin{{figure}}[h!]
\\centering
\\includegraphics[width=0.3\\textwidth]{{{ficheiro}}}
\\caption{{\\label{{fig:{ficheiro}}}{legenda}}}
\\end{{figure}}"""

    def ficheiro(self,production):
        #ficheiro:WORDWNUMBER
        return production[0].value

    def legenda(self,production):
        #legenda:QUOTEDWORD
        return production[0].value
    
    def ccapa(self,production):
        #ccapa:fecho data
        pass 

    def fecho(self,production):
        #fecho:QUOTEDWORD
        pass 

    def titulo(self,production):
        #titulo:QUOTEDWORD
        return production[0].value

    def autor(self,production):
        #autor:WORD
        return production[0].value

    def data(self,production):
        #data:DATA
        pass 

    def DATA(self,production):
        #DATA:DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT DIGIT DIGIT
        pass 

latex = MyTransformer().transform(parse_tree)
print(latex)