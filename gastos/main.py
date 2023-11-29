import pandas as pd
import numpy as np
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import logging
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

logging.basicConfig(level=logging.DEBUG)


# Function to get exchange rates from the API
def get_exchange_rate(from_currency="USD", to_currency="PEN"):
    key = "0c00579d0429fa2941633032280cfda245e31825"
    url = "https://api.getgeoapi.com/v2/currency/convert"
    parameters = {"api_key": key, "from": from_currency, "to": to_currency, "amount": 10, "format": "json"}
    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data.get('rates', {}).get(to_currency, {}).get('rate')

        if exchange_rate is not None:
            return float(exchange_rate)
        else:
            return None
    else:
        return None


usd_to_pen_rate = get_exchange_rate()
pen_to_usd_rate = get_exchange_rate("PEN", "USD")

# Sample data for fixed expenses (replace this with your actual data)
data = {
    "Gastos fijo Mensual": ["Experiam (Central de Riesgo)", "Alquiler de Local Industrial y Administrativo",
                            "Utiles de Aseo Personal Administ y Almacen", "Gastos de Representación_Ventas",
                            "Combustible Despachos _Ventas", "Movilidades Personal", "Telefonos Fijo",
                            "Lineas y equipos Moviles", "Utiles de Oficina Admint, Ventas y Almacen",
                            "Seguros, Vida, Familiar", "Mantenimiento de Sistemas Starsoft",
                            "Fibra de Internet dedicada Empresarial", "Poliza Seguro Todo Riesgo_Camioneta BMW"],
    "Amount (S/)": [200.80, 1020.00, 540.00, 1000.00, 3500.00, 2000.00, 0.00, 1060.00, 800.00, 2580.00, 0.00, 2578.88,
                    0.00],
    "Monto Fijo Mensual ($)": ["#¡VALOR!"] * 13,
    "Enero": ["#¡VALOR!"] * 13,
    "Febrero": ["#¡VALOR!"] * 13,
    "Marzo": ["#¡VALOR!"] * 13,
    "Abril": ["#¡VALOR!"] * 13,
    "Mayo": ["#¡VALOR!"] * 13,
    "Junio": ["#¡VALOR!"] * 13,
    "Julio": ["#¡VALOR!"] * 13,
    "Agosto": ["#¡VALOR!"] * 13,
    "Setiembre": ["#¡VALOR!"] * 13,
    "Octubre": ["#¡VALOR!"] * 13,
    "Noviembre": ["#¡VALOR!"] * 13,
    "Diciembre": ["#¡VALOR!"] * 13,
    "TOTAL": ["#¡VALOR!"] * 13,
}

data1 = {
    "Gastos variables Mensual": [
        "Pago Energia Electrica Local Administrativo",
        "Planilla de Remuneraciones (Sueldos y RxH)",
        "Gastos de Peajes_PEX",
        "Gastos de Combustible_Despachos Vtas",
        "Costos y Gastos Financieros",
    ],
    "Expense Detail": ["SOLES"] * 5,
    "Enero": [740.00, 20875.14, 410.00, 45000.00, "#¡VALOR!"],
    "Febrero": [350.00, 1496.54, 210.00, 45000.00, "#¡VALOR!"],
    "Marzo": [501.00, 3258.54, 894.00, 45000.00, "#¡VALOR!"],
    "Abril": [963.00, 235725.50, 363.00, 45000.00, "#¡VALOR!"],
    "Mayo": [241.00, 145.18, 478.00, 45000.00, "#¡VALOR!"],
    "Junio": [365.00, 34.89, 321.00, 45000.00, "#¡VALOR!"],
    "Julio": [742.00, 7453217.00, 498.00, 45000.00, "#¡VALOR!"],
    "Agosto": [231.00, 2268.31, 320.00, 45000.00, "#¡VALOR!"],
    "Setiembre": [765.00, 15842.00, 789.00, 45000.00, "#¡VALOR!"],
    "Octubre": ["#¡VALOR!"] * 5,
    "Noviembre": ["#¡VALOR!"] * 5,
    "Diciembre": ["#¡VALOR!"] * 5,
}

df = pd.DataFrame(data)
df1 = pd.DataFrame(data1)

