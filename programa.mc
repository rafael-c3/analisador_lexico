function main() {
    let numero:number;
    let pares:number;
    let impares:number;
    let soma:number;

    pares = 0;
    impares = 0;
    soma = 0;

    // Lê números até que o usuário digite um número negativo
    read(numero);

    while (numero >= 0) {
        if ((numero % 2) == 0) {
        pares = pares + 1;
        } else {
        impares = impares + 1;
        }

        soma = soma + numero;

        // Condicional com operador lógico composto
        if ((soma > 100 && pares > 5) || impares > 10) {
            console.log("Muitos números já foram digitados!");
        }
        read(numero);
    }
    console.log("Total de números pares:");
    console.log(pares);
    console.log("Total de números ímpares:");
    console.log(impares);
    console.log("Soma total dos números:");
    console.log(soma);
}