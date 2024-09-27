# Gold Diggers

## Purpose

The Gold Diggers repository is a tool for analyzing investment data, including interest rates, gold prices, and other financial metrics. It provides scripts and notebooks to help users gather, process, and visualize financial data for better investment decision-making.

## Usage

### Scripts

1. **download.py**: This script contains functions to download financial data from Yahoo Finance.
   - Example usage:
     ```python
     from pygold.download import descargar_datos_yahoo
     data = descargar_datos_yahoo('AAPL', '2020-01-01', '2021-01-01')
     print(data.head())
     ```

2. **tasa_rendimiento.py**: This script contains functions to calculate the rate of return on investments.
   - Example usage:
     ```python
     from pygold.tasa_rendimiento import calcular_tasa_rendimiento
     tasa = calcular_tasa_rendimiento(1000, 5, 1500)
     print(tasa)
     ```

3. **graphs.py**: This script contains functions to configure and create graphs for visualizing financial data.
   - Example usage:
     ```python
     from pygold.graphs import configurar_grafica
     configurar_grafica()
     ```

### Notebooks

1. **get_interest_ratio.ipynb**: This notebook demonstrates how to obtain and analyze interest rate data using the Eurostat API.
2. **trading_algo_gold.ipynb**: This notebook contains a trading algorithm for gold prices.

## Installation

To set up the environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/LuisTellezSirocco/gold-diggers.git
   cd gold-diggers
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Future Developments

The following enhancements are planned for future releases:

1. Adding more financial metrics for analysis.
2. Improving data visualization capabilities.
3. Integrating additional data sources for more comprehensive analysis.
4. Developing more advanced trading algorithms.
5. Enhancing the user interface for easier interaction with the tools.
