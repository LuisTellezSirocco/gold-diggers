# simulations.py
# -*- coding: utf-8 -*-
"""
Módulo simulations

Contiene la definición de la clase MortgageSimulator para realizar simulaciones hipotecarias avanzadas.
"""

from mortgage import Mortgage
from house import House
import math


class MortgageSimulator:
    """
    Simula diferentes escenarios hipotecarios, como comparar hipotecas y calcular intereses necesarios según condiciones específicas.
    """

    def __init__(self):
        """
        Inicializa una nueva instancia de MortgageSimulator.
        """
        self.mortgages = []
        self.houses = []

    def add_mortgage(self, mortgage: Mortgage):
        """
        Añade una instancia de Mortgage a la simulación.

        :param mortgage: Instancia de Mortgage.
        """
        self.mortgages.append(mortgage)

    def add_house(self, house: House):
        """
        Añade una instancia de House a la simulación.

        :param house: Instancia de House.
        """
        self.houses.append(house)

    def compare_mortgages(self):
        """
        Compara las hipotecas añadidas mostrando sus cuotas mensuales y totales a pagar.
        """
        print("=== Comparativa de Hipotecas ===\n")
        for mortgage in self.mortgages:
            monthly_payment = mortgage.calculate_monthly_payment()
            total_payment = mortgage.calculate_total_payment()
            print(f"{mortgage}")
            print(f"Cuota Mensual: {monthly_payment:.2f} €")
            print(f"Total a Pagar: {total_payment:.2f} €\n")

    def compare_houses(self):
        """
        Compara las casas añadidas mostrando sus costos totales mensuales.
        """
        print("=== Comparativa de Casas ===\n")
        for house in self.houses:
            total_monthly = house.total_monthly_cost()
            print(f"{house}")
            print(f"Costo Total Mensual: {total_monthly:.2f} €\n")

    def calculate_required_interest(
        self, capital: float, term_years: int, max_monthly_payment: float
    ) -> float:
        """
        Calcula la tasa de interés anual necesaria para una hipoteca dada una cuota mensual máxima.

        :param capital: Cantidad de dinero a financiar (€).
        :param term_years: Plazo del préstamo en años.
        :param max_monthly_payment: Cuota mensual máxima (€).
        :return: Tasa de interés anual requerida (%).
        """
        term_months = term_years * 12

        def objective_function(interest_rate):
            mortgage = Mortgage(capital, interest_rate, term_years)
            return mortgage.calculate_monthly_payment() - max_monthly_payment

        # Utilizamos el método de búsqueda binaria para encontrar la tasa de interés
        lower_bound = 0.0
        upper_bound = 100.0  # Un límite superior muy alto para asegurar convergencia
        tolerance = 1e-6
        max_iterations = 1000
        iterations = 0

        while iterations < max_iterations:
            mid_rate = (lower_bound + upper_bound) / 2
            payment = Mortgage(
                capital, mid_rate, term_years
            ).calculate_monthly_payment()
            if abs(payment - max_monthly_payment) < tolerance:
                return mid_rate
            elif payment > max_monthly_payment:
                upper_bound = mid_rate
            else:
                lower_bound = mid_rate
            iterations += 1

        raise ValueError(
            "No se pudo encontrar una tasa de interés adecuada dentro de los límites establecidos."
        )

    def plot_mortgages(self, amounts, plot_type="both"):
        """
        Genera gráficos comparativos para las hipotecas añadidas.

        :param amounts: Lista de cantidades financiadas (€).
        :param plot_type: Tipo de gráfico a generar ('monthly', 'total', 'both').
        """
        from plot_utils import (
            plot_monthly_payment_vs_amount,
            plot_total_payment_vs_amount,
            plot_both,
        )

        if plot_type == "monthly":
            plot_monthly_payment_vs_amount(self.mortgages, amounts)
        elif plot_type == "total":
            plot_total_payment_vs_amount(self.mortgages, amounts)
        elif plot_type == "both":
            plot_both(self.mortgages, amounts)
        else:
            print("Tipo de gráfico no válido. Selecciona 'monthly', 'total' o 'both'.")

    def plot_houses(self, amounts, plot_type="both"):
        """
        Genera gráficos comparativos para las casas añadidas.

        :param amounts: Lista de cantidades financiadas (€).
        :param plot_type: Tipo de gráfico a generar ('monthly', 'total', 'both').
        """
        from plot_utils import (
            plot_monthly_payment_vs_amount,
            plot_total_payment_vs_amount,
            plot_both,
        )

        # En este caso, plot_mortgages no es directamente aplicable.
        # En su lugar, crearemos gráficos personalizados para House.

        import plotly.graph_objs as go
        from plotly.subplots import make_subplots

        if plot_type == "both":
            fig = make_subplots(
                rows=1, cols=2, subplot_titles=("Costo Total Mensual", "Total a Pagar")
            )
        elif plot_type == "monthly":
            fig = go.Figure()
        elif plot_type == "total":
            fig = go.Figure()
        else:
            print("Tipo de gráfico no válido. Selecciona 'monthly', 'total' o 'both'.")
            return

        for idx, house in enumerate(self.houses):
            # Costo Total Mensual
            if plot_type in ["monthly", "both"]:
                total_monthly = house.total_monthly_cost()
                trace_monthly = go.Scatter(
                    x=amounts,
                    y=[
                        total_monthly * (amount / house.mortgage.capital)
                        for amount in amounts
                    ],
                    mode="lines",
                    name=f"{house.mortgage.interest_rate}% TIN",
                    hovertemplate="Cantidad: %{x:.2f} €<br>Costo Total Mensual: %{y:.2f} €<extra></extra>",
                )
                if plot_type == "monthly":
                    fig.add_trace(trace_monthly)
                else:
                    fig.add_trace(trace_monthly, row=1, col=1)

            # Total a Pagar (Incluye hipoteca y otros costos)
            if plot_type in ["total", "both"]:
                total_payment = house.mortgage.calculate_total_payment()
                # Incluye impuestos, seguros, mantenimiento, etc.
                total_additional = (
                    house.property_tax
                    + house.home_insurance
                    + house.maintenance_cost
                    + (house.community_fees + house.utilities) * 12
                )
                total_pagar = total_payment + total_additional
                trace_total = go.Scatter(
                    x=amounts,
                    y=[
                        total_pagar * (amount / house.mortgage.capital)
                        for amount in amounts
                    ],
                    mode="lines",
                    name=f"{house.mortgage.interest_rate}% TIN",
                    hovertemplate="Cantidad: %{x:.2f} €<br>Total a Pagar: %{y:.2f} €<extra></extra>",
                )
                if plot_type == "total":
                    fig.add_trace(trace_total)
                else:
                    fig.add_trace(trace_total, row=1, col=2)

        # Configurar diseño de los gráficos
        if plot_type == "both":
            fig.update_layout(
                title_text="Análisis Comparativo de Casas",
                legend_title="Tasas de Interés Anuales",
                hovermode="x unified",
                width=1200,
                height=600,
            )
            fig.update_xaxes(title_text="Cantidad Financiada (€)", row=1, col=1)
            fig.update_yaxes(title_text="Costo Total Mensual (€)", row=1, col=1)
            fig.update_xaxes(title_text="Cantidad Financiada (€)", row=1, col=2)
            fig.update_yaxes(title_text="Total a Pagar (€)", row=1, col=2)
        elif plot_type == "monthly":
            fig.update_layout(
                title="Costo Total Mensual vs. Cantidad Financiada",
                xaxis_title="Cantidad Financiada (€)",
                yaxis_title="Costo Total Mensual (€)",
                legend_title="Tasas de Interés Anuales",
                hovermode="x unified",
            )
        elif plot_type == "total":
            fig.update_layout(
                title="Total a Pagar vs. Cantidad Financiada",
                xaxis_title="Cantidad Financiada (€)",
                yaxis_title="Total a Pagar (€)",
                legend_title="Tasas de Interés Anuales",
                hovermode="x unified",
            )

        fig.show()


# Función de utilidad para cálculos específicos si es necesario
def calculate_interest_for_payment(capital, term_years, max_monthly_payment):
    """
    Calcula la tasa de interés necesaria para una hipoteca dada una cuota mensual máxima.

    :param capital: Cantidad de dinero a financiar (€).
    :param term_years: Plazo del préstamo en años.
    :param max_monthly_payment: Cuota mensual máxima (€).
    :return: Tasa de interés anual necesaria (%).
    """
    simulator = MortgageSimulator()
    required_interest = simulator.calculate_required_interest(
        capital, term_years, max_monthly_payment
    )
    return required_interest
