# Membros:
# Rafael Lucas Carlos Gonçalves
# João Victor Queiroz
# José Vieira Stable

from scanner import Scanner

def main():
    # Crie um arquivo 'programa.mc' para testar
    sc = Scanner("programa.mc")
    
    # O loop do-while do Java é implementado assim em Python
    while True:
        tk = sc.next_token()
        if tk is None:  # Em Python, o fim é sinalizado por None (equivalente ao null do Java)
            break
        print(tk)

if __name__ == "__main__":
    main()