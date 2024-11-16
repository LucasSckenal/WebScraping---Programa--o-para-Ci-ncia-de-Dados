import matplotlib.pyplot as plt

class ChartGenerator:
    def __init__(self, data):
        self.data = data

    def validate_columns(self, required_columns):
        """Valida se as colunas necessárias estão no DataFrame."""
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Coluna obrigatória '{col}' não encontrada no DataFrame.")

    def clean_data(self):
        """Limpa os dados para garantir que não haja problemas ao gerar os gráficos."""
        # Verifique se as colunas estão nomeadas corretamente
        print(self.data.columns)

        # Renomeie as colunas caso necessário
        self.data.columns = ['id', 'region', 'game', 'current_month', 'previous_month']

        # Remover quebras de linha e espaços extras nas colunas 'game' e 'region'
        self.data['game'] = self.data['game'].str.replace('\n', ' ', regex=True).str.strip()
        self.data['region'] = self.data['region'].str.strip()

        # Limpeza de valores nas colunas de receita
        for col in ['current_month', 'previous_month']:
            if self.data[col].dtype == 'object':
                self.data[col] = self.data[col].apply(lambda x: str(x).replace('$', '').replace(',', '') if isinstance(x, str) else x)
                self.data[col] = self.data[col].astype(float)
    def generate_bar_chart(self):
        """Gera um gráfico de barras com os dados de receita."""
        try:
            self.validate_columns(['game', 'current_month'])
            self.clean_data()  # Limpeza dos dados antes de gerar o gráfico

            plt.figure(figsize=(10, 6))
            plt.bar(self.data['game'], self.data['current_month'])
            plt.xlabel('game')
            plt.ylabel('Revenue in Current Month (in $)')
            plt.xticks(rotation=90)
            plt.title('Gacha Revenue - Current Month')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico de barras: {e}")

    def generate_pie_chart(self):
        """Gera um gráfico de pizza para mostrar a distribuição de servidores."""
        try:
            self.validate_columns(['region'])
            self.clean_data()  # Limpeza dos dados antes de gerar o gráfico

            region_counts = self.data['region'].value_counts()

            plt.figure(figsize=(8, 8))
            plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('Distribution of games by Server region')
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico de pizza: {e}")

    def generate_top_10_games_avg(self):
        """Gera um gráfico mostrando a média dos lucros dos 10 primeiros jogos."""
        try:
            self.validate_columns(['game', 'current_month'])
            self.clean_data()  # Limpeza dos dados antes de gerar o gráfico

            top_10_games = self.data.nlargest(10, 'current_month')
            avg_revenue = top_10_games['current_month'].mean()

            plt.figure(figsize=(10, 6))
            plt.bar(top_10_games['game'], top_10_games['current_month'])
            plt.axhline(y=avg_revenue, color='r', linestyle='--', label=f'Average: ${avg_revenue:,.2f}')
            plt.xlabel('game')
            plt.ylabel('Revenue in Current Month (in $)')
            plt.xticks(rotation=90)
            plt.title('Top 10 Gacha games by Revenue (Current Month) with Average Line')
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico dos 10 melhores jogos: {e}")

    def generate_comparison_chart(self):
        """Gera um gráfico comparando os lucros do mês anterior e do mês atual."""
        try:
            self.validate_columns(['game', 'current_month', 'previous_month'])
            self.clean_data()  # Limpeza dos dados antes de gerar o gráfico

            comparison_data = self.data[['game', 'current_month', 'previous_month']].set_index('game')
            comparison_data.plot(kind='bar', figsize=(10, 6))
            plt.xlabel('game')
            plt.ylabel('Revenue in $')
            plt.title('Comparison of Gacha Revenue (Current Month vs Previous Month)')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico comparativo: {e}")

    def generate_total_revenue_chart(self):
        """Gera um gráfico mostrando o total de dinheiro dos meses atual e anterior."""
        try:
            self.validate_columns(['current_month', 'previous_month'])
            self.clean_data()  # Limpeza dos dados antes de gerar o gráfico

            total_revenue = {
                'Current Month': self.data['current_month'].sum(),
                'Previous Month': self.data['previous_month'].sum()
            }
            months = list(total_revenue.keys())
            revenues = list(total_revenue.values())

            plt.figure(figsize=(8, 6))
            plt.bar(months, revenues, color=['blue', 'orange'])
            plt.xlabel('Month')
            plt.ylabel('Total Revenue in $')
            plt.title('Total Revenue for Current and Previous Month')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico de receita total: {e}")
