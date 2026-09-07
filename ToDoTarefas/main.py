import flet as ft


def main(page: ft.Page):

    def on_click_add(e):
        value = input_txt.value

        if value.strip() == '':
            dialog.content = ft.Text('O campo está vazio!')
            page.show_dialog(dialog)
        else:
            add_task(value.strip())

        input_txt.value = ''
        input_txt.focus()
        page.update()

    def on_submit_input(e):

        on_click_add(e)

    def close_dialog(e):
        page.pop_dialog()
        page.update()

    def add_task(text):
        checkbox = ft.Checkbox(value=False)
        task_txt = ft.Text(
            value=text,
            expand=True,
        )

        def on_change_checkbox(e):
            if checkbox.value:
                task_txt.italic = True
                task_txt.color = ft.Colors.GREY
                task_txt.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
            else:
                task_txt.italic = False
                task_txt.color = None
                task_txt.style = None
            page.update()

        checkbox.on_change = on_change_checkbox

        def on_click_delete(e):
            output_col.controls.remove(task_row)
            page.update()

        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            on_click=on_click_delete,
        )

        task_row = ft.Row(
            controls=[checkbox, task_txt, delete_btn],
            alignment=ft.MainAxisAlignment.START,
        )

        output_col.controls.append(task_row)

    # ----- Widgets
    dialog = ft.AlertDialog(
        title=ft.Text('Erro!'),
        content=ft.Text(''),
        actions=[
            ft.TextButton('Fechar', on_click=close_dialog)
        ]
    )

    input_txt = ft.TextField(
        expand=True,
        hint_text='Digite uma tarefa... (ex: passear com o cachorro)',
        on_submit=on_submit_input,
    )

    input_btn = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=on_click_add,
    )

    # ----- Layout
    input_row = ft.Row(
        controls=[input_txt, input_btn]
    )

    output_col = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
        controls=[]
    )

    main_col = ft.Column(
        expand=True,
        controls=[input_row, output_col]
    )

    # ----- Página
    page.title = 'ToDoApp'
    page.add(main_col)


if __name__ == "__main__":
    ft.run(main)