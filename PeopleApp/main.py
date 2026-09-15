import flet as ft

def main(page: ft.Page):
    page.title = "Cadastro Básico"
    page.padding = 20

    nome = ft.TextField(label="Nome")
    idade = ft.TextField(label="Idade")
    email = ft.TextField(label="E-mail")

    mensagem = ft.Text(color="red")
    lista = ft.Column()

    def adicionar(e):
        mensagem.value = ""

        if not nome.value or not idade.value or not email.value:
            mensagem.value = "Preencha todos os campos."
            mensagem.color = "red"
        elif not idade.value.isdigit():
            mensagem.value = "Idade deve ser número."
            mensagem.color = "red"
        elif "@" not in email.value:
            mensagem.value = "E-mail inválido."
            mensagem.color = "red"
        else:
            lista.controls.append(
                ft.Text(
                    f"{nome.value}, {idade.value} anos, {email.value}"
                )
            )
            nome.value = ""
            idade.value = ""
            email.value = ""
            mensagem.value = "Cadastro feito!"
            mensagem.color = "green"

        page.update()

    botao = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Adicionar cadastro",
        on_click=adicionar,
    )

    page.add(
        ft.Row(
            [
                nome,
                idade,
                email,
                botao,
            ]
        ),
        mensagem,
        lista,
    )


ft.app(target=main)