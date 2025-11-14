🚀 Mini-Compilador (Analisador Léxico e Sintático)
Este projeto é um mini-compilador desenvolvido em Python para a disciplina de Compiladores, compreendendo os Checkpoints 01 (Analisador Léxico) e 02 (Analisador Sintático).

O programa é capaz de processar um arquivo de código-fonte (.mc), convertê-lo em uma sequência de Tokens (Análise Léxica) e, em seguida, validar se essa sequência obedece à gramática da linguagem (Análise Sintática).

🎯 Funcionalidades Principais
1. Analisador Léxico (scanner.py)
O scanner é robusto e capaz de lidar com uma gramática complexa e entradas malformadas.

Palavras-Chave: Reconhece todas as palavras reservadas da gramática (ex: function, main, let, if, while, read, console.log, etc.).

Operadores: Identifica corretamente todos os operadores:

Aritméticos: +, -, *, /, %

Relacionais (OP_REL): ==, !=, >, <, >=, <=

Lógicos (OP_LOGICO): &&, ||

Atribuição: =

Literais: Diferencia e captura corretamente NUMINT (inteiros), NUMREAL (reais, ex: 1.23 ou .45) e CADEIA (strings).

Validação de Números: Implementa um validador "ganancioso" com Expressão Regular (RegEx) para tratar corretamente números malformados (ex: 1.1.1 ou 12.) como um único token ILLEGAL, conforme solicitado.

Tratamento de Comentários: Ignora com sucesso três tipos de comentários: #, // e /* ... */.

Relatório de Erros Léxicos: Reporta com precisão a linha e a coluna de caracteres inesperados (ex: @, ç).

2. Analisador Sintático (parser.py)
O parser implementa um Analisador Descendente Preditivo Recursivo para validar a estrutura do código.

Implementação da Gramática: Cada regra da gramática (ex: <comando>, <expressaoAritmetica>) foi convertida em uma função Python (parse_comando, parse_expressaoAritmetica).

Correção de Recursão à Esquerda: A gramática original (ex: A : A alpha | beta) foi fatorada e corrigida (para A : beta A', A' : alpha A' | ε) para permitir a implementação descendente recursiva sem loops infinitos.

Validação Estrutural: Verifica a estrutura completa do programa, desde function main... até o } final, incluindo o aninhamento de blocos.

Análise de Expressões: Analisa e valida corretamente expressões aritméticas, lógicas e relacionais complexas, incluindo o tratamento de precedência de operadores e o uso de parênteses.

Relatório de Erros Sintáticos: Em caso de violação da gramática (ex: falta de um ;), o parser para e reporta o token que era esperado versus o que foi encontrado, incluindo a linha do erro.

🛠️ Tecnologias e Requisitos
Python 3.6+

O projeto não requer nenhuma biblioteca externa, pois utiliza apenas módulos padrão do Python (re, enum).

▶️ Como Executar
O main.py é o ponto de entrada que inicializa o Scanner e o Parser. O Parser então "puxa" os tokens do Scanner sob demanda.

Garanta a Estrutura: Coloque todos os arquivos na mesma pasta:

/projeto_compilador
├── main.py
├── scanner.py
├── parser.py
├── token_type.py
├── token_class.py
└── programa_ckp2_sexta.mc
Defina o Alvo: Abra o main.py e garanta que a variável arquivo_teste aponta para o arquivo .mc que você quer analisar.

Python

# main.py
arquivo_teste = "programa_ckp2_sexta.mc"
Execute o Programa: Abra seu terminal, navegue até a pasta do projeto e rode o seguinte comando:

Bash

python main.py
Observe a Saída:

Se o programa.mc estiver sintaticamente correto, você verá a mensagem:

Parse concluído com sucesso!
Se o programa.mc tiver um erro sintático, você verá:

Erro de Compilação: Erro Sintático na linha 15: Esperado TokenType.SEMICOLON, mas encontrou TokenType.IF
Se o programa.mc tiver um erro léxico, você verá:

Erro Léxico: Caractere inesperado '@' na linha 10, coluna 5.
AVISO LÉXICO (ignorado): Token ilegal '@'
... (e o erro sintático que isso provavelmente causará) ...