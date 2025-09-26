Requisitos e Dependências
O projeto foi desenvolvido com simplicidade em mente e não possui dependências externas. Tudo o que você precisa é de uma instalação padrão do Python.

Python 3.6 ou superior (Recomendado, pois o código utiliza f-strings, que foram introduzidas no Python 3.6).

Como Executar
Siga os passos abaixo para executar o analisador léxico:

1. Estrutura de Arquivos:
Certifique-se de que todos os arquivos do projeto estão na mesma pasta:

/seu_projeto
├── main.py
├── scanner.py
├── token_class.py
├── token_type.py
└── programa.mc
2. Código-Fonte de Entrada:
Crie ou edite o arquivo programa.mc. Este arquivo contém o código que você deseja que o analisador processe. Você pode usar o exemplo abaixo:

3. Execução via Terminal:
Abra um terminal ou prompt de comando, navegue até a pasta onde salvou os arquivos e execute o seguinte comando:

python main.py

4. Saída:
A saída do analisador será impressa diretamente no terminal, mostrando a sequência de tokens reconhecidos ou as mensagens de erro léxico encontradas no arquivo programa.mc.
