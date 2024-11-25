import dash
from dash import dcc, html
import dash_bootstrap_components as dbc  # Importar Bootstrap Components

# Inicializar o app com o tema escuro do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])  # Tema escuro

def init_dashboard(charts):
    app.layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("Game Revenue Dashboard", className="text-center"),
                    style={'color': 'white'}  # Título em branco
                ),
                className="mb-4"
            ),
            *[
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(
                            figure=chart,
                            config={"displayModeBar": False},
                            style={
                                'backgroundColor': '#2d2d2d',  # Fundo escuro para gráficos
                                'color': 'white',  # Texto branco dentro do gráfico
                                'border': '1px solid #444444',  # Borda escura
                                'padding': '10px'  # Padding para os gráficos
                            }
                        ),
                        style={'marginBottom': '20px'}
                    ),
                    className="mb-4"
                )
                for chart in charts.values()
            ]
        ],
        fluid=True,  # Tornar o layout responsivo
        style={
            'backgroundColor': '#121212',  # Fundo escuro para o layout
            'color': 'white',  # Texto branco para o layout
            'padding': '20px'  # Padding geral
        }
    )


