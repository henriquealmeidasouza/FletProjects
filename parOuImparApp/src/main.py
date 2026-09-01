import flet as ft


def main(page: ft.Page):
    #------Event Listenners
    def on_click_send(e):
        value = input_txt.value
        try:
            int_value = int(value)
            if(int_value % 2 == 0):
                output_txt.value += f'{int_value} é par\n'
            else:
                output_txt.value += f'{int_value} é ímpar\n'
                print(f'{int_value} é par')
            print(int_value)
        except ValueError:
            output_txt.value += f'{value} não é um número inteiro\n'
            print('Erro')
        input_txt.value = ''

    #--------widjets
    input_txt = ft.TextField(
        expand = True,
        hint_text = 'Digite um número inteiro: '
        )
    input_btn = ft.IconButton(
        icon = ft.Icons.SEND,
        on_click = on_click_send
        )
    output_txt = ft.Text(value = '')

    #--------layout
    input_row = ft.Row(
        controls = [input_txt, input_btn]
    )
    output_col = ft.Column(
        expand= True,
        horizontal_alignment= ft.CrossAxisAlignment.STRETCH,
        scroll= ft.ScrollMode.AUTO,
        controls = [output_txt]
    )
    main_col = ft.Column(
        expand = True,
        controls = [input_row, output_col]
    )

    #-------Página
    page.title = 'ParOuImparApp'
    page.add(main_col)


if __name__ == "__main__":
    ft.run(main)
