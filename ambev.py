import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2ODc3NTMyLCJpYXQiOjE3NDQyODU1MzIsImp0aSI6IjQ4MjdkYzRiN2YyNzQ2ZjU4YWYzZDY0MzBjYjIzMjM2IiwidXNlcl9pZCI6NTh9.RMxgWlV4QftrzCrM-8gXrfYgQwRlgFQ6IxLedgVpwAg"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
    'ticker': 'ABEV3',
    'ano_tri': '20244T'
}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco/',params=params, headers=headers)
r.json()
r.json().keys()
dados = r.json()['dados'][0]
balanco = dados['balanco']
df = pd.DataFrame(balanco)
df2 = df.to_excel("C:\\Users\\marco\\OneDrive\\Área de Trabalho\\python facul\\ambev.xlsx")

#Ativo Circulante
filtro = df["descricao"].str.contains("ativo circulante", case = False)
ativo_circulante = df[filtro]["valor"].values[0]

#Passivo Cirulante
filtro1 = df["descricao"].str.contains("passivo circulante", case = False)
passivo_circulante = df[filtro1]["valor"].values[0]

#Ativo Total
ativo_total = df[df['descricao'].str.contains('Ativo Total', case=False)]["valor"].values[0]

#Passivo Total
passivo_total = df[df["descricao"].str.contains("passivo tota", case = False)]["valor"].values[0]

#Liquidez Corrente
liquidez_corrente = ativo_circulante / passivo_circulante

#Estoque
filtro2 = df['descricao'].str.contains('Estoque', case=False)
df[filtro2][['conta','descricao','valor']]
estoque = df[filtro2]['valor'].values[0]

#Caixa
filtro3 = df['descricao'].str.contains('Caixa', case=False)
df[filtro3][['conta','descricao','valor']]
caixa = df[filtro3]['valor'].values[0]

#Liquidez Seca
liquidez_seca = (ativo_circulante - estoque) / passivo_circulante

#Liquidez Imediata
liquidez_imediata = caixa / passivo_circulante

#Capital de Giro
capital_giro = ativo_circulante - passivo_circulante

#Liquidez Geral
filtro4 = df['descricao'].str.contains('longo', case=False)
df[filtro4][['conta','descricao','valor']]
realizavel_longoprazo = df[filtro4]['valor'].values[0]
liquidez_geral = (ativo_circulante + realizavel_longoprazo) / (passivo_circulante)

#Passivo Não Circulante
filtro5 = df['descricao'].str.contains('passivo não circulante', case=False)
df[filtro5][['conta', 'descricao', 'valor']]
passivo_naocirculante = df[filtro5]['valor'].values[0]

#Passivo (PC + PNC)
passivo = passivo_circulante + passivo_naocirculante

#Passivo Total e PL
passivo_total = df[df['descricao'].str.contains('Passivo Total', case=False)]["valor"].values[0]
pl = df[df['descricao'].str.contains('Patrimônio Líquido Consolidado', case=False)]["valor"].values[0]

#Endividamento Geral
endividamento_geral = passivo / (passivo + pl)

#Estrutura de Capital
estrutura_capital = passivo / pl

#Solvencia
solvencia = ativo_total / passivo

#CE (composição de endividamento)
composição_endividamento = passivo_circulante / passivo

#5 i's ()
def valor_contabil(df, conta, descricao):
    filtro_conta = df[ 'conta'].str. contains (conta, case=False)
    filtro_descricao = df[ 'descricao']. str. contains (descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao] ['valor'].values)
    return valor

#'conta='^1.*'
#descricao = 'imobi.*'
#filtro_conta = df['conta'].str.contains(conta, case=False)
#filtro_descricao = df['descricao'].str.contains(descricao, case=False)
#df[filtro_conta & filtro_descricao]'

intagivel = valor_contabil(df, '^1.','^Intang.')
imobilizado = valor_contabil(df, '^1.*','^Imobilizado$')
investimentos = valor_contabil(df, '^1.*', '^Investimento.$')
pl2 = valor_contabil(df, '^2.','patrim.nio')

#relação CT - CP passivo / PL
relação_CT_CP = passivo / pl2

#5i's
i = intagivel + imobilizado + investimentos

