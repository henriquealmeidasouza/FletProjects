import flet as  ft

def main(page: ft.Page):
    #Muda o titulo da janela na web e do app no mobile
    page.title = 'helloApp'
    #Alinha os elementos inseridos na pagina ao centro da tela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    text = ft.Text(value='Hello World', text_align=ft.TextAlign.CENTER, width=1200)
    text2 = ft.Text(value='Hello World2')
   #adiciona o texto na tela, adiciona elementos controls dentro da pagina
    page.add(text, text2)

if __name__ == '__main__':
    #app cria o objeto page
    #o objeto page e enviado para a função target para ser preenchida
    ft.app(target=main)

