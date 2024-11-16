from selenium import webdriver
import pandas as pd
from prettytable import PrettyTable
from CleaningData import DataCleaner  # Importando a classe DataCleaner

class GachaRevenueScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.table_data = None

    def start_driver(self):
        """Inicia o driver do Selenium."""
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    def extract_table(self):
        """Extrai os dados da tabela da página."""
        table = self.driver.find_element("tag name", "table")
        headers = [header.text for header in table.find_elements("tag name", "th")]

        # Corrigir cabeçalhos duplicados
        unique_headers = []
        for i, header in enumerate(headers):
            if header in unique_headers:
                headers[i] = f"{header}_{i}"
            unique_headers.append(headers[i])

        rows = []
        for row in table.find_elements("tag name", "tr")[1:]:  # Ignora o cabeçalho
            cells = [cell.text.strip() for cell in row.find_elements("tag name", "td")]
            if cells:
                rows.append(cells)

        # Criando o DataFrame
        self.table_data = pd.DataFrame(rows, columns=headers)

        # Renomear as colunas de 'Sep 2024' e 'Oct 2024' para 'Last Month' e 'Current Month'
        self.table_data.rename(columns={
            'Sep 2024': 'Last Month',
            'Oct 2024': 'Current Month'
        }, inplace=True)

    def fetch_data(self):
        """Inicia o processo de coleta de dados e limpeza."""
        self.start_driver()
        self.extract_table()

        # Aplicando o DataCleaner após a coleta de dados
        cleaner = DataCleaner(self.table_data)
        self.table_data = cleaner.clean_data()  # Limpa os dados após a extração

        # Exibe a tabela limpa antes de adicionar ao banco
        self.display_table()

    def get_data(self):
        """Retorna os dados coletados e limpos em formato DataFrame."""
        return self.table_data

    def display_table(self):
        """Exibe a tabela de maneira estilizada com PrettyTable."""
        pretty_table = PrettyTable()
        pretty_table.field_names = self.table_data.columns

        for row in self.table_data.itertuples(index=False):
            pretty_table.add_row(row)

        print(pretty_table)

    def close_driver(self):
        """Fecha o driver do Selenium."""
        self.driver.quit()
