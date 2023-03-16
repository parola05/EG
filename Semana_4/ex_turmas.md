Exercício 1

Desenvolva uma GIC para definir uma linguagem que permita descrever os
alunos (identificados pelo seu nome) de uma turma específica, de tal forma
que a frase abaixo seja uma frase válida dessa linguagem (ignore os \n):
```
TURMA A
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9);
xico (12,16).
TURMA B
ana (12, 13, 15, 12, 13, 15, 14); 
joao (9,7,3,6,9,12);
xico (12,16).
```
Recorrendo ao uso de lark Transformer :

1.1 Conte e imprima o número de alunos presentes, retornando o valor regra de start.

1.2 Calcule e imprima a média de cada aluno,  retornando o valor regra de start.

1.3 Organize os dados de maneira a que a cada nota corresponda os alunos que
tiraram essa nota, retornando o valor regra de start. Exemplo : ```{'12': {'joao', 'xico', 'ana'}, '13': {'ana'}, '15': {'ana'}, '14': {'ana'}, '9': {'joao'}, '7': {'joao'}, '3': {'joao'}, '6': {'joao'}, '16': {'xico'}}```

1.4 Crie uma query INSERT em SQL que insira as notas de cada alunos numa
tabela Resultado, com as seguintes colunas : nomeAluno, nota,
dataInsercao, turma. (Nota: Garanta que não existem nomes repetidos)

1.5 Crie um ficheiro markdown para visualizacao das alineas acima.
Exemplo para a turma A:

~~~
# Visualizador de turmas
## Turma A
### Lista de alunos 
- Ana
- Joao
- Xico
### Notas

| Aluno | Media |
|  --------  |  -------  |
| Ana | 13 
| Joao | 6 |
| Xico | 4 |

~~~

1.6 Crie um ficheiro html para visualizacao das alineas acima. Exemplo :
http://tpcg.io/_7FLIBV 


<h1>Turma A<code><br /></code></h1>
<table style="border-collapse: collapse; width: 100%; height: 81px;" border="1">
<tbody>
<tr style="height: 18px;">
<td style="width: 10%; height: 18px; text-align: center;">Nome</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota1</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota2</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota3</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota4</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota5</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota6</td>
<td style="width: 10%; height: 18px; text-align: center;">Nota7</td>
<td style="width: 10%; height: 18px; text-align: center;">M&eacute;dia</td>
<td style="width: 10%; height: 18px; text-align: center;">&nbsp;</td>
</tr>
<tr style="height: 21px;">
<td style="width: 10%; text-align: center; height: 21px;">ana</td>
<td style="width: 10%; text-align: center; height: 21px;">12</td>
<td style="width: 10%; text-align: center; height: 21px;">13</td>
<td style="width: 10%; text-align: center; height: 21px;">15</td>
<td style="width: 10%; text-align: center; height: 21px;">12</td>
<td style="width: 10%; text-align: center; height: 21px;">13</td>
<td style="width: 10%; text-align: center; height: 21px;">15</td>
<td style="width: 10%; text-align: center; height: 21px;">14</td>
<td style="width: 10%; text-align: center; height: 21px;"><span id="cwos" class="qv3Wpe">13</span></td>
<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-embarassed.gif" alt="embarassed" /></td>
</tr>
<tr style="height: 21px;">
<td style="width: 10%; text-align: center; height: 21px;">joao</td>
<td style="width: 10%; text-align: center; height: 21px;">9</td>
<td style="width: 10%; text-align: center; height: 21px;">7</td>
<td style="width: 10%; text-align: center; height: 21px;">3</td>
<td style="width: 10%; text-align: center; height: 21px;">6</td>
<td style="width: 10%; text-align: center; height: 21px;">9</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">6</td>
<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-cry.gif" alt="cry" /></td>
</tr>
<tr style="height: 21px;">
<td style="width: 10%; text-align: center; height: 21px;">xico</td>
<td style="width: 10%; text-align: center; height: 21px;">12</td>
<td style="width: 10%; text-align: center; height: 21px;">16</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">-</td>
<td style="width: 10%; text-align: center; height: 21px;">4</td>
<td style="width: 10%; text-align: center; height: 21px;"><img src="https://html-online.com/editor/tiny4_9_11/plugins/emoticons/img/smiley-cry.gif" alt="cry" /></td>
</tr>
</tbody>
</table>