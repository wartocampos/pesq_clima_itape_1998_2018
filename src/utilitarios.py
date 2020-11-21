import re

INTEIRO_REGEX = re.compile("^[0-9]+$")
DECIMAL_REGEX = re.compile("^[0-9]+(.[0-9]+)?$")


def ler_numero_inteiro(titulo):
    """
    Funcao que faz a leitura da entrada esperando um numero inteiro.
    :param titulo: Mensagem a ser exibida para informar a leitura da entrada fornecida pelo usuario.
    :return: Numero inteiro digitado pelo usuario.
    """
    return int(ler_entrada_usuario(titulo, INTEIRO_REGEX, 'O texto digitado nao esta valido como numero inteiro. Favor digite novamente.'))


def ler_numero_decimal(titulo):
    """
    Funcao que faz a leitura da entrada esperando um numero decimal.
    :param titulo: Mensagem a ser exibida para informar a leitura da entrada fornecida pelo usuario.
    :return: Numero decimal digitado pelo usuario.
    """
    return float(ler_entrada_usuario(titulo, DECIMAL_REGEX, 'O texto digitado nao esta valido como numero decimal. Favor digite novamente'))


def ler_entrada_usuario(titulo, regex = None, mensagem_erro = None):
    """
    Funcao que faz a leitura da entrada do usuario.
    :param titulo: Mensagem a ser exibida para informar a leitura da entrada fornecida pelo usuario.
    :param regex: Expressao regular para validar o texto informado pelo usuario.
    :param mensagem_erro: Texto a apresentar ao usuario do erro de validacao da entrada informada.
    :return: Texto informado pelo usuario.
    """
    input_correto = False
    while not input_correto:
        print(titulo)
        entrada = str(input())
        if regex is None:
            return entrada
        input_correto = regex.match(entrada) is not None
        if input_correto:
            return str(entrada)
        else:
            print(mensagem_erro)

