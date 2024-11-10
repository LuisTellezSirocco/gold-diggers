# plot_utils.py
# -*- coding: utf-8 -*-
"""
Módulo plot_utils

Contiene funciones para generar gráficos utilizando Plotly.
"""

import plotly.graph_objs as go
from plotly.subplots import make_subplots


def plot_monthly_payment_vs_amount(mortgages, amounts, title="Cuota Mensual vs. Cantidad Financiada"):
    """
    Genera un gráfico de la cuota mensual en función de la cantidad financiada para diferentes tasas de interés.

    :param mortgages: Lista de instancias de Mortgage.
    :param amounts: Lista de cantidades financiadas (€).
    :param title: Título del gráfico.
    """
    fig = go.Figure()

    for mortgage in mortgages:
        payments = [mortgage.calculate_monthly_payment() * (amount / mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=payments,
            mode='lines',
            name=f'{mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Cuota: %{y:.2f} €<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Cantidad Financiada (€)',
        yaxis_title='Cuota Mensual (€)',
        legend_title='Tasas de Interés Anuales',
        hovermode='x unified'
    )
    fig.show()


def plot_total_payment_vs_amount(mortgages, amounts, title="Total a Pagar vs. Cantidad Financiada"):
    """
    Genera un gráfico del total a pagar en función de la cantidad financiada para diferentes tasas de interés.

    :param mortgages: Lista de instancias de Mortgage.
    :param amounts: Lista de cantidades financiadas (€).
    :param title: Título del gráfico.
    """
    fig = go.Figure()

    for mortgage in mortgages:
        totals = [mortgage.calculate_total_payment() * (amount / mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=totals,
            mode='lines',
            name=f'{mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Total a Pagar: %{y:.2f} €<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Cantidad Financiada (€)',
        yaxis_title='Total a Pagar (€)',
        legend_title='Tasas de Interés Anuales',
        hovermode='x unified'
    )
    fig.show()


def plot_both(mortgages, amounts):
    """
    Genera ambos gráficos (Cuota Mensual y Total a Pagar) en una sola visualización.

    :param mortgages: Lista de instancias de Mortgage.
    :param amounts: Lista de cantidades financiadas (€).
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Cuota Mensual", "Total a Pagar"))

    for idx, mortgage in enumerate(mortgages):
        # Cuota Mensual
        payments = [mortgage.calculate_monthly_payment() * (amount / mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=payments,
            mode='lines',
            name=f'{mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Cuota: %{y:.2f} €<extra></extra>'
        ), row=1, col=1)

        # Total a Pagar
        totals = [mortgage.calculate_total_payment() * (amount / mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=totals,
            mode='lines',
            name=f'{mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Total a Pagar: %{y:.2f} €<extra></extra>'
        ), row=1, col=2)

    fig.update_layout(
        title_text='Análisis Comparativo',
        legend_title='Tasas de Interés Anuales',
        hovermode='x unified',
        width=1200,
        height=600
    )
    fig.update_xaxes(title_text='Cantidad Financiada (€)', row=1, col=1)
    fig.update_yaxes(title_text='Cuota Mensual (€)', row=1, col=1)
    fig.update_xaxes(title_text='Cantidad Financiada (€)', row=1, col=2)
    fig.update_yaxes(title_text='Total a Pagar (€)', row=1, col=2)
    fig.show()


def plot_house_costs_vs_amount(houses, amounts, plot_type='both'):
    """
    Genera gráficos de costos totales mensuales y totales a pagar para casas.

    :param houses: Lista de instancias de House.
    :param amounts: Lista de cantidades financiadas (€).
    :param plot_type: Tipo de gráfico a generar ('monthly', 'total', 'both').
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Costo Total Mensual", "Total a Pagar"))

    for idx, house in enumerate(houses):
        # Costo Total Mensual
        total_monthly = house.total_monthly_cost()
        payments = [total_monthly * (amount / house.mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=payments,
            mode='lines',
            name=f'{house.mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Costo Total Mensual: %{y:.2f} €<extra></extra>'
        ), row=1, col=1)

        # Total a Pagar (Incluye hipoteca y otros costos)
        total_payment = house.mortgage.calculate_total_payment() + (
            house.property_tax + house.home_insurance + house.maintenance_cost +
            (house.community_fees + house.utilities) * 12
        )
        totals = [total_payment * (amount / house.mortgage.capital) for amount in amounts]
        fig.add_trace(go.Scatter(
            x=amounts,
            y=totals,
            mode='lines',
            name=f'{house.mortgage.interest_rate}% TIN',
            hovertemplate='Cantidad: %{x:.2f} €<br>Total a Pagar: %{y:.2f} €<extra></extra>'
        ), row=1, col=2)

    fig.update_layout(
        title_text='Análisis Comparativo de Casas',
        legend_title='Tasas de Interés Anuales',
        hovermode='x unified',
        width=1200,
        height=600
    )
    fig.update_xaxes(title_text='Cantidad Financiada (€)', row=1, col=1)
    fig.update_yaxes(title_text='Costo Total Mensual (€)', row=1, col=1)
    fig.update_xaxes(title_text='Cantidad Financiada (€)', row=1, col=2)
    fig.update_yaxes(title_text='Total a Pagar (€)', row=1, col=2)
    fig.show()
