from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark import Transformer
from lark import Discard
from datetime import date

grammar = '''
//Regras Sintaticas
start: turma*
turma: "TURMA" LETTER alunos
alunos: (aluno PONTOVIR)* aluno PONTO
aluno: WORD PE notas PD
notas: INT (VIR INT)*
//Regras Lexicográficas
PE:"("
PD:")"
VIR:","
PONTOVIR: ";"
PONTO: "."
//Tratamento dos espaços em branco
%import common.WS
%import common.LETTER
%import common.WORD
%import common.INT
%ignore WS
'''

class AlunosTransformer(Transformer):
    turmas = {}
    studentsByGrades = {}
    meanOfStudentsGrades = {}
    maxGradesStudentsByClass = {}
    markdown = '''
# Visualizador de turmas'''
    querySQL = '''CREATE TABLE escola (
    nomeAluno VARCHAR(50) PRIMARY KEY,
    nota INT
    turma VARCHAR(1)
    dataInsercao DATETIME
);
INSERT INTO escola (nomeAluno, nota, dataInsercao, turma)
VALUES'''
    totalStudents = 0
    htmlPage = ""

    def start(self,elementos):
        return self.totalStudents, self.meanOfStudentsGrades.items(), self.studentsByGrades, self.markdown, self.querySQL, self.htmlPage

    def turma(self, turma):
        self.turmas[turma[0].value] = turma[1]

        self.maxGradesStudentsByClass[turma[0].value] = max(len(aluno["notas"]) for aluno in turma[1])

        self.createTurmaMarkdownEntry(turma[0].value, turma[1])
        self.createQuery(turma[0].value,turma[1])
        self.createTurmaHTML(turma[0].value,turma[1])
        
        return Discard
    
    def alunos(self,alunos):
        return alunos
        
    def aluno(self,aluno):

        # ex 1
        self.totalStudents = self.totalStudents + 1

        # ex 2
        # add student mean in the map that store means of students grades
        self.meanOfStudentsGrades[aluno[0].value] = sum(aluno[1])/len(aluno[1])

        # ex 3
        # for each student grade, append the student in the students list that have the grade
        for nota in aluno[1]:
            if self.studentsByGrades[nota] is None:
                self.studentsByGrades[nota] = [aluno[0].value]
            elif aluno[0].value not in self.studentsByGrades[nota]:
                self.studentsByGrades[nota].append(aluno[0].value)

        return {
            "nome":aluno[0].value,
            "notas":aluno[1]
        }

    def notas(self, notas):

        # ex 3 preparation
        # create empty entries for a given note if note does not exist in self.studentsByGrades
        for nota in notas:
            if nota not in self.studentsByGrades:
                self.studentsByGrades[nota] = []

        return notas
    
    def INT(self, number):
        return int(number)
        
    def PE(self,pe):
        return Discard

    def PD(self,pd):
        return Discard 

    def VIR(self,vir):
        return Discard
    
    def PONTOVIR(self,pontoVir):
        return Discard
    
    def PONTO(self,ponto):
        return Discard
    
    # ALTERNATIVE APPROACH EX 1
    # calculate number of students in all classes
    def getNumberOfStudents(self):
        res = 0
        for turma in self.turmas.values():
            res += len(turma)
        return res

    # ALTERNATIVE APPROACH EX 2
    # return a list with objects: {student, grades_mean}
    def getMeanOfStudentsGrades(self):
        studentsMean = []

        for turma in self.turmas.values():
            for aluno in turma:
                studentsMean.append({
                    "student": aluno["nome"],
                    "meanGrades": sum(aluno["notas"])/len(aluno["notas"])
                })

        return studentsMean

    # ALTERNATIVE APPROACH EX 3
    # return a object, where each key is a given grade
    # and each value is the students that have this grade
    def getStudentsByGrade(self):
        studentsByGrades = {}

        for turma in self.turmas.values():
            for aluno in turma:
                for nota in aluno["notas"]:
                    if nota in studentsByGrades:
                        if aluno not in studentsByGrades[nota]:
                            studentsByGrades[nota] = studentsByGrades[nota].append(aluno)
                    else:
                        studentsByGrades[nota] = [aluno]

        return studentsByGrades

    # create a class markdown string given a class
    def createTurmaMarkdownEntry(self, turmaID, alunos):
        
        self.markdown += '''
## Turma ''' + turmaID

        for aluno in alunos:
            self.markdown += '''
* ''' + aluno["nome"]

        self.markdown += '''
### Notas
| Aluno | Media |
| ----- | ----- |'''

        for aluno in alunos:
            self.markdown += '''
|''' + aluno["nome"] + '''|''' + str(self.meanOfStudentsGrades[aluno["nome"]]) + '''|'''

    # create a query SQL string to insert students of a given class
    def createQuery(self,turmaID,alunos):
        for aluno in alunos:
            for nota in aluno["notas"]:
                self.querySQL += '''
('''+ aluno["nome"] + ''', ''' + str(nota) + ''', ''' + str(date.today()) +  ''', ''' + turmaID + ''');'''

    # create a html string with a table of notes given a class
    def createTurmaHTML(self, turmaID, alunos):
        self.htmlPage += '''<h1>Turma''' + turmaID +'''</h1>
<table style="border-collapse: collapse; width: 100%; height: 81px;" border="1">
<tbody>
<tr style="height: 18px;">
<td style="width: 10%; height: 18px; text-align: center;">Nome</td>
'''     

        for i in range(0,self.maxGradesStudentsByClass[turmaID]):
            self.htmlPage += '''<td style="width: 10%; height: 18px; text-align: center;">Nota ''' + str(i) + '''</td>'''

        self.htmlPage += ''''
<td style="width: 10%; height: 18px; text-align: center;">M&eacute;dia</td>
<td style="width: 10%; height: 18px; text-align: center;">&nbsp;</td>
</tr>
<tr style="height: 21px;">        
'''
        for aluno in alunos:
            self.htmlPage += '''<td style="width: 10%; text-align: center; height: 21px;">''' + aluno["nome"] + '''</td>'''

            for i in range(0,self.maxGradesStudentsByClass[turmaID]):
                if len(aluno["notas"]) > i:
                    self.htmlPage += '''<td style="width: 10%; text-align: center; height: 21px;">''' + str(aluno["notas"][i]) + '''</td>'''
                else:
                    self.htmlPage += '''<td style="width: 10%; text-align: center; height: 21px;"> - </td>'''

            self.htmlPage += '''<td style="width: 10%; text-align: center; height: 21px;"><span id="cwos" class="qv3Wpe">''' + str(round(sum(aluno["notas"])/self.maxGradesStudentsByClass[turmaID],2)) + '''</span></td>'''

            if (self.meanOfStudentsGrades[aluno["nome"]] > 9.5):
                self.htmlPage += '''
<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-embarassed.gif" alt="embarassed" /></td>
</tr>'''
            else:
                self.htmlPage += '''
<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-cry.gif" alt="embarassed" /></td>
</tr>'''

        self.htmlPage += '''</table>'''


frase = """
TURMA A
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9);
xico (12,16).
TURMA B
henrique (12, 13, 15, 12, 13, 15, 14, 70); 
pedro (9,7,3,6,9,12);
suarez (10,16,19);
Messi(20,20,20,20).
"""

p = Lark(grammar)  
tree = p.parse(frase)
numberOfStudents, meanOfStudentsGrades, studentsByGrades, markdown, querySQL, htmlPage = AlunosTransformer().transform(tree) 

print("> Total number of students: ", numberOfStudents)
print("> Média de cada aluno: ")
for studentName, studentMean in meanOfStudentsGrades:
    print("    " +studentName + ": " + str(round(studentMean,2)))
print("> Alunos que tiraram cada nota: ")
for grade in studentsByGrades.keys():
    print("    " + str(grade) + ":")
    for student in studentsByGrades[grade]:
        print("        " + student)

f = open("markdown.md", "w")
f.write(markdown)

f = open("query.sql", "w")
f.write(querySQL)

f = open("pag.html", "w")
f.write(htmlPage)
