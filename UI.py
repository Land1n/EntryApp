import flet as ft


class Frame(ft.Container):
    def __init__(self,obj:list=[],label_text="Frame",label_icon=ft.icons.CIRCLE_OUTLINED):
        super().__init__()

        self.obj = obj
        self.label_text = label_text
        self.label_icon = label_icon

        self.bgcolor='grey900'
        self.padding=20
        self.border_radius=20
        self.content=ft.Column(
            [
                ft.Row([ft.Icon(name=self.label_icon),ft.Text(self.label_text,size=20)]),
                *self.obj
            ]
        )

if __name__ == '__main__':
    def main(page:ft.Page):
        page.add(Frame())
    ft.app(main)
