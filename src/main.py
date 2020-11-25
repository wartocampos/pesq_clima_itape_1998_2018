import pandas as pd
import matplotlib.pyplot as plt
import datetime
import re
from utilitarios import ler_entrada_usuario, ler_numero_decimal, ler_confirmacao_usuario, DECIMAL_REGEX

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
LISTA_DE_CORES = [
    '#A9A9A9', '#836FFF', '#00BFFF', '#7FFFD4', '#00FF7F', '#228B22',
    '#DAA520', '#D2691E', '#D2B48C', '#FF00FF', '#DC143C', '#A52A2A',
    '#FF0000', '#FFA500', '#FFFF00', '#F0F8FF', '#EEE8AA', '#FFF0F5',
    '#D8BFD8', '#B0E0E6', '#F5F5F5', '#DDA0DD', '#696969', '#00BFFF',
    '#008080', '#8FBC8F', '#ADFF2F', '#DAA520', '#F0E68C', '#FDF5E6',
    '#F5FFFA'
]
MESES_ANO = [
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]
INDICE_EIXO_X = 'x'
INDICE_EIXO_Y = 'y'


def iniciar_configuracao():
    """
    Funcao que inicializa configuracoes que serao utilizadas ao longo do programa.
    """
    pd.set_option("display.max_rows", None, "display.max_columns", None)


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


def rodape_programa():
    print('')
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


def verifica_exibir_todos_dados(dados=None):
    """
    Funcao que questiona usuario se deseja exibir os dados da pesquisa
    """
    dados_exibir = dados_pesquisa if dados is None else dados
    texto_inicial = 'Voce deseja exibir os dados? (s/n)'
    texto_recorrente = 'Voce deseja exibir os dados novamente? (s/n)'
    iteracoes = 0
    exibir_dados = True
    while exibir_dados:
        resposta = ler_confirmacao_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
        exibir_dados = (resposta is not None) and (resposta.strip().lower() == 's')
        if exibir_dados:
            iteracoes += 1
            print(dados_exibir)


def ordernar_dados(nome_coluna, tipo_ordenacao, dados=None):
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
        resposta = ler_confirmacao_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
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


def filtrar_dados(nome_coluna, tipo_filtro, valor, dados=None):
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


def verifica_filtrar_dados(dados=None):
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
        resposta = ler_confirmacao_usuario(texto_inicial if iteracoes == 0 else texto_recorrente)
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


def exportar_dados(dados=None):
    """
    Funcao que exporta os dados do usuario para um arquivo csv
    """
    dados = dados_pesquisa if dados is None else dados
    horario_agora = datetime.datetime.now()
    nome_arquivo = f'./export_{horario_agora.strftime("%d_%m_%Y_%H_%M_%S")}.csv'
    dados = dados_pesquisa if dados is None else dados
    print('Exportando dados.')
    dados.to_csv(nome_arquivo, index=False, sep=';')
    print(f'Dados exportados no arquivo: {nome_arquivo}')


def verifica_exportar_dados(dados=None):
    """
    Funcao que verifica se usuario deseja exportar dados
    """
    dados = dados_pesquisa if dados is None else dados
    resposta = ler_confirmacao_usuario("Voce deseja exportar esses dados? (s/n)")
    if (resposta is not None) and (resposta.strip().lower() == 's'):
        exportar_dados(dados)


def retornar_dados_grafico_precipitacao_media():
    """
    Funcao que retorna os dados para grafico de precipitacao media.
    :return: dados do grafico em um dicionario com chaves x e y.
    """
    dados = filtrar_dados('mes', 'igual', 'Junho', dados_pesquisa)
    return dict([
        (INDICE_EIXO_X, dados['dia']),
        (INDICE_EIXO_Y, dados['precipitacao_media'])
    ])


def retornar_dados_grafico_temperatura_minima():
    """
    Funcao que retorna os dados para grafico de media de temperatura minima.
    :return: dados do grafico em um dicionario com chaves x e y.
    """
    dados = filtrar_dados('mes', 'igual', 'Junho', dados_pesquisa)
    return dict([
        (INDICE_EIXO_X, dados['dia']),
        (INDICE_EIXO_Y, dados['temperatura_minima'])
    ])


def retornar_dados_volume_pluviometrico_medio():
    """
    Funcao que retorna os de volume pluviometrico medio anual.
    :return: dados do em um dicionario com chaves Nome do Mes.
    """
    propriedade = 'precipitacao_media'
    dicionario = {}
    for indice in range(len(MESES_ANO)):
        mes_ano = MESES_ANO[indice]
        dicionario[mes_ano] = filtrar_dados('mes', 'igual', mes_ano, dados_pesquisa)[propriedade].mean()
    return dicionario


