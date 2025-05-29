import requests
import pandas as pd
import matplotlib.pyplot as plt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMTEwNDcyLCJpYXQiOjE3NDg1MTg0NTcsImp0aSI6IjY4NmVhZGU1Y2IyZTRmNTA5Yjg0OTg3OTI3NWFiYTY0IiwidXNlcl9pZCI6NzV9.kg06uYddVqlWmcn9lxNx5F8QWYnDQadOeQjN1La-kzo"
headers = {'Authorization': 'JWT {}'.format(token)}

def pegar_balanco(ticker, trimestre):
    empresa = f"{ticker}"
    data = f"{trimestre}"
    params = {
    'ticker': empresa,
    'ano_tri': data
    }
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco/',params=params, headers=headers)
    r.json().keys()
    dados = r.json()['dados'][0]
    balanco = dados['balanco']
    df = pd.DataFrame(balanco)
    return df

def preco_corrigido(ticker, dataini, datafim):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMTEwNDcyLCJpYXQiOjE3NDg1MTg0NTcsImp0aSI6IjY4NmVhZGU1Y2IyZTRmNTA5Yjg0OTg3OTI3NWFiYTY0IiwidXNlcl9pZCI6NzV9.kg06uYddVqlWmcn9lxNx5F8QWYnDQadOeQjN1La-kzo"
    headers = {'Authorization': 'JWT {}'.format(token)}
    empresa = f"{ticker}"
    data_ini = f"{dataini}"
    data_fim = f"{datafim}"
    params = {
    'ticker': empresa,
    'data_ini': data_ini,
    'data_fim': data_fim
    }
    if ticker=='ibov':
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos',params=params, headers=headers)
    else:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
    r.json().keys()
    dados = r.json()['dados']
    df = pd.DataFrame(dados)
    return df

def valor_acao(df):
    preco_ini = df.iloc[0]['fechamento']
    preco_fim = df.iloc[-1]['fechamento']
    preco_acao = preco_fim/preco_ini
    return {
        'preco_ini' : preco_ini,
        'preco_fim' : preco_fim,
        'preco_acao': preco_acao
    }

#Ativo Circulante
def valor_contabil(df, conta, descricao):
    filtro_conta = df[ 'conta'].str. contains (conta, case=False)
    filtro_descricao = df[ 'descricao']. str. contains (descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao] ['valor'].values)
    return valor

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df[ 'conta'].str. contains (conta, case=False)
    filtro_descricao = df[ 'descricao']. str. contains (descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao] ['valor'].values)
    return valor

