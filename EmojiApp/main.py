import flet as ft 

#Lista de emojis que serão exibidos
#essa lista pode ser ampliada, o aplicativo irá lidarcom isso

EMOJIS = ["🐧", "🌋", "🦧", "🦍", "🏳️‍⚧️", "🏳️‍🌈"]
#IDX controla o indice da lista de emojis. Sempre estará atualizado com o emoji que está sendo exibido na tela
IDX = 0

#a função main recebe o objeto pagina, que carrega todos os elementos gráficos (controlss).
#Page é criado pelo fraamework flet durante a execução.
def main(page: ft.Page):
    #configs pg
    #editar a titulo da janela/aba do navegador/nome do app
    page.title = "Emoji App"
    #alinha verticalmente o elemento (control) que foi inserido na pagina ft.MainAxisAlignment.CENTER -> centraliza verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # meus elementos controls
    #ft.Text -> elemento textual
    #parametro value deste objeto contém o valor mostrado na tela
    #size -> altera o tamanho do texto do elemento
    input = ft.Text(value=EMOJIS[0], size = 30)

    #função que e resetada ao clicar em btn
    #função alinhada a main
    #a função é alinhada a main, pois ela precisa acessar a variavel global IDX, que é atualizada a cada clique no botão
    #o PARAMETRO "e" da função carrega informações sobre o evento executado, 
    #é possível acessar a partir de "e" o elemento que sofreu o evento.
    def refresh_click(e):
        global IDX
        #Incremento circular:
        #   *Acresce IDX em 1
        #   *Se IDX for maior que o tamanho da lista EMOJIS
        #       *IDX volta para 0
        #OBS: IDX nunca passa do maior indice da lista
        #IDX = 0,1,2,3,4,0,1,2,3,4...

        IDX = (IDX +1) % len(EMOJIS)
        #altera o elemento textual para o emoji da posição IDX
        input.value = EMOJIS[IDX]

    #Elemento botão com icone de atualizar, que chama a função refresh_click ao ser clicado
    #on_click -> corresponde ao apontamento da função "refresh_click",
    #que será executada toda vez que o botão "btn" for clicado.
        
    btn = ft.IconButton(ft.Icons.REFRESH, on_click = refresh_click)

    #Elemento layout
    #ft.Row -> controi uma linha no aplicativo.
    #Cada linha item inserido em "controls" será exibido na horizontal, um ao lado do outro.
    #"input" e "btn" são os elementos que serão exibidos lado a lado
    #aligment -> alinha os elementos ao centro da linha.
    row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls = [input, btn]
    )

    # adicionando elementos na pagina
    #como "row" contém "input" e "btn", ao adicionar "row" na pagina, os elementos contidos em "row" também serão exibidos.
    page.add(row)

if __name__ == '__main__':
    # ft.app -> dá inicio a execução do aplicativo
    #do app
    ft.run(main)


