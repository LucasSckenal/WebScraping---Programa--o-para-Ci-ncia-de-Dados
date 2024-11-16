from GameScraping import GachaRevenueScraper
from db import DB_CONFIG, PostgreSQLDatabase
from Graficos import ChartGenerator

# URL da página
url = "https://www.gacharevenue.com/revenue"

try:
    # Criação do scraper e extração de dados
    print("Iniciando o scraper...")
    try:
        scraper = GachaRevenueScraper(url)
        scraper.fetch_data()
        data = scraper.get_data()

        # Verifica se os dados foram extraídos corretamente
        if data.empty:
            raise ValueError("Nenhum dado foi extraído do site.")
    except Exception as e:
        print(f"Erro ao acessar o site ou raspar dados: {e}")
        print("Acessando dados diretamente do banco de dados...")

        # Se o scraper falhar, usa dados do banco
        data = None  

    #Conexão ao banco de dados
    print("Conectando ao banco de dados...")
    db = PostgreSQLDatabase(DB_CONFIG)
    db.connect()

    # Se os dados não foram extraídos via scraper, recupera diretamente do banco de dados
    if data is None or data.empty:
        print("Recuperando dados do banco de dados...")
        data = db.fetch_data('gacha_revenue') 

        if data.empty:
            raise ValueError("Nenhum dado disponível no banco de dados.")

    # Geração dos gráficos
    print("Gerando gráficos...")
    chart_generator = ChartGenerator(data)  
    chart_generator.generate_all_charts()

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Garantir o fechamento das conexões, mesmo em caso de erro
    print("Finalizando operações...")
    if 'db' in locals():
        db.close_connection()
    if 'scraper' in locals():
        scraper.close_driver()
