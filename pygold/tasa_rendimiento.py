import pandas as pd

def calcular_tasa_rendimiento(VP, n, VF):
    """
    Calcula la tasa de rendimiento a partir de VP, n y VF.

    Argumentos:
    VP -- Valor presente o cantidad inicial invertida.
    n -- Número de períodos.
    VF -- Valor futuro de la inversión.

    Devuelve:
    r -- Tasa de rendimiento.
    """
    r = (VF / VP) ** (1 / n) - 1
    return r

def calcular_tasa_rendimiento_df(data, col='adj close', start_date=None, end_date=None):
    """
    Calcula la tasa de rendimiento a partir de datos de un DataFrame de pandas.

    Argumentos:
    data -- DataFrame de pandas que contiene los datos con fechas en el índice.
    col -- Nombre de la columna a usar para los cálculos (por defecto: 'adj close').
    start_date -- Fecha de inicio en formato 'YYYY-MM-DD' (opcional).
    end_date -- Fecha de fin en formato 'YYYY-MM-DD' (opcional).

    Devuelve:
    r -- Tasa de rendimiento (en decimal), o None si hay error.
    """
    try:
        # Si las fechas no están dadas, tomar el primer y último valor disponible
        if start_date is None:
            start_date = data.index.min()  # Primera fecha disponible
        if end_date is None:
            end_date = data.index.max()    # Última fecha disponible

        # Verificamos si las fechas están dentro del rango del índice del DataFrame
        if pd.to_datetime(start_date) not in data.index or pd.to_datetime(end_date) not in data.index:
            print("Fechas fuera de rango en el DataFrame")
            return None

        # Valores de la columna en las fechas dadas
        VP = data.loc[start_date, col]
        VF = data.loc[end_date, col]

        # Número de períodos entre las fechas (en años, si las fechas son fechas completas)
        n = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365.25

        # Condición para evitar divisiones por cero
        if VP == 0:
            print("El valor presente (VP) es 0, no es posible calcular la tasa de rendimiento")
            return None

        # Cálculo de la tasa de rendimiento
        r = (VF / VP) ** (1 / n) - 1
        return r
    except Exception as e:
        print(f"Error al calcular la tasa de rendimiento: {e}")
        return None