# Check column names
print(df1.columns)
for month in df1.columns[2:]:
    df1[month + "_DOLARES"] = df1[month].apply(
        lambda x: x / pen_to_usd_rate if pd.notna(x) and isinstance(x, (int, float)) else x)

# Convert Amount (S/) to Dollars using exchange rate and handle NaN
if usd_to_pen_rate:
    df["Monto Fijo Mensual ($)"] = df["Amount (S/)"] / usd_to_pen_rate
    # Handle NaN values in the "Monto Fijo Mensual ($)" column
    df["Monto Fijo Mensual ($)"].fillna("#¡VALOR!", inplace=True)
    for month in df.columns[3:15]:
        df[month] = df["Monto Fijo Mensual ($)"].apply(lambda x: x if pd.notna(x) and not np.isnan(x) else 0.0)

# Calculate the TOTAL column by summing values from Enero to Diciembre
df["TOTAL"] = df[df.columns[3:15]].sum(axis=1)

# Check if the column 'Gastos variables Mensual' is in the DataFrame
if 'Gastos variables Mensual' in df1.columns:
    # Your code here, e.g., filtering or using the column
    print(df1['Gastos variables Mensual'])
else:
    print("Column 'Gastos variables Mensual' not found in the DataFrame.")

# Replace placeholder values with NaN in both DataFrames
df.replace('#¡VALOR!', np.nan, inplace=True)
df1.replace('#¡VALOR!', np.nan, inplace=True)

# Fetch exchange rate
usd_to_pen_rate = get_exchange_rate()
pen_to_usd_rate = get_exchange_rate("PEN", "USD")

# Convertir de Soles a dólares
for month in df1.columns[2:]:
    df1[f"{month}_DOLARES"] = df1[month].apply(
        lambda x: x / pen_to_usd_rate if pd.notna(x) and isinstance(x, (int, float)) else x)

# Convert Amount (S/) to Dollars using exchange rate and handle NaN
if usd_to_pen_rate:
    df["Monto Fijo Mensual ($)"] = df["Amount (S/)"] / usd_to_pen_rate
    # Handle NaN values in the "Monto Fijo Mensual ($)" column
    df["Monto Fijo Mensual ($)"].fillna("#¡VALOR!", inplace=True)
    for month in df.columns[3:15]:
        df[f"{month}_DOLARES"] = df["Monto Fijo Mensual ($)"].apply(
            lambda x: x if pd.notna(x) and not np.isnan(x) else 0.0)
# Calculate the TOTAL column by summing values from Enero to Diciembre
df["TOTAL"] = df[df.columns[3:15]].sum(axis=1)

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'backgroundColor': '#1f2536'},
    children=[
        html.H1("Finance Table", style={'color': 'white'}),
        html.Div([
            html.H2("Gastos Fijos Mensuales", style={'color': 'white'}),
            html.P("GASTOS FIJOS MONETARIO", style={'color': 'white'}),
            html.Div([
                dash_table.DataTable(
                    id='gastos-fijos-table',
                    columns=[
                        {'name': col, 'id': col} for col in df.columns
                    ],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'auto', 'margin-bottom': '20px'},
                    style_cell={"backgroundColor": "#242a3b", "color": "#d0ef84"},
                    style_header={"backgroundColor": "#1f2536", "padding": "0px 5px", 'color': 'white'}
                ),
            ],
                style={'overflowX': 'auto', 'margin-bottom': '20px'}),
        ]),

        html.Div([
            html.Label("Month", style={'color': 'white'}),
            dcc.Dropdown(id='month-dropdown',
                         options=[{'label': html.Span(month), 'value': month} for month in df1.columns[2:]],
                         value=df1.columns[2], style={'width': '50%', 'color': '#000000'}),
            html.Label("Gastos Variables", style={'color': 'white'}),
            dcc.Dropdown(
                id='gastos-variable-dropdown',
                options=[{'label': html.Span(gasto), 'value': gasto} for gasto in
                         df1['Gastos variables Mensual'].unique()],
                value=df1['Gastos variables Mensual'].iloc[0],
                style={'width': '50%', 'color': '#000000'},
                className='dropdown-style'
                # Set option height for better visibility
            ),
            html.P("GASTOS VARIABLES MONETARIO", style={'color': 'white'}),
            dash_table.DataTable(
                id='gastos-variables-table',
                columns=[{'name': col, 'id': col} for col in df1.columns[:2]] +
                        [{'name': f'{col}', 'id': f'{col}', 'editable': True} for col in df1.columns[2:14]] +
                        [{'name': f'{col}_DOLARES', 'id': f'{col}_DOLARES', 'editable': True} for col in
                         df1.columns[2:14] if
                         col not in ['Enero_DOLARES_DOLARES', 'Febrero_DOLARES_DOLARES', 'Marzo_DOLARES_DOLARES',
                                     'Abril_DOLARES_DOLARES', 'Mayo_DOLARES_DOLARES', 'Junio_DOLARES_DOLARES',
                                     'Julio_DOLARES_DOLARES', 'Agosto_DOLARES_DOLARES', 'Setiembre_DOLARES_DOLARES',
                                     'Octubre_DOLARES_DOLARES', 'Noviembre_DOLARES_DOLARES',
                                     'Diciembre_DOLARES_DOLARES']],
                data=df1.to_dict('records'),
                editable=True,
                style_table={'overflowX': 'auto', 'margin-bottom': '20px'},
                style_cell={"backgroundColor": "#1f2536", "color": "#d0ef84"},
                style_header={"background-color": "#1f2536", "padding": "0px 5px", 'color': 'white'}
            ),
        ]),
        html.Div([
            dcc.Graph(
                id='expenses-plotly-express-bar-chart',
                figure={},
            )
        ])
    ]
)