def retornar_dados_grafico_volume_pluviometrico_medio():
    """
    Funcao que retorna os dados para grafico de volume pluviometrico medio anual.
    :return: dados do grafico em um dicionario com chaves x e y.
    """
    dados = retornar_dados_volume_pluviometrico_medio()
    dados_eixo_y = []
    for indice in range(len(MESES_ANO)):
        mes_ano = MESES_ANO[indice]
        dados_eixo_y.append(dados.get(mes_ano))
    return dict([
        (INDICE_EIXO_X, MESES_ANO),
        (INDICE_EIXO_Y, dados_eixo_y)
    ])


def retornar_dados_grafico_distribuicao_chuva():
    """
    Funcao que retorna os dados para grafico de volume distribuicao de chuva.
    :return: dados do grafico em um dicionario com chaves x e y.
    """
    dados = retornar_dados_volume_pluviometrico_medio()
    dados_eixo_x = ['Primavera', 'Verao', 'Outono', 'Inverno']
    primavera = dados.get(MESES_ANO[10]) + dados.get(MESES_ANO[9]) + dados.get(MESES_ANO[8])
    verao = dados.get(MESES_ANO[11]) + dados.get(MESES_ANO[0]) + dados.get(MESES_ANO[1])
    outono = dados.get(MESES_ANO[2]) + dados.get(MESES_ANO[3]) + dados.get(MESES_ANO[4])
    inverno = dados.get(MESES_ANO[5]) + dados.get(MESES_ANO[6]) + dados.get(MESES_ANO[7])
    total = primavera + verao + outono + inverno
    dados_eixo_y = [
        (primavera / total) * 100,
        (verao / total) * 100,
        (outono / total) * 100,
        (inverno / total) * 100
    ]
    return dict([
        (INDICE_EIXO_X, dados_eixo_x),
        (INDICE_EIXO_Y, dados_eixo_y)
    ])


def gerar_graficos():
    """
    Funcao que gera 4 tipos de graficos: Precipitacao Media: Junho 1998-2018, Temperatura Minima: Junho 1998-2018, Volume Pluviometrico e Distribuicao de chuvas.
    """
    dados_precipitacao_media = retornar_dados_grafico_precipitacao_media()
    dados_temperatura_minima = retornar_dados_grafico_temperatura_minima()
    dados_pluviometrico_medio = retornar_dados_grafico_volume_pluviometrico_medio()
    dados_distribuicao_chuva = retornar_dados_grafico_distribuicao_chuva()
    fig, axs = plt.subplots(2, 2)
    # grafico de precipitacao media junho 1998 - 2018
    axs[0, 0].bar(dados_precipitacao_media.get(INDICE_EIXO_X), dados_precipitacao_media.get(INDICE_EIXO_Y), color=LISTA_DE_CORES)
    axs[0, 0].set_title('Precipitacao Media em Junho: 1998 - 2018')
    # grafico de media de temperatura minima 1998 - 2018
    axs[0, 1].bar(dados_temperatura_minima.get(INDICE_EIXO_X), dados_temperatura_minima.get(INDICE_EIXO_Y), color=LISTA_DE_CORES)
    axs[0, 1].set_title('Media de Temperatura Minima em Junho: 1998 - 2018')
    # grafico de volume medio pluviometrico anual
    axs[1, 0].plot(dados_pluviometrico_medio.get(INDICE_EIXO_Y))
    axs[1, 0].set_title('Volume Pluviometrico Medio: 1998 - 2018')
    # grafico de media de distribuicao de chuvas
    axs[1, 1].pie(dados_distribuicao_chuva.get(INDICE_EIXO_Y), labels=dados_distribuicao_chuva.get(INDICE_EIXO_X),
        colors=LISTA_DE_CORES, explode=(0, 0.1, 0, 0),  autopct='%1.1f%%')
    axs[1, 1].set_title('Media de Distribuicao de Chuvas: 1998 - 2018')


def verifica_gerar_graficos():
    """
    Funcao que verifica como o usuario deseja visualizar os graficos.
    """
    print('Gerando graficos.')
    gerar_graficos()
    print('Graficos gerados.')
    resposta = int(ler_entrada_usuario(
        'Escolha a opcao para visualizacao do grafico: 1 - Em uma nova janela, 2 - Salvar em um arquivo',
        re.compile("^[1|2]$"),
        'Opcao invalida.'
    ))
    if resposta == 1:
        plt.show()
    else:
        horario_agora = datetime.datetime.now()
        nome_arquivo = f'./graficos_{horario_agora.strftime("%d_%m_%Y_%H_%M_%S")}.png'
        print('Salvando graficos em um arquivo.')
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        fig.savefig(nome_arquivo, dpi=100)
        print(f'Grafico salvo no arquivo: {nome_arquivo}')


iniciar_configuracao()
cabecalho_programa()
dados_pesquisa = ler_arquivo_pesquisa_climatica()
verifica_exibir_todos_dados()
dados_ordenados = verifica_ordernar_dados()
dados_filtrados = verifica_filtrar_dados(dados_ordenados)
verifica_exportar_dados(dados_filtrados)
verifica_gerar_graficos()
rodape_programa()
