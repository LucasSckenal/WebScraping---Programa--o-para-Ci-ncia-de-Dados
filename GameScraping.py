from selenium import webdriver
import pandas as pd
from prettytable import PrettyTable
from CleaningData import DataCleaner  
class GachaRevenueScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.table_data = None

    # Inicia o driver do Selenium
    def start_driver(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    # Extrai os dados da tabela da página
    def extract_table(self):
        
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

        
        self.table_data.rename(columns={
            'Sep 2024': 'Last Month',
            'Oct 2024': 'Current Month'
        }, inplace=True)

    # Inicia o processo de coleta de dados e limpeza
    def fetch_data(self):
        self.start_driver()
        self.extract_table()

        cleaner = DataCleaner(self.table_data)
        self.table_data = cleaner.clean_data()  
        self.display_table()

    
    def get_data(self):
        return self.table_data

    # Exibe a tabela de maneira estilizada com PrettyTable."""
    def display_table(self):
        pretty_table = PrettyTable()
        pretty_table.field_names = self.table_data.columns

        for row in self.table_data.itertuples(index=False):
            pretty_table.add_row(row)

        print(pretty_table)

    # Fecha o driver do Selenium
    def close_driver(self):
        self.driver.quit()
