import asyncio
import inspect
import flet as ft


class FakePage:
    def __init__(self):
        self.views = [ft.View()]
        self.route_calls = []

    def update(self):
        pass

    async def push_route(self, route):
        self.route_calls.append(route)
        self.on_route_change(None)


def test_uses_default_image_when_book_url_is_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("FLET_APP_STORAGE_DATA", str(tmp_path))
    from view import DEFAULT_IMAGE_URL, build_image_src

    assert build_image_src("") == DEFAULT_IMAGE_URL
    assert build_image_src("   ") == DEFAULT_IMAGE_URL


def test_uses_book_image_url_when_provided(tmp_path, monkeypatch):
    monkeypatch.setenv("FLET_APP_STORAGE_DATA", str(tmp_path))
    from view import build_image_src

    image_url = "https://example.com/book-cover.jpg"

    assert build_image_src(image_url) == image_url


def test_can_navigate_between_add_and_book_detail(tmp_path, monkeypatch):
    monkeypatch.setenv("FLET_APP_STORAGE_DATA", str(tmp_path))

    import database
    from main import main
    from model import Book

    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "bookApp.db"))
    database.Database().insert(
        Book("O Hobbit", "J.R.R. Tolkien", "Uma aventura", 39.9)
    )

    page = FakePage()
    main(page)

    async def exercise_navigation():
        assert len(page.views) == 1
        assert page.views[0].route == "/"

        add_screen = page.views[0].controls[0].content
        assert add_screen.content.controls[0].controls[0].value == "Tela 1"
        go_to_screen_2 = add_screen.content.controls[0].controls[1]
        assert go_to_screen_2.content == "Ir para Tela 2"
        await go_to_screen_2.on_click(None)

        assert len(page.views) == 2
        assert page.views[-1].route == "/add"

        book_screen = page.views[-1].controls[0].content
        assert book_screen.content.controls[0].controls[0].value == "Tela 2"
        go_to_screen_1 = book_screen.content.controls[0].controls[1]
        assert go_to_screen_1.content == "Ir para Tela 1"
        await go_to_screen_1.on_click(None)

        assert len(page.views) == 1
        assert page.views[-1].route == "/"

        await go_to_screen_2.on_click(None)
        assert page.views[-1].route == "/add"

        book_screen = page.views[-1].controls[0].content
        book_card = book_screen.output_col.controls[0]
        assert book_card.ink
        assert inspect.iscoroutinefunction(book_card.on_click)
        await book_card.on_click(None)

        assert len(page.views) == 3
        assert page.views[-1].route == "/book"

        details = page.views[-1].controls[0].content
        detail_controls = details.content.controls
        assert isinstance(detail_controls[1], ft.Image)
        assert detail_controls[1].src == "default_book.jpg"
        assert [control.value for control in detail_controls[2:]] == [
            "O Hobbit",
            "J.R.R. Tolkien",
            "Uma aventura",
            "39.9",
        ]

        back_button = detail_controls[0]
        await back_button.on_click(None)

        assert len(page.views) == 2
        assert page.views[-1].route == "/add"
        assert page.route_calls == ["/add", "/", "/add", "/book", "/add"]

    asyncio.run(exercise_navigation())
