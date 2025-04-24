import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4MDg0NTIzLCJpYXQiOjE3NDU0OTI1MjMsImp0aSI6IjEzMGQ3Zjk3MTdmYjRiZTQ4NTIxYTdmNjU4ODViMmNiIiwidXNlcl9pZCI6Njd9.Bt6MrjstfFkgr9QMMux46wv5-GGsmU9VHP__OziBRgc"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'ticker': 'ABEV3',
'ano_tri': '20244T',
}

r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
r.json().keys()
dados = r.json()['dados'][0]
dados.keys()

df = pd.DataFrame(dados['balanco'])
file = df.to_excel("C:\\Users\\202403765021\\Documents\\análisedados\\ambev.xlsx")
filtro = df["descricao"].str.contains("ativo circulante", case = False)
ativo_circulante = df[filtro]["valor"].values[0]

filtro1 = df["descricao"].str.contains("passivo circulante", case = False)
passivo_circulante = df[filtro1]["valor"].values[0]
il = ativo_circulante/passivo_circulante

filtro2 = df[df["descricao"].str.contains("longo", case = False)][["conta", "descricao"]]
ativo_longo_prazo = df[filtro2]["valor"].values[0]

capital_giro = ativo_circulante - passivo_circulante
passivo_total = df[df["descricao"].str.contains("passivo tota", case = False)]["valor"].values[0]
pl = df[df["descricao"].str.contains("líquido consolidado", case = False)]["valor"].values[0]
endividamento = passivo_total / (passivo_total + pl)

ativo_total = passivo_total = df[df["descricao"].str.contains("ativo total", case = False)]["valor"].values[0]
solvencia = ativo_total/passivo_total

def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case= False)
    filtro_descricao = df[ 'descricao' ].str.contains(descricao, case = False)
    valor = sum(df[filtro_conta & filtro_descricao]['valor'].values)
    return valor

intagivel = valor_contabil(df, '^1.*','^Intang*')
imobilizado = valor_contabil(df, '^1.*', '^Imobilizado$')
investimento = valor_contabil(df, '^1.*', 'Invest')
ipl = (intagivel+imobilizado+investimento)/pl