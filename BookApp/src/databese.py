import os 
import sqlite3
from model import Book

#os.path join concatena caminhos com o separador do sistema
#i.e. no Windows, o separador é \ e no Linux é /
BOOKAPP_SQL_PATH = os.path.join(
    #nome do diretório em que o arquivo database.py está
    #ex: /home/user/BookApp/src/sql
    os.path.dirname(os.path.abspath(__file__)), 
'sql', 
'bookApp.sql'
)

INSERT_BOOK_QUERY = '''
    INSERT INTO books (title, author, desc, price) 
        VALUES (?, ?, ?, ?);
'''

class Database(object):
    def __init__(self, db_path:str):
        '''db_path: caminho para o arquivo de banco de dados(sqlite)'''
        self.db_path = db_path
        self.__create_tables()
    def __connect(self) -> sqlite3.Connection:
        '''
        Abre o arquivo sqlite para consulta/modificação
        *    abre a conexão "conn" com o banco sqlite
        *    abre o arquivo bookApp.sql e lê o script SQL
        *    cria tabelas a partir da leitura do script
        *    fecha "conn" e fecha "sqlf"
        '''
        return sqlite3.connect(self.db_path)
    def __create_tables(self):
        ''''Cria as tabelas do banco de dados'''
        with self.__connect() as conn:
            with open(BOOKAPP_SQL_PATH, 'r', encoding='utf-8') as sqlf:
                sql_script = sqlf.read()
            conn.executescript(sql_script)
    def insert(self, book: Book):
        '''
        Insere um livro no banco de dados
        *   recebee um objeto book pertencente a classe book
        *   conectar ao banco de dados
        *   executar a query de inserção de livro no banco
        '''

        with self.__connect() as conn:
            conn.execute(INSERT_BOOK_QUERY, (book.title, book.author, book.desc, book.price))
    def fetch_all(self) -> list[Book]:
        pass