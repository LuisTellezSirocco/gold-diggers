import pandas as pd
from typing import List, Tuple


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


def calcular_tasa_rendimiento_df(data, col="adj close", start_date=None, end_date=None):
    """
    Calcula la tasa de rendimiento a partir de datos de un DataFrame de pandas,
    ajustando 'start_date' y 'end_date' a las fechas más cercanas disponibles en cualquier dirección.

    Argumentos:
    data -- DataFrame de pandas que contiene los datos con fechas en el índice.
    col -- Nombre de la columna a usar para los cálculos (por defecto: 'adj close').
    start_date -- Fecha de inicio en formato 'YYYY-MM-DD' (opcional).
    end_date -- Fecha de fin en formato 'YYYY-MM-DD' (opcional).

    Devuelve:
    r -- Tasa de rendimiento (en decimal), o None si hay error.
    """
    try:
        # Si las fechas no están dadas, usar la primera y última fecha disponible
        if start_date is None:
            start_date = data.index.min()
        if end_date is None:
            end_date = data.index.max()

        # Convertir si es necesario
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Función auxiliar para encontrar la fecha más cercana en cualquier dirección
        def buscar_fecha_mas_cercana(fecha_objetivo, index):
            pos = index.searchsorted(fecha_objetivo)
            if pos == 0:
                return index[0]
            elif pos == len(index):
                return index[-1]
            antes = index[pos - 1]
            despues = index[pos]
            if abs((despues - fecha_objetivo).days) < abs(
                (antes - fecha_objetivo).days
            ):
                return despues
            else:
                return antes

        # Ajuste de start_date si no está en el índice
        if start_date not in data.index:
            start_date = buscar_fecha_mas_cercana(start_date, data.index)
            print(f"Fecha de inicio ajustada a la más cercana disponible: {start_date}")

        # Ajuste de end_date si no está en el índice
        if end_date not in data.index:
            end_date = buscar_fecha_mas_cercana(end_date, data.index)
            print(f"Fecha de fin ajustada a la más cercana disponible: {end_date}")

        # Obtener los valores de la columna en las fechas ajustadas
        VP = data.loc[start_date, col]
        VF = data.loc[end_date, col]

        # Calcular el número de periodos (en años) entre las fechas ajustadas
        n = (end_date - start_date).days / 365.25

        # Asegurarse de evitar divisiones por cero
        if VP == 0:
            print(
                "El valor inicial (VP) es 0, no es posible calcular la tasa de rendimiento."
            )
            return None

        # Cálculo de la tasa de rendimiento anualizada
        r = (VF / VP) ** (1 / n) - 1
        return r

    except Exception as e:
        print(f"Error al calcular la tasa de rendimiento: {e}")
        return None


def calcular_rentabilidad_ac_periodos(
    data: pd.DataFrame,
    periods_years: int = 5,
    col: str = "adj close",
    top: bool = True,
    sort_by_date: bool = False,
) -> List[Tuple[pd.Timestamp, pd.Timestamp, float]]:
    """
    Calcula el rendimiento acumulado de periodos de X años consecutivos
    en el DataFrame dado, ajustando las fechas de inicio y fin a las más cercanas
    si no están disponibles en el índice.

    Argumentos:
    data -- DataFrame de pandas que contiene los datos con fechas en el índice.
    col -- Nombre de la columna a usar para los cálculos (por defecto: 'adj close').
    top -- Si es True, devuelve los periodos ordenados por rendimiento acumulado.
    sort_by_date -- Si es True, ordena los periodos por fecha de inicio.
    
    Devuelve:
    results -- Lista de tuplas (periodo_inicio, periodo_fin, rendimiento_acumulado).
    """
    # Validaciones
    if not isinstance(data, pd.DataFrame):
        raise ValueError("El argumento 'data' debe ser un DataFrame de pandas.")
    if col not in data.columns:
        raise ValueError(f"La columna '{col}' no se encuentra en el DataFrame.")
    if not isinstance(periods_years, int) or periods_years <= 0:
        raise ValueError("El argumento 'periods_years' debe ser un entero positivo.")
    if not isinstance(top, bool):
        raise ValueError("El argumento 'top' debe ser un valor booleano.")

    results = []

    # Obtener el año mínimo y máximo del DataFrame
    min_year = data.index.min().year
    max_year = data.index.max().year

    # Para periodos de X años completos
    for start_year in range(min_year, max_year - periods_years + 1):
        # Definir el inicio y fin del periodo de X años
        period_start = pd.Timestamp(f"{start_year}-01-01")
        period_end = pd.Timestamp(f"{start_year + periods_years}-12-31")

        # Ajustar las fechas a las más cercanas anteriores usando 'asof'
        if period_start < data.index.min():
            continue  # Si el inicio está fuera del rango de la data, lo omitimos

        period_start_adjusted = data.index.asof(period_start)
        period_end_adjusted = data.index.asof(period_end)

        # Cálculo del rendimiento usando las fechas ajustadas
        r = calcular_tasa_rendimiento_df(
            data,
            start_date=period_start_adjusted,
            end_date=period_end_adjusted,
            col=col,
        )

        if r is not None:
            results.append((period_start_adjusted, period_end_adjusted, r))

    # Ordenar según el valor del rendimiento acumulado
    results = sorted(
        results, key=lambda x: x[2], reverse=top
    )  # De mayor a menor si top=True, menor a mayor si top=False

    # Si sort_by_date es True, ordenar por fecha de inicio
    if sort_by_date:
        results = sorted(results, key=lambda x: x[0])

    # Devolver los 5 resultados
    return results


def rendimiento_anual(data: pd.DataFrame, 
                      col: str = 'adj close',
                      sort_by_date: bool = False):
    """
    Calcula la tasa de rendimiento anual año por año.

    Argumentos:
    data -- DataFrame que contiene los datos con fechas en el índice.
    col -- Nombre de la columna a usar (por defecto 'adj close').
    sort_by_date -- Si es True, ordena los resultados por fecha.

    Devuelve:
    results -- Lista de tuplas (año, rendimiento).
    """
    results = []
    years = data.index.year.unique()
    for year in years:
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        r = calcular_tasa_rendimiento_df(data, start_date=start_date, end_date=end_date, col=col)
        results.append((year, r))
        
    results = sorted(results, key=lambda x: x[1])
        
    if sort_by_date:
        results = sorted(results, key=lambda x: x[0])
    return results 
