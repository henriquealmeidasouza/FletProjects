import flet as ft
import os,databese, Database, Book

def main(page: ft.Page):
    db_path = os.path.join(os.environ['FLET_APP_STORAGE_DATA'], 'bookApp.db')

    db = Database(db_path)
    #durante uma inserção
    book = Book("O Senhor dos Anéis", "J.R.R. Tolkien", "Um livro de fantasia épica", 39.90)

    db.insert(book)
    

    page.title = 'BookApp'
    page.add(ft.Column())
    page.padding = 20
    
    Titulo= ft.TextField(label="Titulo")
    Autor= ft.TextField(label="Autor")
    Descricao = ft.TextField(label="Descricao")
    Preco = ft.TextField(label="Preco")
    
    page.add(
        ft.Text("Book App"),
        Titulo,
        Autor,
        Descricao,
        ft.Row([Preco, ft.Button("+")]),
        ft.Divider(),
        ft.Text("Titulo"),
        ft.Text("Autor"),
        ft.Text("Descricao"),
        ft.Text("Preco"))
    
    book = ft.Column()
    
    def adicionar(e):
        book = ft.Column([
            ft.Text(Titulo.value),
            ft.Text(Autor.value),
            ft.Text(Descricao.value),
            ft.Text("R$ " + Preco.value),
            ft.Divider()
        ])
        book.controls.append(book)
        Titulo.value = ""
        Autor.value = ""
        Descricao.value = ""
        Preco.value = ""
        page.update()
    
        botao = ft.Button("+", on_click=adicionar)
    
        page.add(
            ft.Text("Book App"),
            Titulo,
            Autor,
            Descricao,
            ft.Row([Preco, botao]),
            book
            )
    

if __name__ == "__main__":
    ft.run(main)

   