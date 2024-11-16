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
    # Inicializa a conexão com o PostgreSQL
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    # Conecta ao banco de dados
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Conexão bem-sucedida com o banco de dados!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
   
    # Cria a tabela no banco de dados
    def create_table(self, table_name):
        
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

    # Insere ou atualiza dados na tabela
    def insert_or_update_data(self, table_name, data):
        try:
            # Renomeando as colunas para que sejam consistentes com o banco
            data.rename(columns={
                'Last Month': 'previous_month',
                'Current Month': 'current_month'
            }, inplace=True)

            # Garantindo que as colunas de receita sejam numéricas
            data['current_month'] = pd.to_numeric(data['current_month'], errors='coerce')
            data['previous_month'] = pd.to_numeric(data['previous_month'], errors='coerce')

            query = sql.SQL("""
                INSERT INTO {table} (region, game, current_month, previous_month)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (region, game)  -- Caso a combinação de region e game já exista
                DO UPDATE SET
                    current_month = EXCLUDED.current_month,  -- Atualiza o valor de current_month
                    previous_month = EXCLUDED.previous_month;  -- Atualiza o valor de previous_month
            """).format(table=sql.Identifier(table_name))

            # Inserção em massa para otimizar a performance
            for _, row in data.iterrows():
                self.cursor.execute(query, (row['Region'], row['Game'], row['current_month'], row['previous_month']))
            self.conn.commit()
            print("Dados inseridos ou atualizados com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")

    # Busca dados da tabela e retorna como um DataFrame
    def fetch_data(self, table_name):
        try:
            query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name))
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            colnames = [desc[0] for desc in self.cursor.description]
            print(f"Colunas recuperadas: {colnames}") 

            df = pd.DataFrame(rows, columns=colnames)

            print(f"Dados recuperados do banco de dados: \n{df.head()}")

            return df 
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return pd.DataFrame() 

    # Fecha a conexão com o banco de dados
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Conexão encerrada.")
