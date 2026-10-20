import flet as ft

@ft.control
class Tela1(ft.Container):
    def init(self):
        self.txt_tela1 = ft.Text("Tela 1")
        self.btn_go= ft.Button("Ir para Tela 2", on_click = self.on_click_btn_go)
        self.bgcolor = ft.Colors.BLUE_900
        self.expand = True
        self.col = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.txt_tela1, self.btn_go]
        )
        self.content = ft.Row(
            controls=[self.col]
        )
    def on_click_btn_go(self, e):
        print("Hello")

@ft.control
class Tela2(ft.Container):
    def init(self):
            self.txt_tela1 = ft.Text("Tela 2")
            self.btn_go= ft.Button("Ir para Tela 1", on_click = self.on_click_btn_go)
            self.bgcolor = ft.Colors.RED_900
            self.expand = True
            self.col = ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.txt_tela1, self.btn_go]
            )
            self.content = ft.Row(
                controls=[self.col]
            )
    def on_click_btn_go(self, e):
            print("Hello")
    

def main(page: ft.Page):
    page.title = "App"
    page.padding = 0

    appbar = ft.AppBar(
        title=ft.Text("App"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_VARIANT
    )

    def route_change_listener(e=None):
        page.views.clear()
        page.views.append(
             ft.View(
                  route= '/',
                  controls=[Tela1()]
             )
        )
        if page.route == '/tela2':
            page.views.append(
                 ft.View(
                      route= '/tela2',
                      controls=[Tela2()]
                 )
            )
        page.update()

if __name__ == "__main__":
    ft.run(main)
