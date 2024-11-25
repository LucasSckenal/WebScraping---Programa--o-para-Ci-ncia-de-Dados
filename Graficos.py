import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from CleaningData import DataCleaner


class ChartGenerator:
    def __init__(self, data):
        self.data = data
        self.cleaner = DataCleaner(data)

    # Validar colunas necessárias
    def validate_columns(self, *required_columns):
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Limpar dados usando o módulo de limpeza
    def clean_data_graph(self):
        self.data = self.cleaner.clean_data_graph()

    # Gráfico de barras de receita mensal com cores únicas por jogo
    def generate_monthly_revenue_bar_chart(self):
        try:
            self.validate_columns('game', 'current_month')
            self.clean_data_graph()

            self.data = self.data.dropna(subset=['game', 'current_month'])
            self.data = self.data.sort_values('current_month', ascending=True)

            fig = px.bar(
                self.data,
                x="game",
                y="current_month",
                title="Monthly Revenue by Game",
                labels={"current_month": "Revenue ($)", "game": "Game"},
                color="game",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                xaxis=dict(title="Game", tickangle=45),
                yaxis=dict(title="Revenue ($)", tickformat="$,.0f"),
                title=dict(x=0.5)  # Centraliza o título
            )
            return fig

        except Exception as e:
            print(f"Error generating monthly revenue bar chart: {e}")

    # Gráfico de pizza para distribuição por região de servidor
    def generate_server_distribution_pie_chart(self):
        try:
            self.validate_columns('region')
            self.clean_data_graph()

            region_counts = self.data['region'].value_counts().reset_index()
            region_counts.columns = ['region', 'count']

            fig = px.pie(
                region_counts,
                values="count",
                names="region",
                title="Server Distribution by Region",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textinfo='percent+label')
            return fig

        except Exception as e:
            print(f"Error generating server distribution pie chart: {e}")

    # Gráfico de barras comparando receita entre o mês atual e o anterior
    def generate_monthly_revenue_comparison_bar_chart(self):
        try:
            self.validate_columns('game', 'current_month', 'previous_month')
            self.clean_data_graph()

            total_revenue_current = self.data['current_month'].sum()
            total_revenue_previous = self.data['previous_month'].sum()

            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=['Previous Month', 'Current Month'],
                x=[total_revenue_previous, total_revenue_current],
                orientation='h',
                marker_color=['#FF7F7F', '#90EE90']
            ))
            fig.update_layout(
                title="Revenue Comparison Between Months",
                xaxis_title="Total Revenue ($)",
                yaxis_title="Month",
                xaxis=dict(tickformat="$,.0f"),
                title_x=0.5
            )
            return fig

        except Exception as e:
            print(f"Error generating monthly revenue comparison bar chart: {e}")

    # Heatmap comparando receitas de jogos
    def generate_revenue_heatmap(self):
        try:
            self.validate_columns('game', 'current_month', 'previous_month')
            self.clean_data_graph()

            heatmap_data = self.data[['game', 'current_month', 'previous_month']]
            heatmap_data = heatmap_data.melt(id_vars='game', var_name='month', value_name='revenue')

            fig = px.density_heatmap(
                heatmap_data,
                x='game',
                y='month',
                z='revenue',
                color_continuous_scale='Viridis',
                title="Heatmap: Revenue Comparison",
                labels={"game": "Game", "month": "Month", "revenue": "Revenue ($)"}
            )
            fig.update_layout(
                xaxis=dict(tickangle=45),
                yaxis=dict(title="Month"),
                title_x=0.5
            )
            return fig
        except Exception as e:
            print(f"Error generating revenue heatmap: {e}")

    # Gráfico de dispersão de receita por região de servidor
    # Gráfico de barras agrupadas para comparação de lucro por região e jogo
    def generate_grouped_bar_chart(self):
        try:
            # Validar as colunas necessárias
            self.validate_columns('game', 'region', 'current_month')
            self.clean_data_graph()

            # Agrupar os dados para facilitar o gráfico
            grouped_data = self.data.groupby(['game', 'region'])['current_month'].sum().reset_index()

            # Criar o gráfico de barras agrupadas
            fig = px.bar(
                grouped_data,
                x="game",
                y="current_month",
                color="region",
                title="Revenue Comparison by Game and Region",
                labels={"current_month": "Revenue ($)", "game": "Game", "region": "Region"},
                barmode="group",  # Define o agrupamento das barras
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            # Configurar o layout do gráfico
            fig.update_layout(
                xaxis=dict(title="Game", tickangle=45),
                yaxis=dict(title="Revenue ($)", tickformat="$,.0f"),
                title=dict(x=0.5)  # Centraliza o título
            )
            return fig

        except Exception as e:
            print(f"Error generating grouped bar chart: {e}")


    # Gráfico de pizza para distribuição de receita por servidor
    def generate_revenue_distribution_pie_chart(self):
        try:
            self.validate_columns('region', 'current_month', 'previous_month')
            self.clean_data_graph()

            region_data = self.data.groupby('region')[['current_month', 'previous_month']].sum().sum(axis=1).reset_index()
            region_data.columns = ['region', 'total_revenue']

            fig = px.pie(
                region_data,
                values='total_revenue',
                names='region',
                title="Revenue Distribution by Region",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textinfo='percent+label')
            return fig

        except Exception as e:
            print(f"Error generating revenue distribution pie chart: {e}")

    # Gerar todos os gráficos
    def generate_all_charts(self):
        try:
            self.clean_data_graph()
            charts = {
                "server_distribution_pie_chart": self.generate_server_distribution_pie_chart(),
                "revenue_distribution_pie_chart": self.generate_revenue_distribution_pie_chart(),
                "monthly_revenue_bar_chart": self.generate_monthly_revenue_bar_chart(),
                "monthly_revenue_comparison_bar_chart": self.generate_monthly_revenue_comparison_bar_chart(),
                "revenue_trend_line_chart": self.generate_revenue_heatmap(),
                "grouped_bar_chart": self.generate_grouped_bar_chart(),
            }
            print("All charts generated successfully!")
            return charts
        except Exception as e:
            print(f"Error generating all charts: {e}")