def indices_basicos(df):
    Ativo_C = valor_contabil(df, '^1.0', '^ativo cir')
    Estoque = valor_contabil(df, '^1.0', '^estoque')
    Despesa_Antecipada = valor_contabil(df, '^1.0', '^despesa')
    Caixa = valor_contabil(df, '^1.0', '^caixa')
    Aplicacao_F = valor_contabil(df, '^1.0', '^aplica')
    Disponivel = Caixa + Aplicacao_F
    Ativo_RNC = valor_contabil(df, '^1.0*', '^ativo realiz')
    Ativo_NR = valor_contabil(df,'^1.*','^invest') + valor_contabil(df,'^1.*','^imobilizado$') + valor_contabil(df,'^1.*','^intang*')
    Passivo_C = valor_contabil(df, '^2.0', '^passivo cir')
    Passivo_NC = valor_contabil(df, '^2.0*', '^passivo n.o cir')
    Patrimonio_L = valor_contabil(df,'^2.*','patrim.nio')
    POn = (valor_contabil(df, '^2.01', '^empr.stimo'))+(valor_contabil(df, '^2.02', '^empr.stimo'))+(valor_contabil(df, '^2.01', '^deb.ntures'))+(valor_contabil(df, '^2.02', '^deb.ntures'))
    Imposto_de_renda_AC = valor_contabil(df, '^1.0', '^imposto de renda')
    Emprestimos = valor_contabil(df, '^2.0', '^empr.stimo')
    Provisoes = valor_contabil(df, '^2.0', '^provis.es')
    Imposto_de_renda_PC = valor_contabil(df, '^2.0', '^imposto de renda')
    Dividendos = valor_contabil_2(df, '^2.0', '^dividendos')
    Ativo_T = valor_contabil(df,'^1.*','ativo total')
    Investimento = POn + Patrimonio_L
    IR_Corrente = (valor_contabil(df, '^3.0', '^imposto de renda'))*(-1)
    Lair = valor_contabil_2(df, '^3.0', 'antes')
    Despesa_Financeira =  (valor_contabil(df,'^3.*','^despesas financeiras'))*(-1)
    investimentos = valor_contabil(df,'^1.*','^invest')
    imobilizado = valor_contabil(df,'^1.*','^imobilizado$')
    intangivel = valor_contabil(df,'^1.*','^intang*')
    Custo_MV = valor_contabil(df,'^3.*','custo')
    Clientes = valor_contabil(df,'^1.*','clientes')
    Receita_liquida = valor_contabil(df,'^3.*','receita')
    Fornecedor = valor_contabil(df,'^2.*','fornecedor')
    Ebit = valor_contabil(df, '^3.0', 'Resultado Antes do Resultado')
    Amortizacao = valor_contabil(df, '^6.0', 'Amortiza')
    Lucro_Liquido = valor_contabil(df, '^3.', 'Consolidado')
    Ke = 0.1725
    
    return {
        'Ativo_C'            : Ativo_C,
        'Estoque'            : Estoque,
        'Despesa_Antecipada' : Despesa_Antecipada,
        'Caixa'              : Caixa,
        'Aplicacao_F'        : Aplicacao_F,
        'Disponivel'         : Disponivel,
        'Ativo_RNC'          : Ativo_RNC,
        'Ativo_NR'           : Ativo_NR,
        'Passivo_C'          : Passivo_C,
        'Passivo_NC'         : Passivo_NC,
        'Patrimonio_L'       : Patrimonio_L,
        'POn'                : POn,
        'Imposto_de_renda_AC': Imposto_de_renda_AC,
        'Emprestimos'        : Emprestimos,
        'Provisoes'          : Provisoes,
        'Imposto_de_renda_PC': Imposto_de_renda_PC,
        'Dividendos'         : Dividendos,
        'Ativo_T'            : Ativo_T,
        'Investimento'       : Investimento,
        'IR_Corrente'        : IR_Corrente,
        'Lair'               : Lair,
        'Despesa_Financeira' : Despesa_Financeira,
        'investimentos'      : investimentos,
        'imobilizado'        : imobilizado,
        'intangivel'         : intangivel,
        'Custo_MV'           : Custo_MV,
        'Clientes'           : Clientes,
        'Receita_liquida'    : Receita_liquida,
        'Fornecedor'         : Fornecedor,
        'Ebit'               : Ebit,
        'Amortizacao'        : Amortizacao,
        'Lucro_Liquido'      : Lucro_Liquido,
        'Ke'                 : Ke
    }

