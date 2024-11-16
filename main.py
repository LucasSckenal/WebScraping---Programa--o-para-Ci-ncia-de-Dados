from GameScraping import GachaRevenueScraper
from db import DB_CONFIG, PostgreSQLDatabase
from Graficos import ChartGenerator

# URL da página
url = "https://www.gacharevenue.com/revenue"

try:
    # Etapa 1: Criação do scraper e extração de dados
    print("Iniciando o scraper...")
    scraper = GachaRevenueScraper(url)
    scraper.fetch_data()
    data = scraper.get_data()

    # Verifica se os dados foram extraídos corretamente
    if data.empty:
        raise ValueError("Nenhum dado foi extraído do site.")

    # Etapa 2: Conexão ao banco de dados e inserção de dados
    print("Conectando ao banco de dados...")
    db = PostgreSQLDatabase(DB_CONFIG)
    db.connect()
    db.create_table('gacha_revenue')  # Certifique-se de que a tabela tem a estrutura esperada

    # Use o método correto para inserção ou atualização
    db.insert_or_update_data('gacha_revenue', data)

    # Etapa 3: Recuperação de dados e geração de gráficos
    print("Recuperando dados e gerando gráficos...")
    db_data = db.fetch_data('gacha_revenue')  # Agora, esse método deve retornar um DataFrame
    chart_generator = ChartGenerator(db_data)
    chart_generator.generate_bar_chart()

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Garantir o fechamento das conexões, mesmo em caso de erro
    print("Finalizando operações...")
    if 'db' in locals():
        db.close_connection()
    if 'scraper' in locals():
        scraper.close_driver()
