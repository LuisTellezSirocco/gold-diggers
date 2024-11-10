# mortgage.py
# -*- coding: utf-8 -*-
"""
Módulo Mortgage

Contiene la definición de la clase Mortgage para realizar cálculos relacionados con hipotecas.
"""

import math


class Mortgage:
    """
    Representa una hipoteca con métodos para calcular cuotas mensuales, total a pagar y generar cuadros de amortización.
    """

    def __init__(self, capital: float, interest_rate: float, term_years: int):
        """
        Inicializa una nueva instancia de la clase Mortgage.

        :param capital: Cantidad de dinero a financiar (€).
        :param interest_rate: Tasa de interés anual (%) (TIN).
        :param term_years: Plazo del préstamo en años.
        """
        self.capital = capital
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.term_months = term_years * 12
        self.monthly_interest = interest_rate / (12 * 100)

    def calculate_monthly_payment(self) -> float:
        """
        Calcula la cuota mensual de la hipoteca utilizando la fórmula de amortización francesa.

        :return: Cuota mensual (€).
        """
        if self.monthly_interest == 0:
            return self.capital / self.term_months
        numerator = (
            self.capital
            * self.monthly_interest
            * (1 + self.monthly_interest) ** self.term_months
        )
        denominator = (1 + self.monthly_interest) ** self.term_months - 1
        return numerator / denominator

    def calculate_total_payment(self) -> float:
        """
        Calcula el total a pagar por la hipoteca a lo largo del plazo.

        :return: Total a pagar (€).
        """
        return self.calculate_monthly_payment() * self.term_months

    def generate_amortization_schedule(self) -> list:
        """
        Genera el cuadro de amortización de la hipoteca.

        :return: Lista de diccionarios con detalles de cada mes.
        """
        schedule = []
        remaining_balance = self.capital
        monthly_payment = self.calculate_monthly_payment()

        for month in range(1, self.term_months + 1):
            interest_payment = remaining_balance * self.monthly_interest
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            remaining_balance = max(remaining_balance, 0)  # Evita saldos negativos
            schedule.append(
                {
                    "Mes": month,
                    "Cuota": round(monthly_payment, 2),
                    "Interés": round(interest_payment, 2),
                    "Capital Amortizado": round(principal_payment, 2),
                    "Saldo Pendiente": round(remaining_balance, 2),
                }
            )
            if remaining_balance == 0:
                break

        return schedule

    def __str__(self):
        return (
            f"Mortgage(capital={self.capital}, interest_rate={self.interest_rate}, "
            f"term_years={self.term_years})"
        )