def indices_liquidez(indices_basicos):
    Ativo_C = indices_basicos["Ativo_C"]
    Passivo_C = indices_basicos["Passivo_C"]
    Estoque = indices_basicos["Estoque"]
    Despesa_Antecipada = indices_basicos["Despesa_Antecipada"]
    Disponivel = indices_basicos["Disponivel"]
    Ativo_RNC = indices_basicos["Ativo_RNC"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    

    L_Corrente = Ativo_C / Passivo_C
    L_Seca = (Ativo_C - Estoque - Despesa_Antecipada) / Passivo_C
    L_Imediata = Disponivel / Passivo_C
    L_Geral = (Ativo_C + Ativo_RNC) / (Passivo_C + Passivo_NC)


    return {
        'L_Corrente': L_Corrente,
        'L_Seca'    : L_Seca,
        'L_Imediata': L_Imediata,
        'L_Geral'   : L_Geral,
    }

def indices_giro_tesouraria(indices_basicos):
    Ativo_C = indices_basicos["Ativo_C"]
    Passivo_C = indices_basicos["Passivo_C"]
    Disponivel = indices_basicos["Disponivel"]
    Imposto_de_renda_AC = indices_basicos["Imposto_de_renda_AC"]
    Emprestimos = indices_basicos["Emprestimos"]
    Provisoes = indices_basicos["Provisoes"]
    Imposto_de_renda_PC = indices_basicos["Imposto_de_renda_PC"]
    Dividendos = indices_basicos["Dividendos"]

    Ativo_CF = Disponivel + Imposto_de_renda_AC
    Ativo_CO = Ativo_C - Ativo_CF
    Passivo_CF = (Emprestimos + Provisoes + Imposto_de_renda_PC + Dividendos)
    Passivo_CO = (Passivo_C - Passivo_CF)
    #Capital de Giro
    Capital_de_Giro = Ativo_C - Passivo_C
    #Necessidade de Capital de Giro
    Necessidade_de_CG = Ativo_CO - Passivo_CO
    #Saldo Tesouraria
    Saldo_Tesouraria = Ativo_CF - Passivo_CF

    return {
        'Capital_de_Giro'   : Capital_de_Giro,
        'Necessidade_de_CG' : Necessidade_de_CG,
        'Saldo_Tesouraria'  : Saldo_Tesouraria,
    }

def indices_endividamento(indices_basicos):
    Passivo_C = indices_basicos["Passivo_C"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    Ativo_T = indices_basicos["Ativo_T"]

    CtCp = (Passivo_C + Passivo_NC) / Patrimonio_L
    Endividamento_geral = (Passivo_C + Passivo_NC) / (Passivo_C + Passivo_NC + Patrimonio_L)
    Solvencia = Ativo_T / (Passivo_C + Passivo_NC)
    Composicao_E = Passivo_C / (Passivo_C + Passivo_NC)

    return {
        'CtCp'               : CtCp,
        'Endividamento_geral': Endividamento_geral,
        'Solvencia'          : Solvencia,
        'Composicao_E'       : Composicao_E,
    }

def indices_emprestimos(indices_basicos):
    Passivo_C = indices_basicos["Passivo_C"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    Disponivel = indices_basicos["Disponivel"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    POn = indices_basicos["POn"]

    PFun = (Passivo_C+Passivo_NC)-POn
    Divida_liquida = POn - Disponivel
    Capital_Oneroso = Divida_liquida+Patrimonio_L
    Indice_DLPL = Divida_liquida/Patrimonio_L
    Indice_DLCO = Divida_liquida/Capital_Oneroso
    
    return {
        'PFun'            : PFun,
        'Indice_DLCO'     : Indice_DLCO,
        'Indice_DLPL'     : Indice_DLPL,
    }

def indices_juros(indices_basicos):
    POn = indices_basicos["POn"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    Investimento = indices_basicos["Investimento"]
    IR_Corrente = indices_basicos["IR_Corrente"]
    Nopat = Investimento/IR_Corrente
    Lair = indices_basicos["Lair"]
    Despesa_Financeira = indices_basicos["Despesa_Financeira"]

   #Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiananciamentos) e We(Peso do capital social)
    Wi = POn / Investimento
    We = Patrimonio_L / Investimento
    Aliquota = IR_Corrente / Lair
    Benefício_Tributário = Despesa_Financeira * Aliquota
    DF_Liquida = Despesa_Financeira - Benefício_Tributário
    #Ki(quanto que foi pago em relacao a divida total(em %))
    Ki = DF_Liquida / POn
    Ke = 0.17
    Custo_MPC = (Wi * Ki) + (We * Ke)

    return {
        'Custo_MPC' : Custo_MPC,
    }

def indice_valor_agregado(indices_basicos, indices_juros, indices_rentabilidade):
    Custo_MPC = indices_juros['Custo_MPC']
    Investimento = indices_basicos['Investimento']
    Ebit = indices_basicos['Ebit']
    Roe = indices_rentabilidade['Roe']
    Ke = indices_basicos['Ke']

    Eva = Ebit-(Investimento*Custo_MPC)
    Spread = Roe-Ke
    return {
        'Eva'    : Eva,
        'Spread' : Spread
    }

def indice_rentabilidade(indices_basicos):
    Investimento = indices_basicos['Investimento']
    Ebit = indices_basicos['Ebit']
    Amortizacao = indices_basicos['Amortizacao']
    IR_Corrente = indices_basicos['IR_Corrente']
    Lucro_Liquido = indices_basicos['Lucro_Liquido']
    Patrimonio_L = indices_basicos['Patrimonio_L']

    #Lucros antes da amortizacao e depois do imposto de renda
    Ebitda = Ebit + Amortizacao
    Nopat = Ebit - IR_Corrente
    #Retorno de Investimento(de financiamentos e capital social)
    Roi = Nopat/Investimento
    #Retorno do patrimonio(apenas capital social)
    Roe = Lucro_Liquido/Patrimonio_L
    #Grau de Alavancagem financeira
    Gaf = Roe/Roi

    return {
        'Ebitda': Ebitda,
        'Nopat' : Nopat,
        'Roi'   : Roi,
        'Roe'   : Roe,
        'Gaf'   : Gaf
    }

def indice_nao_realizavel(indices_basicos):
    investimentos = indices_basicos["investimentos"]
    imobilizado = indices_basicos["imobilizado"]
    intangivel = indices_basicos["intangivel"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]

    Indice_PL = (investimentos + intangivel + imobilizado) / Patrimonio_L

    return {
        'Indice_PL' : Indice_PL
    }

def indices_ciclos(basicos_23, basicos_24):
    Clientes_23 = basicos_23['Clientes']
    Fornecedor_23 = basicos_23['Fornecedor']
    Estoque_23 = basicos_23['Estoque']
    Custo_MV_24 = basicos_24['Custo_MV']
    Clientes_24 = basicos_24['Clientes']
    Receita_liquida_24 = basicos_24['Receita_liquida']
    Fornecedor_24 = basicos_24['Fornecedor']
    Estoque_24 = basicos_24['Estoque']
    
    #PME
    Estoque_med = (Estoque_23+Estoque_24)/2
    PM_Estocagem = ((Estoque_med*360)/Custo_MV_24)*(-1)
    #PMRV= (clientes med*360/Receita liquida))
    Clientes_med = (Clientes_23+Clientes_24)/2
    PM_Recebimento_V = (Clientes_med*360)/Receita_liquida_24
    #PMPF(fornecedor med*360/(Compra = Estoque Final - Estoque Inicial +CMV))
    Fornecedor_med = (Fornecedor_23+Fornecedor_24)/2
    compra = Estoque_24 - Estoque_23 + Custo_MV_24
    PM_Pagamento_F = ((Fornecedor_med*360)/compra)*(-1)
    #CO
    Ciclo_Operacional = PM_Estocagem + PM_Recebimento_V
    #CF
    Ciclo_Financeiro = Ciclo_Operacional - PM_Pagamento_F
    #CE
    Ciclo_Economico = PM_Estocagem
    return {
        'PM_Estocagem'     : PM_Estocagem,
        'PM_Recebimento_V' : PM_Recebimento_V,
        'PM_Pagamento_F'   : PM_Pagamento_F,
        'Ciclo_Operacional': Ciclo_Operacional,
        'Ciclo_Financeiro' : Ciclo_Financeiro,
        'Ciclo_Economico'  : Ciclo_Economico
    }

def print_dict(name, ticker, trimestre, data):
    print(f"{name} — {ticker} — {trimestre}")
    for key, value in data.items():
        print(f"  {key}: {value}")
    print()

def print_dict_2(name, ticker, dataini, datafim, valor_acao):
    print(f"{name} — {ticker} — {dataini}/{datafim}")
    for key, value in valor_acao.items():
        print(f"  {key}: {value}")
    print()

import matplotlib.pyplot as plt


import matplotlib.pyplot as plt

# Parâmetros
dataini = "2019-04-01"
datafim = "2025-03-31"
empresas = ["ABEV3", "JBSS3", "MRFG3", "BRFS3", "BEEF3", "MDIA3"]
cores = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

# Inicializa a figura e os eixos
fig, ax1 = plt.subplots(figsize=(14, 7))
ax2 = ax1.twinx()  # Eixo direito para IBOV

# Plotando ações no eixo esquerdo
for i, ticker in enumerate(empresas):
    try:
        df = preco_corrigido(ticker, dataini, datafim)
        if df.empty or 'fechamento' not in df.columns:
            print(f"Dados não disponíveis para {ticker}")
            continue
        df['retorno_normalizado'] = df['fechamento'] / df['fechamento'].iloc[0]
        ax1.plot(df['data'], df['retorno_normalizado'], label=ticker, color=cores[i])
    except Exception as e:
        print(f"Erro com {ticker}: {e}")

# Plotando IBOV no eixo direito
try:
    df_ibov = preco_corrigido('ibov', dataini, datafim)
    if not df_ibov.empty and 'fechamento' in df_ibov.columns:
        df_ibov['retorno_normalizado'] = df_ibov['fechamento'] / df_ibov['fechamento'].iloc[0]
        ax2.plot(df_ibov['data'], df_ibov['retorno_normalizado'], label='IBOV', color='black', linestyle='--', linewidth=2)
    else:
        print("Não foi possível obter dados do IBOV.")
except Exception as e:
    print(f"Erro com IBOV: {e}")

# Configuração dos eixos
ax1.set_xlabel('Data')
ax1.set_ylabel('Retorno Normalizado (Ações)')
ax2.set_ylabel('Retorno Normalizado (IBOV)')

# Legenda
linhas1, labels1 = ax1.get_legend_handles_labels()
linhas2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(linhas1 + linhas2, labels1 + labels2, loc='upper left')

# Estética final
plt.title(f"Comparação de Retorno Normalizado — Ações vs IBOV ({dataini} a {datafim})")
plt.grid(True)
plt.tight_layout()
plt.show()

