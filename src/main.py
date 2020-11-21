import pandas as pd
import matplotlib.pyplot as plt
from utilitarios import ler_entrada_usuario, ler_numero_decimal, DECIMAL_REGEX

ASC = 'ascendente'
DESC = 'descendente'
STRING = 'string'
NUMERICO = 'numerico'
NOMES_COLUNAS = ['mes', 'dia', 'temperatura_media', 'temperatura_maxima', 'temperatura_minima', 'precipitacao_media']
TIPOS_FILTROS = dict([
    (NUMERICO, ['maior', 'menor', 'igual', 'diferente']),
    (STRING, ['igual', 'diferente', 'contem'])
])
FILTROS_COLUNAS = dict([
    (NOMES_COLUNAS[0], TIPOS_FILTROS.get(STRING)),
    (NOMES_COLUNAS[1], TIPOS_FILTROS.get(NUMERICO)),
    (NOMES_COLUNAS[2], TIPOS_FILTROS.get(NUMERICO)),
    (NOMES_COLUNAS[3], TIPOS_FILTROS.get(NUMERICO)),
    (NOMES_COLUNAS[4], TIPOS_FILTROS.get(NUMERICO)),
    (NOMES_COLUNAS[5], TIPOS_FILTROS.get(NUMERICO))
])


def cabecalho_programa():
    """
    Funcao que exibe o cabecalho do programa
    """
    print('###########################################################################')
    print('#                Pesquisa Climatica Itapetininga 1998 - 2018              #')
    print('#                   Atividade de Avaliacao Substitutiva P2                #')
    print('#                Curso: Analise e Desenvolviemnto de Sistemas             #')
    print('#                               Ciclo: 3                                  #')
    print('#                            2o Semestre / 2020                           #')
    print('#                             Periodo Noturno                             #')
    print('###########################################################################')
    print('#                    Software Desenvolvido pelos alunos:                  #')
    print('#                    * Arthur Ferrarezi                                   #')
    print('#                    * Cassia Leonel                                      #')
    print('#                    * Vinicius Campos                                    #')
    print('###########################################################################')
    print('#                    Software Desenvolvido sob a licensa MIT              #')
    print('#    https://github.com/wartocampos/pesq_clima_itape_1998_2018.git        #')
    print('###########################################################################')
    print('')

def obrigado():
    print('###########################################################################')
    print('#              Muito obrigado por utilizar nossa aplicacao                #')
    print('###########################################################################')

def ler_arquivo_pesquisa_climatica():
    """
    Funcao que faz a leitura do arquivo de pesquisa climatica
    :return: lista dos dados consolidados da pesquisa
    """
    print('Carregando os dados da pesquisa.')
    dados = pd.read_csv('./resources/pesquisa_clima_itapetining_1998_2018.csv', delimiter=';')
    print('Dados da pesquisa carregados com sucesso.')
    return dados


def verifica_exibir_todos_dados(dados = None):
    """
    Funcao que questiona usuario se deseja exibir os dados da pesquisa
    """
    dados_exibir = dados_pesquisa if dados is None else dados
    texto_inicial = 'Voce deseja exibir os dados? (s/n)'
    texto_recorrente = 'Voce deseja exibir os dados novamente? (s/n)'
    iteracoes = 0
    exibir_dados = True
    while exibir_dados:
        resposta = ler_entrada_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        exibir_dados = (resposta is not None) and (resposta.strip().lower() == 's')
        if exibir_dados:
            iteracoes += 1
            print(dados_exibir)


def ordernar_dados(nome_coluna, tipo_ordenacao, dados = None):
    """
    Funcao que fara a ordenacao dos dados.
    :param nome_coluna: nome da coluna para ordernar os dados.
    :param tipo_ordenacao: ascendente ou descendente
    :return: dados ordenados
    """
    dados = dados_pesquisa if dados is None else dados
    if nome_coluna not in NOMES_COLUNAS:
        raise Exception('Nome de coluna invalido.')
    if tipo_ordenacao not in [ASC, DESC]:
        raise Exception('Tipo de ordenacao invalido.')
    return dados.sort_values(by=[nome_coluna], ascending=(tipo_ordenacao == ASC))


