import pandas as pd

class DataCleaner:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def clean_data(self) -> pd.DataFrame:
        # Limpeza para dados do banco de dados
        print("Colunas no DataFrame (Banco de Dados):", self.data.columns)

        # Substituição de símbolos por strings em todo o DataFrame
        self.data.replace({'🇯🇵': "jp", '🇨🇳': "cn", '🇰🇷': "kr", '🇺🇸': "us", '☠️': 0, '🌐': 'WW'}, inplace=True)

        # Renomeia as colunas para garantir que 'Last Month' e 'Current Month' sejam reconhecidas
        self.data.columns = self.data.columns.str.strip()  # Remove espaços extras
        self.data.rename(columns={'Last Month': 'previous_month', 'Current Month': 'current_month'}, inplace=True)

        # Limpeza dos dados, removendo símbolos de moeda e convertendo para numérico
        if self.data['previous_month'].dtype == 'object':
            self.data['previous_month'] = self.data['previous_month'].replace({r'\$': '', r',': ''}, regex=True).apply(pd.to_numeric, errors='coerce')

        # Substitui valores ausentes ou "new" por 0 em 'previous_month'
        self.data['previous_month'] = self.data['previous_month'].fillna(0)

        if self.data['current_month'].dtype == 'object':
            self.data['current_month'] = self.data['current_month'].replace({r'\$': '', r',': ''}, regex=True).apply(pd.to_numeric, errors='coerce')

        # Remover todas as colunas antes de 'Region'
        region_index = self.data.columns.get_loc('Region')
        self.data = self.data.iloc[:, region_index:]

        print(f"Colunas após renomeação (Banco de Dados): {self.data.columns}")
        return self.data

    def clean_data_graph(self) -> pd.DataFrame:
        # Limpeza para gráficos
        print("Colunas no DataFrame (Gráficos):", self.data.columns)

        # Limpeza específica para gráficos (remove quebras de linha, espaços extras, etc.)
        self.data['game'] = self.data['game'].str.replace('\n', ' ', regex=True).str.strip()
        self.data['region'] = self.data['region'].str.strip()

        print(f"Colunas após renomeação (Gráficos): {self.data.columns}")
        return self.data