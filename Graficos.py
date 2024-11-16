import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from CleaningData import DataCleaner  

class ChartGenerator:
    def __init__(self, data):
        self.data = data
        self.cleaner = DataCleaner(data)  

    # Valida se as colunas necessárias estão no DataFrame
    def validate_columns(self, required_columns):
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Coluna obrigatória '{col}' não encontrada no DataFrame.")

    # função de limpeza
    def clean_data_graph(self):
        self.data = self.cleaner.clean_data_graph()  

    # Formata os números para adicionar sufixos como k, M, B
    def format_large_numbers(self, value, tick_pos):
        if value >= 1_000_000_000:
            return f'{value/1_000_000_000:.1f}B'
        elif value >= 1_000_000:
            return f'{value/1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value/1_000:.1f}K'
        else:
            return str(value)

    # Gera um gráfico de barras com os dados de receita
    def revenue_graph(self):
        try:
            self.validate_columns(['game', 'current_month'])
            self.clean_data_graph()  
            self.data = self.data.sort_values('current_month', ascending=True)

            plt.figure(figsize=(10, 6))
            sns.barplot(x='game', y='current_month', data=self.data, palette='Purples')
            plt.xlabel('Game')
            plt.ylabel('Revenue in Current Month (in $)')
            plt.xticks(rotation=90)
            plt.title('Lucros dos Gachas')

            plt.gca().yaxis.set_major_formatter(FuncFormatter(self.format_large_numbers))

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico de barras: {e}")

    # Gera um gráfico de pizza para mostrar a distribuição de servidores
    def servers_graphs(self):
        try:
            self.validate_columns(['region'])
            self.clean_data_graph()  

            region_counts = self.data['region'].value_counts()

            plt.figure(figsize=(10, 10))

            wedges, texts, autotexts = plt.pie(region_counts, 
                                                labels=region_counts.index, 
                                                autopct='%1.1f%%', 
                                                startangle=90, 
                                                colors=sns.color_palette('RdYlGn', n_colors=len(region_counts)))

            legend_labels = [f'{label} ({autotext.get_text()})' for label, autotext in zip(region_counts.index, autotexts)]
            
            plt.legend(wedges, legend_labels, title="Regions", loc="upper left", bbox_to_anchor=(1, 1))
            plt.title('Distribuição dos jogos por região de servidor')
            plt.tight_layout() 
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico de pizza: {e}")

   
    # Gera um gráfico de dispersão comparando os lucros do mês anterior e do mês atual
    def compartion_revenue_graph(self):
        try:
            self.validate_columns(['game', 'current_month', 'previous_month'])
            self.clean_data_graph()  

            total_revenue_current = self.data['current_month'].sum()
            total_revenue_previous = self.data['previous_month'].sum()

            months = ['Previous Month', 'Current Month']
            revenues = [total_revenue_previous, total_revenue_current]

            plt.figure(figsize=(10, 6))

            # Gráfico de barras laterais (horizontal)
            sns.barplot(x=revenues, y=months, palette=['lightcoral', 'lightgreen'])

            plt.xlabel('Total Revenue ($)')
            plt.ylabel('Month')
            plt.title('Comparacao de lucro entre os meses')

            plt.gca().xaxis.set_major_formatter(FuncFormatter(self.format_large_numbers))

            plt.tight_layout()

            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico comparativo: {e}")

    # Gera um gráfico de linha comparando as receitas do mês anterior e do mês atual
    def lineGraph_allGames(self):
        try:
            self.validate_columns(['game', 'current_month', 'previous_month'])
            self.clean_data_graph()  

            comparison_data = self.data[['game', 'current_month', 'previous_month']].set_index('game')
            comparison_data = comparison_data.reset_index()

            plt.figure(figsize=(10, 6))
            sns.lineplot(x='game', y='current_month', data=comparison_data, label='Current Month', marker='o', color='#F00')
            sns.lineplot(x='game', y='previous_month', data=comparison_data, label='Previous Month', marker='o', color='#0FF')

            plt.xlabel('Game')
            plt.ylabel('Revenue in $')
            plt.title('Comparacao dos lucros de todos os gachas entre o mes atual')
            plt.xticks(rotation=90)
            plt.legend()

            plt.gca().yaxis.set_major_formatter(FuncFormatter(self.format_large_numbers))

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Erro ao gerar gráfico de linha: {e}")

    # gráfico de dispersão por Servidor
    def scatter_plot_by_server(self):
        try:
            self.validate_columns(['region', 'current_month'])
            self.clean_data_graph()

            comparison_data = self.data[['region', 'current_month']].groupby('region').sum().reset_index()

            plt.figure(figsize=(10, 6))

            colors = sns.color_palette('Set2', n_colors=len(comparison_data))

            for i, region in enumerate(comparison_data['region']):
                plt.scatter(
                    x=[region], 
                    y=comparison_data.loc[i, 'current_month'], 
                    color=colors[i], 
                    edgecolor='black', 
                    s=200, 
                    label=region
                )

            plt.xlabel('Region')
            plt.ylabel('Total Revenue ($)')
            plt.title('lucro de cada servidor')
            plt.gca().yaxis.set_major_formatter(FuncFormatter(self.format_large_numbers))
            plt.xticks(rotation=45)
            plt.legend(title='Regions')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico de dispersão por servidor: {e}")

    
    # Gráfico de pizza para Comparação de Lucros por Servidor
    def pie_chart_revenue(self):
        try:
            self.validate_columns(['region', 'current_month', 'previous_month'])
            self.clean_data_graph()

            region_data = self.data.groupby('region')[['current_month', 'previous_month']].sum()

            total_revenue = region_data.sum(axis=1)

            colors = plt.cm.Paired(range(len(region_data)))

            plt.figure(figsize=(8, 8))
            wedges, texts, autotexts = plt.pie(
                total_revenue, 
                labels=region_data.index, 
                autopct='%1.1f%%', 
                colors=colors, 
                startangle=90,  
                wedgeprops={'edgecolor': 'black', 'linewidth': 1},  
            )

            legend_labels = [f'{label} ({autotext.get_text()})' for label, autotext in zip(region_data.index, autotexts)]

            plt.legend(
                wedges, 
                legend_labels, 
                title="Region", 
                loc="upper left", 
                bbox_to_anchor=(1, 1)
            )

            plt.title('Comparação de Lucros por Servidor')
            plt.axis('equal')  
            plt.tight_layout()  
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico de pizza: {e}")


    def generate_all_charts(self):
        self.clean_data_graph()
        self.revenue_graph() 
        self.servers_graphs()
        self.compartion_revenue_graph() 
        self.lineGraph_allGames() 
        self.scatter_plot_by_server()
        self.pie_chart_revenue()
        print("Gráficos gerados com sucesso!")
