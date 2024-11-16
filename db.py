import psycopg2
from psycopg2 import sql
import pandas as pd

# Configurações do banco de dados
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

class PostgreSQLDatabase:
    def __init__(self, config):
        """Inicializa a conexão com o PostgreSQL."""
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        """Conecta ao banco de dados."""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Conexão bem-sucedida com o banco de dados!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_table(self, table_name):
        """Cria uma tabela no banco de dados."""
        try:
            query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {table} (
                    id SERIAL PRIMARY KEY,
                    region TEXT,
                    game TEXT,
                    current_month NUMERIC,
                    previous_month NUMERIC,
                    UNIQUE(region, game)  -- Garantir unicidade com base em region e game
                );
            """).format(table=sql.Identifier(table_name))
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Tabela '{table_name}' criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

    def insert_or_update_data(self, table_name, data):
        """Insere ou atualiza dados na tabela."""
        try:
            query = sql.SQL("""
                INSERT INTO {table} (region, game, current_month, previous_month)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (region, game)  -- Caso a combinação de region e game já exista
                DO UPDATE SET
                    current_month = EXCLUDED.current_month,  -- Atualiza o valor de current_month
                    previous_month = EXCLUDED.previous_month;  -- Atualiza o valor de previous_month
            """).format(table=sql.Identifier(table_name))

            # Verificando as colunas do DataFrame para depurar
            print(f"Colunas no DataFrame: {data.columns}")

            # Renomeando as colunas para que sejam consistentes com o banco
            data.rename(columns={
                'Last Month': 'previous_month',
                'Current Month': 'current_month'
            }, inplace=True)

            for _, row in data.iterrows():
                print(f"Inserindo ou atualizando dados: {row['Region']}, {row['Game']}, {row['current_month']}, {row['previous_month']}")
                self.cursor.execute(query, (row['Region'], row['Game'], row['previous_month'], row['current_month']))
            self.conn.commit()
            print("Dados inseridos ou atualizados com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")

    def fetch_data(self, table_name):
        """Busca dados da tabela."""
        try:
            query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name))
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Conexão encerrada.")
