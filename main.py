from selenium import webdriver
import pandas as pd
from prettytable import PrettyTable

# Inicia o driver do Selenium (ajuste o caminho para o seu WebDriver)
driver = webdriver.Chrome()

# URL da página com a tabela
url = "https://www.gacharevenue.com/revenue"
driver.get(url)

# Aguardar a tabela carregar (pode precisar de ajustes dependendo da página)
driver.implicitly_wait(10)

# Encontrando a tabela na página
table = driver.find_element("tag name", "table")

# Extraindo cabeçalhos da tabela
headers = [header.text for header in table.find_elements("tag name", "th")]

# Verificar e corrigir cabeçalhos duplicados
unique_headers = []
for i, header in enumerate(headers):
    if header in unique_headers:
        # Criar um novo nome único para o cabeçalho duplicado
        headers[i] = f"{header}_{i}"
    unique_headers.append(headers[i])

# Extraindo dados da tabela
rows = []
for row in table.find_elements("tag name", "tr")[1:]:  # Ignora o cabeçalho
    cells = [cell.text.strip() for cell in row.find_elements("tag name", "td")]
    if cells:
        rows.append(cells)

# Criando DataFrame
df = pd.DataFrame(rows, columns=headers)

# Usando PrettyTable para exibir a tabela de maneira estilizada
pretty_table = PrettyTable()

# Adicionando os cabeçalhos
pretty_table.field_names = df.columns

# Adicionando as linhas
for row in df.itertuples(index=False):
    pretty_table.add_row(row)

# Exibindo a tabela formatada
print(pretty_table)

# Fechar o driver
driver.quit()
