from modulo import (indice_valor_agregado, indice_rentabilidade, indices_basicos, indices_juros, pegar_balanco)
import pandas as pd
def main():
    list_ticker = ["ABEV3", "JBSS3", "MRFG3", "BRFS3", "BEEF3", "MDIA3"]
    list_trimestre = ["20244T"]
    df_comparacao = pd.DataFrame()
    ticker_repetido = []
    list_roi = []  
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

            roi = rentabilidade.get("Roi")  
            eva = valor_agregado.get("Eva") 

            list_roi.append(roi)
            list_eva.append(eva)
            list_valor_agregado.append(valor_agregado)

    df_roi_eva = pd.DataFrame({
        "ticker": ticker_repetido,
        "Roi": list_roi,
        "Eva": list_eva
    })

    print(df_roi_eva)
    df_valor_agregado = pd.DataFrame(list_valor_agregado)
main()