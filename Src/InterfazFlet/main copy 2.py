import flet as ft
Width, Height = 550,700

class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.GREEN_800
        self.text = text
        self.on_click = on_click
def clicked():
    pass

async def main(page: ft.Page):

    page.window_height=Height
    page.window_width=Width
    page.padding=0
    page.adaptive = True

    ItemsSuperior =[
        ft.Slider(min=0, max=100, divisions=100, label="x:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="y:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="z:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="R:{value}")
    ]
    Sliders = [ft.Container(content=ft.Column(ItemsSuperior),width=250,height=300,margin=ft.margin.only(top=20)),
               ft.Container(width=265,height=300,border=ft.border.all(color="red"))]
    
    Superior = ft.Container(content=ft.Row(Sliders),width=530,height=300,margin=ft.margin.only(top=15))

    ItemsMedio =[ft.Row(spacing=120,controls=[MyButton(text="Boton1",on_click=clicked),
        MyButton(text="Boton2",on_click=clicked),
        MyButton(text="Boton3",on_click=clicked)],height=100),
        ft.Row(spacing=120,controls=[MyButton(text="Boton4",on_click=clicked),
        MyButton(text="Boton5",on_click=clicked),
        MyButton(text="Boton6",on_click=clicked)],height=100)]
    
    

    


    Medio = ft.Container(content=ft.Column(ItemsMedio),
                         width=530,height=200,margin=ft.margin.only(top=5),
                         border=ft.border.all(color="blue"))
    
    Inferior = ft.Container(width=530,height=100,margin=ft.margin.only(top=5),
                            border=ft.border.all(color="blue"))
   
    colum = ft.Column(spacing=0,controls=[
        Superior,
        Medio,
        Inferior
    ]

    )

    container = ft.Container(colum,height=Height,alignment=ft.alignment.top_center)
    await page.add_async(
        container
        )

ft.app(target=main)