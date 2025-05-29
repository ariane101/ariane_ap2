from modulo import (indice_valor_agregado, 
                    indice_rentabilidade, indices_basicos, 
                    indices_juros, pegar_balanco, preco_corrigido, 
                    print_dict, valor_acao, print_dict_2)
import pandas as pd
import requests
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


    list_ticker2 = []
    list_ticker2.append("ABEV3")
    list_ticker2.append("JBSS3")
    list_ticker2.append("MRFG3")
    list_ticker2.append("BRFS3")
    list_ticker2.append("BEEF3")
    list_ticker2.append("MDIA3")
    list_ticker2.append("ibov")

    list_df2 = []
    list_data_inicio = []
    list_data_inicio.append("2023-04-01")
    list_data_inicio.append("2019-04-01")
    list_data_inicio.append("2014-04-01")
    list_data_fim = []
    list_data_fim.append("2025-03-31")

    list_valor_acao = []
    for ticker in list_ticker2:
        for datafim in list_data_fim:
            for dataini in list_data_inicio:
                
                df = preco_corrigido(ticker, dataini, datafim)
                list_df2.append(df)
                valores_acao = valor_acao(df)
                
                list_valor_acao.append(valores_acao)
                print_dict_2("Valores da ação", ticker, dataini, datafim, valores_acao)
    
main()