#IPL
ipl = (intagivel + imobilizado + investimentos) / pl2


import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2ODc3NTMyLCJpYXQiOjE3NDQyODU1MzIsImp0aSI6IjQ4MjdkYzRiN2YyNzQ2ZjU4YWYzZDY0MzBjYjIzMjM2IiwidXNlcl9pZCI6NTh9.RMxgWlV4QftrzCrM-8gXrfYgQwRlgFQ6IxLedgVpwAg"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
    'ticker': 'ABEV3',
    'ano_tri': '20234T'
}
r2 = requests.get('https://laboratoriodefinancas.com/api/v1/balanco/',params=params, headers=headers)
r2.json()
r2.json().keys()
dados2 = r2.json()['dados'][0]
balanco2 = dados2['balanco']
df3 = pd.DataFrame(balanco2)
df3.to_excel("C:\\Users\\marco\\OneDrive\\Área de Trabalho\\python facul\\ambev23.xlsx")
df4 = pd.read_excel("C:\\Users\\marco\\OneDrive\\Área de Trabalho\\python facul\\ambev23.xlsx")

#Estoque médio
estoque_24 = valor_contabil(df, "^1.0*", "estoque")
estoque_23 = valor_contabil(df4, "^1.0*", "estoque")
estoque_medio = (estoque_24 + estoque_23) / 2

#fornecedores médio
fornecedores_24 = valor_contabil(df, "^2.0*", "^Fornecedores$")
fornecedores_23 = valor_contabil(df4, "^2.0*", "^Fornecedores$")
fornecedores_medio = (fornecedores_24 + fornecedores_23) / 2

#clientes médio
clientes_24 = valor_contabil(df, "^1.0*", "^Clientes$")
contas_receber_24 = valor_contabil(df, "^1.0*", "^Contas a Receber$")

clientes_23 = valor_contabil(df4, "^1.0*", "^Clientes$")
contas_receber_23 = valor_contabil(df4, "^1.0*", "^Contas a Receber$")

clientes_medio = (clientes_24 + clientes_23) / 2


receita_24 = valor_contabil(df, "^7.0*", "^Receitas$")
cmv_24 = valor_contabil(df, "^3.0*", "^Custo dos Produtos$")*(-1)
compras = estoque_24 - estoque_23 + cmv_24 

#PME
pme = (estoque_medio / cmv_24)*360

#PMRV
pmrv = (clientes_medio / receita_24)*360

#PMPF
pmpf = (fornecedores_medio / compras)*360

#Ciclo Operacional (CO)
co = pme + pmrv 

#Ciclo Financeiro (CF)
cf = co - pmpf

#Ciclo Ecônomico (CE) 
ce = pme

#ACF
caixa_EC = valor_contabil(df, '^1.*','^Caixa e Equivalentes de Caixa$') / 2
operacoes_derivativos = valor_contabil(df, '^1.*','^Operações com Derivativos$') - 298888
credito_partes_relacionadas = valor_contabil(df, '^1.*','^Créditos com Partes Relacionadas$')

acf = caixa_EC + operacoes_derivativos + credito_partes_relacionadas

#PCF
emprestimos_financiamentos = valor_contabil(df, '^2.01.04$','^Empréstimos e Financiamentos$') 
ircsp = valor_contabil(df, '^2.*','^Imposto de Renda e Contribuição Social a Pagar$')
debito_partes_relacionadas = valor_contabil(df, '^2.*','^Débitos com Outras Partes Relacionadas$')
operacoes_derivativos2 = valor_contabil(df, '^2.01.05.02.05$','^Operaçoes com Derivativos$')
dividendos_JCP_pagar = valor_contabil(df, '^2.*','^Dividendos e JCP a Pagar$')
passivo_arrendamento_partesRelacionadas = valor_contabil(df, '^2.01.05.02.10$','^Passivo de arrendamento com partes relacionadas$')

pcf = emprestimos_financiamentos + ircsp + debito_partes_relacionadas + operacoes_derivativos2 +dividendos_JCP_pagar + passivo_arrendamento_partesRelacionadas

#ACO
aco = ativo_circulante - acf 

#PCO
pco = passivo_circulante - pcf 

#NCG
ncg = aco - pco

#ST
st = acf - pcf