def verifica_ordernar_dados():
    """
    Funcao que verifica se usuario deseja ordernar dados
    :return: dados ordenados
    """
    texto_inicial = 'Voce deseja ordernar os dados? (s/n)'
    texto_recorrente = 'Voce deseja mudar a ordenacao dos dados? (s/n)'
    iteracoes = 0
    ordernar = True
    dados = None
    while ordernar:
        resposta = ler_entrada_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        ordernar = (resposta is not None) and (resposta.strip().lower() == 's')
        if ordernar:
            iteracoes += 1
            nome_coluna = ler_entrada_usuario(f'Favor escolher uma das colunas: {NOMES_COLUNAS}')
            tipo_ordenacao = ler_entrada_usuario(f'Favor escolher o tipo de ordenacao: {ASC, DESC}')
            try:
                dados = ordernar_dados(nome_coluna, tipo_ordenacao, dados)
                verifica_exibir_todos_dados(dados)
            except Exception as erro:
                print(erro)
    return dados


def filtrar_dados(nome_coluna, tipo_filtro, valor, dados = None):
    """
    Funcao que filtra dados baseado no nome da coluna e tipo de filtro.
    :param nome_coluna: nome da coluna a filtrar
    :param tipo_filtro: tipo de filtro
    :param valor: valor do filtro
    :return: dados filtrados
    """
    dados = dados_pesquisa if dados is None else dados
    if nome_coluna not in NOMES_COLUNAS:
        raise Exception('Nome de coluna invalido.')
    filtro_coluna = FILTROS_COLUNAS.get(nome_coluna)
    if tipo_filtro not in filtro_coluna:
        raise Exception('Nome de filtro invalido.')
    if filtro_coluna == TIPOS_FILTROS.get(STRING):
        if tipo_filtro == 'igual':
            return dados[dados[nome_coluna] == valor]
        elif tipo_filtro == 'diferente':
            return dados[dados[nome_coluna] != valor]
        else:
            return dados[str(valor).lower() in dados[nome_coluna].lower()]
    else:
        if DECIMAL_REGEX.match(str(valor)) is None:
            raise Exception('Valor do filtro nao possui valor numerico.')
        if tipo_filtro == 'maior':
            return dados[dados[nome_coluna] > float(valor)]
        elif tipo_filtro == 'menor':
            return dados[dados[nome_coluna] < float(valor)]
        elif tipo_filtro == 'igual':
            return dados[dados[nome_coluna] == float(valor)]
        else:
            return dados[dados[nome_coluna] != float(valor)]


def verifica_filtrar_dados(dados = None):
    """
    Funcao que verifica se usuario deseja filtrar dados
    :return: dados ordenados
    """
    dados = dados_pesquisa if dados is None else dados
    texto_inicial = 'Voce deseja filtrar os dados? (s/n)'
    texto_recorrente = 'Voce deseja adionar outro filtro aos dados? (s/n)'
    iteracoes = 0
    filtrar = True
    dados = None
    while filtrar:
        resposta = ler_entrada_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        filtrar = (resposta is not None) and (resposta.strip().lower() == 's')
        if filtrar:
            iteracoes += 1
            valor_filtro = None
            nome_coluna = ler_entrada_usuario(f'Favor escolher uma das colunas: {NOMES_COLUNAS}')
            filtro_coluna = FILTROS_COLUNAS.get(nome_coluna)
            tipo_filtro = ler_entrada_usuario(f'Favor escolher um tipo de filtro para {nome_coluna}: {filtro_coluna}')
            texto_valor_filtro = f'Por favor informe o valor do filtro para a coluna {nome_coluna}:'
            if filtro_coluna == TIPOS_FILTROS.get(STRING):
                valor_filtro = ler_entrada_usuario(texto_valor_filtro)
            else:
                valor_filtro = ler_numero_decimal(texto_valor_filtro)
            try:
                dados = filtrar_dados(nome_coluna, tipo_filtro, valor_filtro, dados)
                verifica_exibir_todos_dados(dados)
            except Exception as erro:
                print(erro)
    return dados


def exportar_dados(dados: None):
    """
    Funcao que exporta os dados do usuario para um arquivo csv
    """
    dados = dados_pesquisa if dados is None else dados


cabecalho_programa()
dados_pesquisa = ler_arquivo_pesquisa_climatica()
verifica_exibir_todos_dados()
dados_ordenados = verifica_ordernar_dados()
dados_filtrados = verifica_filtrar_dados(dados_ordenados)
exportar_dados(dados_filtrados)
obrigado()
