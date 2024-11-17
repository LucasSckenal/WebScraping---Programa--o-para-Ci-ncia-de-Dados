from GameScraping import GachaRevenueScraper
from db import DB_CONFIG, PostgreSQLDatabase
from Graficos import ChartGenerator

# URL da página
url = "https://www.gacharevenue.com/revenue"

try:
    # Criação do scraper e extração de dados
    print("Iniciando o scraper...")
    data = None
    try:
        scraper = GachaRevenueScraper(url)
        scraper.fetch_data()
        data = scraper.get_data()

        if data.empty:
            raise ValueError("Nenhum dado foi extraído do site.")
        print(f"Dados extraídos: {data.shape}")  # Exibe linhas e colunas
    except Exception as e:
        print(f"Erro ao acessar o site ou raspar dados: {e}")
        print("Acessando dados diretamente do banco de dados...")

    # Conexão ao banco de dados
    print("Conectando ao banco de dados...")
    db = PostgreSQLDatabase(DB_CONFIG)
    db.connect()

    # Criar a tabela caso não exista
    print("Verificando a criação da tabela no banco de dados...")
    db.create_table('gacha_revenue') 

    # Inserir ou atualizar os dados na tabela
    if data is not None and not data.empty:
        print("Inserindo ou atualizando dados no banco de dados...")
        db.insert_or_update_data('gacha_revenue', data)

    # Se os dados não foram extraídos via scraper, recupera diretamente do banco
    if data is None or data.empty:
        print("Recuperando dados do banco de dados...")
        data = db.fetch_data('gacha_revenue')

        if data.empty:
            raise ValueError("Nenhum dado disponível no banco de dados.")
        print(f"Dados recuperados do banco: {data.shape}")

    # Validar colunas essenciais
    required_columns = ['region', 'game', 'current_month', 'previous_month']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

    # Geração dos gráficos
    print("Gerando gráficos...")
    chart_generator = ChartGenerator(data)
    chart_generator.generate_all_charts()

except Exception as e:
    print(f"Erro: {e}")

finally:
    print("Finalizando operações...")
    if 'db' in locals() and db.conn:
        db.close_connection()
    if 'scraper' in locals() and scraper.driver:
        scraper.close_driver()
