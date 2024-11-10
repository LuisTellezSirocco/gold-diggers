# main.py
# -*- coding: utf-8 -*-
"""
Script principal para realizar simulaciones hipotecarias y generar gráficos.
"""

from mortgage import Mortgage
from house import House
from simulations import MortgageSimulator
import sys


def main():
    print("=== Simulación de Hipotecas y Análisis de Propiedades ===\n")

    # Solicitar datos al usuario
    try:
        plazo_anios = int(input("Introduce el plazo en años: "))
        intereses_input = input("Introduce las tasas de interés anuales separadas por comas (%): ")
        intereses_anuales = [float(x.strip()) for x in intereses_input.split(',')]
        cantidad_minima = float(input("Introduce la cantidad mínima a financiar (€): "))
        cantidad_maxima = float(input("Introduce la cantidad máxima a financiar (€): "))
        incremento = float(input("Introduce el incremento de la cantidad (€): "))

        # Información adicional para House
        print("\n=== Información Adicional de la Propiedad ===")
        property_tax = float(input("Introduce el impuesto anual sobre la propiedad (€): "))
        home_insurance = float(input("Introduce el seguro anual de hogar (€): "))
        maintenance_cost = float(input("Introduce los costos anuales de mantenimiento (€): "))
        community_fees = float(input("Introduce los gastos de comunidad mensuales (€): "))
        utilities = float(input("Introduce los gastos mensuales de utilities (€): "))
    except ValueError:
        print("Entrada inválida. Asegúrate de introducir números correctamente.")
        sys.exit(1)

    # Crear instancias de Mortgage y House, y añadirlas al simulador
    simulator = MortgageSimulator()

    # Definir el capital base para las hipotecas
    # Este valor será escalado en los gráficos según la cantidad financiada
    base_capital = 100000  # €100,000

    for interes in intereses_anuales:
        mortgage = Mortgage(capital=base_capital, interest_rate=interes, term_years=plazo_anios)
        house = House(
            mortgage=mortgage,
            property_tax=property_tax,
            home_insurance=home_insurance,
            maintenance_cost=maintenance_cost,
            community_fees=community_fees,
            utilities=utilities
        )
        simulator.add_house(house)

    # Generar rango de cantidades
    import numpy as np
    amounts = np.arange(cantidad_minima, cantidad_maxima + incremento, incremento)

    # Seleccionar tipo de gráfico
    print("\n¿Qué gráfico deseas visualizar?")
    print("1. Cuota mensual vs. Cantidad financiada")
    print("2. Total a pagar vs. Cantidad financiada")
    print("3. Ambos gráficos")
    print("4. Análisis de Costos Totales de Casas")
    opcion = input("Selecciona una opción (1, 2, 3 o 4): ")

    plot_type = 'both'  # Predeterminado
    if opcion == '1':
        plot_type = 'monthly'
    elif opcion == '2':
        plot_type = 'total'
    elif opcion == '3':
        plot_type = 'both'
    elif opcion == '4':
        plot_type = 'both'  # Para análisis de casas, usaremos 'both'
    else:
        print("Opción no válida. Se mostrarán ambos gráficos por defecto.")
        plot_type = 'both'

    # Generar gráficos según la opción seleccionada
    if opcion in ['1', '2', '3']:
        simulator.plot_mortgages(amounts, plot_type=plot_type)
    elif opcion == '4':
        simulator.plot_houses(amounts, plot_type='both')
    else:
        simulator.plot_mortgages(amounts, plot_type=plot_type)


if __name__ == "__main__":
    main()

