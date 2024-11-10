# house.py
# -*- coding: utf-8 -*-
"""
Módulo House

Contiene la definición de la clase House para gestionar los costos asociados a una propiedad.
"""

from mortgage import Mortgage


class House:
    """
    Representa una casa con todos los costos asociados, incluyendo hipoteca, impuestos, seguros, etc.
    """

    def __init__(self, mortgage: Mortgage, property_tax: float, home_insurance: float,
                 maintenance_cost: float, community_fees: float, utilities: float):
        """
        Inicializa una nueva instancia de la clase House.

        :param mortgage: Instancia de Mortgage asociada a la propiedad.
        :param property_tax: Impuesto anual sobre la propiedad (€).
        :param home_insurance: Seguro de hogar anual (€).
        :param maintenance_cost: Costos anuales de mantenimiento (€).
        :param community_fees: Gastos de comunidad mensuales (€).
        :param utilities: Gastos mensuales de utilities (€).
        """
        self.mortgage = mortgage
        self.property_tax = property_tax
        self.home_insurance = home_insurance
        self.maintenance_cost = maintenance_cost
        self.community_fees = community_fees
        self.utilities = utilities

    def monthly_property_tax(self) -> float:
        """
        Calcula el impuesto mensual sobre la propiedad.

        :return: Impuesto mensual (€).
        """
        return self.property_tax / 12

    def monthly_home_insurance(self) -> float:
        """
        Calcula el seguro de hogar mensual.

        :return: Seguro mensual (€).
        """
        return self.home_insurance / 12

    def monthly_maintenance_cost(self) -> float:
        """
        Calcula el costo de mantenimiento mensual.

        :return: Costo mensual (€).
        """
        return self.maintenance_cost / 12

    def total_monthly_cost(self) -> float:
        """
        Calcula el costo total mensual de la propiedad.

        :return: Costo total mensual (€).
        """
        return (
            self.mortgage.calculate_monthly_payment() +
            self.monthly_property_tax() +
            self.monthly_home_insurance() +
            self.monthly_maintenance_cost() +
            self.community_fees +
            self.utilities
        )

    def generate_detailed_schedule(self) -> list:
        """
        Genera un cuadro de amortización detallado incluyendo otros costos.

        :return: Lista de diccionarios con detalles de cada mes.
        """
        amortization_schedule = self.mortgage.generate_amortization_schedule()
        detailed_schedule = []

        for payment in amortization_schedule:
            month = payment['Mes']
            cuota = payment['Cuota']
            interes = payment['Interés']
            capital_amortizado = payment['Capital Amortizado']
            saldo_pendiente = payment['Saldo Pendiente']

            # Cálculos de costos adicionales
            property_tax = self.monthly_property_tax()
            home_insurance = self.monthly_home_insurance()
            maintenance = self.monthly_maintenance_cost()
            community = self.community_fees
            utilities = self.utilities

            # Costo total del mes
            total_cost = cuota + property_tax + home_insurance + maintenance + community + utilities

            detailed_schedule.append({
                'Mes': month,
                'Cuota': round(cuota, 2),
                'Interés': round(interes, 2),
                'Capital Amortizado': round(capital_amortizado, 2),
                'Saldo Pendiente': round(saldo_pendiente, 2),
                'Impuesto Propiedad': round(property_tax, 2),
                'Seguro Hogar': round(home_insurance, 2),
                'Mantenimiento': round(maintenance, 2),
                'Gastos Comunidad': round(community, 2),
                'Utilities': round(utilities, 2),
                'Costo Total Mes': round(total_cost, 2)
            })

            if saldo_pendiente == 0:
                break

        return detailed_schedule

    def __str__(self):
        return (
            f"House(mortgage={self.mortgage}, property_tax={self.property_tax}, "
            f"home_insurance={self.home_insurance}, maintenance_cost={self.maintenance_cost}, "
            f"community_fees={self.community_fees}, utilities={self.utilities})"
        )
