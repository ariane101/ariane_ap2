from modulo import (indice_valor_agregado, indice_rentabilidade, indices_basicos, indices_juros, pegar_balanco)
import pandas as pd
def main():
    list_ticker = ["ABEV3", "JBSS3", "MRFG3", "BRFS3", "BEEF3", "MDIA3"]
    list_trimestre = ["20244T"]
    df_comparacao = pd.DataFrame()
    ticker_repetido = []
    list_roe = []  
    list_eva = []  
    list_valor_agregado = []

    for ticker in list_ticker:
        for trimestre in list_trimestre:
            ticker_repetido.append(ticker)
            df = pegar_balanco(ticker, trimestre)
            basicos = indices_basicos(df)
            juros = indices_juros(basicos)
            rentabilidade = indice_rentabilidade(basicos)
            valor_agregado = indice_valor_agregado(basicos, juros, rentabilidade)

            roe = rentabilidade.get("Roe")  
            eva = valor_agregado.get("Eva") 

            list_roe.append(roe)
            list_eva.append(eva)
            list_valor_agregado.append(valor_agregado)

    df_roe_eva = pd.DataFrame({
        "ticker": ticker_repetido,
        "Roe": list_roe,
        "Eva": list_eva
    })

    print(df_roe_eva)
    df_valor_agregado = pd.DataFrame(list_valor_agregado)
main()

