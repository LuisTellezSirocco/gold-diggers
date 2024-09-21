import yfinance as yf


def descargar_datos_yahoo(ticker, inicio, fin, intervalo="1d", acciones_split=False):
    """
    Función para descargar datos de Yahoo Finance.

    Parámetros:
    - ticker: Símbolo del ticker de la acción (por ejemplo, 'AAPL' para Apple Inc.).
    - inicio: Fecha de inicio en formato 'YYYY-MM-DD'.
    - fin: Fecha de fin en formato 'YYYY-MM-DD'.
    - intervalo: Frecuencia de los datos ('1d' para diarios, '1wk' para semanales, '1mo' para mensuales, etc.).
    - acciones_split: Booleano para incluir o no datos de divisiones de acciones.

    Retorna:
    - DataFrame con los datos descargados.
    """
    try:
        data = yf.download(
            ticker, start=inicio, end=fin, interval=intervalo, actions=acciones_split
        )
        data.columns = ["open", "high", "low", "close", "adj close", "volume"]
        data.index.name = "time"
        return data
    except Exception as e:
        print("Error al descargar datos:", e)
        return None
