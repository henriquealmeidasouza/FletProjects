import flet as ft
from model import Book
from view import BookApp, build_book_details

def main(page: ft.Page):
    page.title = 'BookApp'
    page.padding = 0

    async def go_back(e=None):
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)

    async def open_book(book: Book):
        page.views.append(
            ft.View(
                route="/book",
                controls=[
                    ft.SafeArea(
                        expand=True,
                        content=build_book_details(book, go_back),
                    )
                ],
            )
        )
        await page.push_route("/book")

    async def open_screen_2(e=None):
        page.views.append(
            ft.View(
                route="/add",
                controls=[
                    ft.SafeArea(
                        expand=True,
                        content=BookApp(
                            on_switch_screen=go_back,
                            on_open_book=open_book,
                            screen_number=2,
                        ),
                    )
                ],
            )
        )
        await page.push_route("/add")

    page.on_route_change = lambda e: page.update()
    page.on_view_pop = go_back
    page.views.clear()
    page.views.append(
        ft.View(
            route="/",
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=BookApp(
                        on_switch_screen=open_screen_2,
                        on_open_book=open_book,
                        screen_number=1,
                    ),
                )
            ],
        )
    )

if __name__ == "__main__":
    ft.run(main)

'''def main(page: ft.Page):
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
    
'''



   