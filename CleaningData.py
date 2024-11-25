import pandas as pd

class DataCleaner:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def clean_numeric_column(self, column: pd.Series) -> pd.Series:
        """Limpa e converte valores monetários em uma coluna para numérico."""
        if column.dtype == 'object':
            # Remove símbolos de moeda e vírgulas, depois converte para numérico
            column = column.replace({r'\$': '', r',': ''}, regex=True).apply(pd.to_numeric, errors='coerce')
        # Preenche NaNs com 0 (ou use outra estratégia, se necessário)
        return column.fillna(0)

    def clean_data(self) -> pd.DataFrame:
        # Valida colunas essenciais
        expected_columns = ['Region', 'Game', 'Last Month', 'Current Month']
        missing_columns = [col for col in expected_columns if col not in self.data.columns]

        if missing_columns:
            raise ValueError(f"Colunas ausentes no DataFrame: {missing_columns}")

        # Substitui símbolos por strings
        self.data.replace({
            '🇯🇵': "jp", '🇨🇳': "cn", '🇰🇷': "kr", '🇺🇸': "us", '☠️': 0, '🌐': 'WW'
        }, inplace=True)

        # Renomeia colunas para consistência
        self.data.rename(columns={
            'Last Month': 'previous_month',
            'Current Month': 'current_month',
            'Region': 'region',
            'Game': 'game'
        }, inplace=True)

        # Limpa e converte colunas numéricas
        self.data['previous_month'] = self.clean_numeric_column(self.data['previous_month'])
        self.data['current_month'] = self.clean_numeric_column(self.data['current_month'])

        # Remove colunas antes da 'region'
        if 'region' in self.data.columns:
            region_index = self.data.columns.get_loc('region')
            self.data = self.data.iloc[:, region_index:]
        else:
            raise ValueError("Coluna 'region' não encontrada no DataFrame.")

        # Imprime os nomes das colunas após a limpeza
        print(f"Colunas após a limpeza (Banco de Dados): {self.data.columns}")
        return self.data

    def clean_data_graph(self) -> pd.DataFrame:
        # Limpeza de dados textuais para melhor legibilidade nos gráficos
        print("Colunas no DataFrame (Gráficos):", self.data.columns)

        # Remove quebras de linha e elimina espaços extras do texto
        self.data['game'] = self.data['game'].str.replace('\n', ' ', regex=True).str.strip()
        self.data['region'] = self.data['region'].str.strip()

        # Imprime os nomes das colunas após a limpeza para os gráficos
        print(f"Colunas após a limpeza (Gráficos): {self.data.columns}")
        return self.data
