import os 
import sqlite3
from model import Book

#
DB_PATH = os.path.join(os.environ['FLET_APP_STORAGE_DATA'], 'bookApp.db')

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

FETCH_BOOKS_QUERY = '''
    SELECT title, author, desc, price FROM books;
'''

class Database(object):
    def __init__(self):
        self.__create_tables()
    def __connect(self) -> sqlite3.Connection:
        '''
        Abre o arquivo sqlite para consulta/modificação
        *    abre a conexão "conn" com o banco sqlite
        *    abre o arquivo bookApp.sql e lê o script SQL
        *    cria tabelas a partir da leitura do script
        *    fecha "conn" e fecha "sqlf"
        '''
        return sqlite3.connect(DB_PATH)
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
        '''
        fetch_all pega todos os livros do banco de dados e retorna uma lista de objetos Book'''

        ret = []
        with self.__connect() as conn:
            cur = conn.cursor()
            cur.execute(FETCH_BOOKS_QUERY)
            #cada valor de rows corresponde a uma tupla
            #contendo os valores de cada coluna do banco de dados
            rows = cur.fetchall()
            for row in rows:
                book = Book(
                    title=str(row[0]),
                    author=str(row[1]),
                    desc=str(row[2]),
                    price=float(row[3])
                )
                ret.append(book)
        return ret