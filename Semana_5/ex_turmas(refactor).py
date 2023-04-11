from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from datetime import date

class MyInterpreter(Interpreter):
    def __init__(self) -> None:
        super().__init__()
        self.num_alunos = 0
        self.turma_atual = ''
        self.aluno_atual = ''
        self.media_alunos_por_turma = {} # turma -> [aluno] -> media
        self.alunos_por_notas = {} # nota -> [aluno]
        self.markdown = '''
# Visualizador de turmas
'''
        self.querySQL = '''
CREATE TABLE escola (
    nomeAluno VARCHAR(50) PRIMARY KEY,
    nota INT
    turma VARCHAR(1)
    dataInsercao DATETIME
);
INSERT INTO escola (nomeAluno, nota, dataInsercao, turma)
VALUES
'''

    def start(self,listaTurmas):
        #start: turma+
        self.turmasDic = {}
        for turma in listaTurmas.children:
            self.visit(turma)
        return {
            "num_alunos": self.num_alunos,
            "media_alunos_por_turma": self.media_alunos_por_turma,
            "alunos_por_notas": self.alunos_por_notas,
            "markdown": self.markdown,
            "querySQL": self.querySQL,
        }

    def turma(self,turma): 
        #turma : ("TURMA" MAIUSCULA+ alunos PONTO)
        #print("TURMA",turma.children[0])
        self.markdown += '''## Turma ''' + turma.children[0] + '''
''' 
        self.media_alunos_por_turma[turma.children[0]] = {}
        self.turma_atual = turma.children[0]
        tree_alunos = turma.children[1]
        alunos = self.visit(tree_alunos)
        self.turmasDic[turma.children[0].value]=alunos
        self.markdown += '''### Notas
| Aluno | Média |
| ----- | ----- |
'''
        for aluno, mediaAluno in self.media_alunos_por_turma[self.turma_atual].items():
            self.markdown += '''|''' + aluno + '''|''' + str(mediaAluno) + '''|
'''
    
    def alunos(self,alunos):
        #alunos: aluno (PONTOVIRGULA aluno)*
        #print("Visitar os alunos")
        alunosList = []
        # Visitar todos os alunos
        for element in alunos.children:
        # So visitamos os tipo tree que sao os alunos
            if (type(element) == Tree and element.data == "aluno"):
                aluno = self.visit(element)
                alunosList.append(aluno)
        return alunosList

    def aluno(self,aluno):
        #aluno: NOME "(" notas ")"
        nome = aluno.children[0].value
        self.aluno_atual = nome
        self.markdown += '''* ''' + nome + '''
'''
        notas = self.visit(aluno.children[1])
        self.media_alunos_por_turma[self.turma_atual][nome] = sum(notas)/len(notas)
        return {
            "nome": nome,
            "notas": notas
        }
    
    def notas(self,notas):
        #notas: NUMERO ("," NUMERO*
        notas_list = []
        for element in notas.children:
            self.querySQL += '''('''+ self.aluno_atual + ''', ''' + element.value + ''', ''' + str(date.today()) +  ''', ''' + self.turma_atual + ''');
'''
            if (type(element) == Token):
                notas_list.append(int(element.value))

            if element.value not in self.alunos_por_notas:
                self.alunos_por_notas[element.value] = [self.aluno_atual]
            elif (self.aluno_atual not in self.alunos_por_notas[element.value]):
                self.alunos_por_notas[element.value].append(self.aluno_atual)

        return notas_list


grammar = '''
start: turma+
turma : ("TURMA" MAIUSCULA alunos PONTO)
alunos: aluno (PONTOVIRGULA aluno)*
aluno: NOME "(" notas ")"
notas: NUMERO ( "," NUMERO)*
MAIUSCULA:("A".."Z")+
NOME: ("A".."Z"|"a".."z")+
NUMERO:"0".."9"+
PONTO:"."
PONTOVIRGULA:";"
%import common.WS
%ignore WS
'''

frase = "TURMA A ana (1,2,3); ze (2,4);rui(12). TURMA PL zeca(2); rita(2,4,6). TURMA EG rosa (10,11,12,13)."

p = Lark(grammar,start="start")
parse_tree = p.parse(frase)
data = MyInterpreter().visit(parse_tree)

print("> Total number of students: ", data["num_alunos"])
print("> Média de cada aluno: ")

for turmaID, mediaAlunos in data["media_alunos_por_turma"].items():
    print("   Turma ", str(turmaID))
    for aluno, mediaAluno in mediaAlunos.items():
        print("        ", aluno, ": ", str(mediaAluno))

print("> Alunos por notas: ")

for nota, alunos in data["alunos_por_notas"].items():
    print("    ", nota, ":")
    for aluno in alunos:
        print("        ",aluno)

f = open("pag.md", "w")
f.write(data["markdown"])

f = open("query.sql", "w")
f.write(data["querySQL"])
