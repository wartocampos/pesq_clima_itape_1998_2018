import pandas as pd
import matplotlib.pyplot as plt
from utilitarios import ler_entrada_usuario

ASC = 'ascendente'
DESC = 'descendente'
STRING = 'string'
NUMERICO = 'numerico'
nomes_colunas = ['mes', 'dia', 'temperatura_media', 'temperatura_maxima', 'temperatura_minima', 'precipitacao_media']
tipos_filtros = dict([
    (NUMERICO, ['maior', 'menor', 'igual', 'diferente', 'entre']),
    (STRING, ['igual', 'diferente', 'contem'])
])
filtros_colunas = dict([
    (nomes_colunas[0], tipos_filtros[STRING]),
    (nomes_colunas[1], tipos_filtros[NUMERICO]),
    (nomes_colunas[2], tipos_filtros[NUMERICO]),
    (nomes_colunas[3], tipos_filtros[NUMERICO]),
    (nomes_colunas[4], tipos_filtros[NUMERICO]),
    (nomes_colunas[5], tipos_filtros[NUMERICO])
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


def ler_arquivo_pesquisa_climatica():
    """
    Funcao que faz a leitura do arquivo de pesquisa climatica
    :return: lista dos dados consolidados da pesquisa
    """
    print('Carregando os dados da pesquisa.')
    return pd.read_csv('./resources/pesquisa_clima_itapetining_1998_2018.csv', delimiter=';')


def verifica_exibir_todos_dados():
    """
    Funcao que questiona usuario se deseja exibir os dados da pesquisa
    """
    texto_inicial = 'Voce deseja exibir todos os dados? (s/n)'
    texto_recorrente = 'Voce deseja exibir todos os dados novamente? (s/n)'
    iteracoes = 0
    exibir_dados = True
    while exibir_dados:
        resposta = ler_entrada_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        exibir_dados = (resposta is not None) and (resposta.strip().lower() == 's')
        if exibir_dados:
            iteracoes += 1
            print(dados)


def ordernar_dados(nome_coluna, tipo_ordenacao):
    """
    Funcao que fara a ordenacao dos dados.
    :param nome_coluna: nome da coluna para ordernar os dados.
    :param tipo_ordenacao: ascendente ou descendente
    :return:
    """
    global dados
    if nome_coluna not in nomes_colunas:
        raise Exception('Nome de coluna invalido.')
    if tipo_ordenacao not in [ASC, DESC]:
        raise Exception('Tipo de ordenacao invalido.')
    dados = dados.sort_values(by=[nome_coluna], ascending=(tipo_ordenacao == ASC))
    return dados


def verifica_ordernar_dados():
    """
    Funcao que verifica se usuario deseja ordernar dados
    """
    texto_inicial = 'Voce deseja ordernar os dados? (s/n)'
    texto_recorrente = 'Voce deseja ordernar os dados novamente? (s/n)'
    iteracoes = 0
    ordernar = True
    while ordernar:
        resposta = ler_entrada_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        ordernar = (resposta is not None) and (resposta.strip().lower() == 's')
        if ordernar:
            iteracoes += 1
            nome_coluna = ler_entrada_usuario(f'Favor escolher alguma das colunas: {nomes_colunas}')
            tipo_ordenacao = ler_entrada_usuario(f'Favor escolher o tipo de ordenacao: {ASC, DESC}')
            try:
                ordernar_dados(nome_coluna, tipo_ordenacao)
                verifica_exibir_todos_dados()
            except Exception as erro:
                print(erro)


cabecalho_programa()
dados = ler_arquivo_pesquisa_climatica()
verifica_exibir_todos_dados()
verifica_ordernar_dados()
