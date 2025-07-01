def saudacao(nome):
    mensagem = f"Olá, {nome}! Bem-vindo ao mundo do Python."
    return mensagem

def soma(a, b):
    resultado = a + b
    return resultado

# Início do programa
nome_usuario = "Francieli"
print(saudacao(nome_usuario))

valor1 = 10
valor2 = 20
total = soma(valor1, valor2)
print(f"O resultado da soma é: {total}")