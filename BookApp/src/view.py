import flet as ft

from database import Database
from model import Book

DEFAULT_IMAGE_URL = "default_book.jpg"


def build_image_src(url: str):
    cleaned_url = (url or "").strip()
    if not cleaned_url:
        return DEFAULT_IMAGE_URL

    if cleaned_url.startswith("data:image/"):
        return cleaned_url

    if cleaned_url.startswith("//"):
        return "https:" + cleaned_url

    if "://" not in cleaned_url:
        if cleaned_url.startswith("/"):
            return cleaned_url
        return "https://" + cleaned_url

    return cleaned_url


def build_book_details(book: Book, on_back):
    return ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK,
        padding=20,
        content=ft.Column(
            expand=True,
            scroll="auto",
            controls=[
                ft.Button("Voltar", on_click=on_back),
                ft.Image(
                    src=build_image_src(book.image_url),
                    width=180,
                    height=250,
                    fit="cover",
                    border_radius=12,
                ),
                ft.Text(
                    book.title,
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(book.author, size=16, color=ft.Colors.BLUE_100),
                ft.Text(book.desc, size=16, color=ft.Colors.GREY_300),
                ft.Text(str(book.price), size=16, color=ft.Colors.GREEN_300),
                *(
                    [ft.Text(book.image_url, size=14, color=ft.Colors.GREY_300)]
                    if book.image_url
                    else []
                ),
            ],
            spacing=12,
        ),
    )


@ft.control
class BookApp(ft.Container):
    def __init__(self, on_switch_screen=None, on_open_book=None, screen_number=1):
        super().__init__()
        self.expand = True
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = 18
        self.padding = 20
        self.db = Database()
        self.on_switch_screen = on_switch_screen
        self.on_open_book = on_open_book

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    f"Tela {screen_number}",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Button(
                    f"Ir para Tela {3 - screen_number}",
                    on_click=self.on_switch_screen,
                ),
            ],
        )

        self.title_txt = ft.TextField(
            label="Title",
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_400,
        )
        self.author_txt = ft.TextField(
            label="Author",
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_400,
        )
        self.desc_txt = ft.TextField(
            label="Description",
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_400,
            multiline=True,
            min_lines=2,
            max_lines=4,
        )
        self.price_txt = ft.TextField(
            label="Price",
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_400,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(
                allow=True,
                regex_string=r"^\d*\.?\d*$",
                replacement_string="",
            ),
        )
        self.image_url_txt = ft.TextField(
            label="Image URL",
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_400,
        )
        self.output_col = ft.Column(expand=True, spacing=10, scroll="auto")

        save_btn = ft.IconButton(
            icon=ft.Icons.ADD,
            on_click=self.save_book,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
            ),
            width=90,
            height=140,
        )

        form_row = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.title_txt,
                            self.author_txt,
                            self.desc_txt,
                            self.price_txt,
                            self.image_url_txt,
                        ],
                        spacing=8,
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                    padding=12,
                ),
                ft.Container(
                    content=save_btn,
                    alignment=ft.Alignment(0.5, 0.5),
                    padding=8,
                    width=90,
                    height=120,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                ),
            ],
        )

        self.content = ft.Column(
            expand=True,
            controls=[header, form_row, self.output_col],
            spacing=20,
        )
        self.load_books()

    def load_books(self):
        self.output_col.controls.clear()
        books = self.db.fetch_all()
        for book in books:
            self.new_book_entry(book)

        try:
            self.output_col.update()
        except RuntimeError:
            pass

    def new_book_entry(self, book: Book):
        image_url = build_image_src(book.image_url)
        image = ft.Image(
            src=image_url,
            width=120,
            height=170,
            fit="cover",
            border_radius=12,
        )

        book_info_col = ft.Column(
            controls=[
                ft.Text(book.title, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(book.author, size=12, color=ft.Colors.BLUE_100),
                ft.Text(book.desc, size=12, color=ft.Colors.GREY_300),
            ],
            spacing=4,
            expand=True,
        )
        book_price_txt = ft.Text("R$ " + str(book.price), size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_300)
        book_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[image, book_info_col],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                    padding=12,
                ),
                ft.Container(
                    content=book_price_txt,
                    alignment=ft.Alignment(1, 0.5),
                    width=90,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                    padding=12,
                ),
            ],
        )
        async def open_book(e):
            if self.on_open_book:
                await self.on_open_book(book)

        self.output_col.controls.append(
            ft.Container(
                content=book_row,
                ink=True,
                on_click=open_book,
            )
        )

    def clear_fields(self):
        self.title_txt.value = ""
        self.author_txt.value = ""
        self.desc_txt.value = ""
        self.price_txt.value = ""
        self.image_url_txt.value = ""

    def save_book(self, e):
        title = (self.title_txt.value or "").strip()
        author = (self.author_txt.value or "").strip()
        desc = (self.desc_txt.value or "").strip()
        price_value = (self.price_txt.value or "").strip()
        image_url = (self.image_url_txt.value or "").strip()

        if not title or not author or not desc or not price_value:
            return

        try:
            price = float(price_value)
        except ValueError:
            return

        book = Book(title, author, desc, price, image_url)
        self.new_book_entry(book)
        self.db.insert(book)

        self.clear_fields()

        try:
            self.page.update()
        except RuntimeError:
            self.update()