@app.callback(
    Output('expenses-plotly-express-bar-chart', 'figure'),
    [Input('month-dropdown', 'value'), Input('gastos-variable-dropdown', 'value')],
)
def update_bar_chart(selected_month, selected_gasto):
    filtered_df1 = df1[(df1['Gastos variables Mensual'] == selected_gasto)]

    # Melt the DataFrame for Plotly Express bar chart
    df1_melted = pd.melt(filtered_df1, id_vars=["Gastos variables Mensual", "Expense Detail"], var_name="Month",
                         value_name="Amount")

    # Convert the Amount column to dollars using the exchange rate
    usd_to_pen_rate = get_exchange_rate()
    df1_melted["Amount_DOLARES"] = df1_melted["Amount"] / usd_to_pen_rate

    # Filter the melted DataFrame for the selected month
    filtered_df1_melted = df1_melted[df1_melted['Month'] == selected_month]

    y_axis_range = [0, filtered_df1_melted["Amount"].max()]
    # Create the Plotly Express bar chart
    fig = px.bar(
        filtered_df1_melted,
        x="Expense Detail",
        y=["Amount", "Amount_DOLARES"],
        color="Gastos variables Mensual",
        barmode="group",
        labels={"Amount": "Amount (Soles)", "Amount_DOLARES": "Amount (USD)"},
        height=400,
        width=800,
        text_auto=True,
        pattern_shape="Gastos variables Mensual",
        pattern_shape_sequence=["+"],  # Change "X" to [0]
        range_color=y_axis_range,
    )
    fig.update_traces(
        marker_color='#6892d5',
        marker_line_color='rgb(8,48,147)',
        marker_line_width=1.5,
        opacity=0.8,
        textfont_color='#cbf078',
        textfont=dict(size=18),
    )
    fig.update_layout(
        title=f'Plotly Express Bar Chart for {selected_month} - {selected_gasto}',
        xaxis_title="Expense Detail",
        yaxis_title="Amount",
        barmode="group",
        margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},  # Adjust margins as needed
        plot_bgcolor="#1f2536",  # Background color of the plot area
        paper_bgcolor="#1f2536",  # Background color of the entire chart
        title_font=dict(color="white"),
        legend=dict(title=dict(text="Gastos variables Mensual", font=dict(color="white"))),
        xaxis=dict(title=dict(font=dict(color="white")),
                   tickfont=dict(color="white")),

        yaxis=dict(title=dict(font=dict(color="white")),
                   tickfont=dict(color="white")),
    ),

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)