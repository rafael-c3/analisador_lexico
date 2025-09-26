# Membros:
# Rafael Lucas Carlos Gonçalves
# João Victor Queiroz
# José Vieira Stable

from scanner import Scanner

def main():
    sc = Scanner("programa.mc")

    while True:
        tk = sc.next_token()
        if tk is None:
            break
        print(tk)

if __name__ == "__main__":
    main()