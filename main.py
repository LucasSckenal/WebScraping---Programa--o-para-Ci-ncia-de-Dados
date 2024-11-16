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
    db.create_table('gacha_revenue')  # Cria a tabela se ela não existir

    # Inserir ou atualizar os dados no banco
    db.insert_or_update_data('gacha_revenue', data)

    # Etapa 3: Recuperação de dados do banco de dados
    print("Recuperando dados do banco de dados...")
    db_data = db.fetch_data('gacha_revenue')  # Recupera os dados do banco e armazena em db_data

    # Agora db_data contém os dados que podem ser utilizados para gráficos

    # Etapa 4: Geração dos gráficos
    print("Gerando gráficos...")
    chart_generator = ChartGenerator(db_data)  # Passando o DataFrame recuperado
    chart_generator.generate_bar_chart()  # Gera o gráfico de barras
    chart_generator.generate_pie_chart()  # Gera o gráfico de pizza
    chart_generator.generate_top_10_games_avg()  # Gera o gráfico dos 10 melhores jogos
    chart_generator.generate_comparison_chart()  # Gera o gráfico comparativo
    chart_generator.generate_total_revenue_chart()  # Gera o gráfico de receita total

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Garantir o fechamento das conexões, mesmo em caso de erro
    print("Finalizando operações...")
    if 'db' in locals():
        db.close_connection()
    if 'scraper' in locals():
        scraper.close_driver()
