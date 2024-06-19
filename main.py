import flet as ft
from asyncio import sleep
from AI import search_btn
from pyautogui import click
from UI import Frame

class SearchFrame(Frame):
    
    def __init__(self,page:ft.Page):
        self.searching = False

        self.page = page

        self.main_btn = ft.FloatingActionButton(
            content=ft.Row(
                [ft.Text("Поиск",color='white')],
                alignment="center",
                spacing=5
            ),
            width=self.page.window.width*0.9,
            shape=ft.RoundedRectangleBorder(radius=5),
            bgcolor='yellow700',
            on_click=self.search
        )   

        self.text_help = ft.Text('Поиск...')
        self.pb = ft.ProgressBar(width=self.page.window.width,value=0)
        self.pb_col = ft.Column([self.pb])
        
        super().__init__(
            obj=[
                self.main_btn,
                self.pb_col
                ],
            label_text='Поиск игры',
            label_icon=ft.icons.SEARCH
        )

    async def search(self,event):
        self.searching = False if self.searching else True
        await self.set_status("searching") if self.searching else await self.set_status("stopped")
        while self.searching:
            result = search_btn()
            if len(result) > 0:
                self.searching = False
                await self.set_status("found")
                btn_position = ((result[2]+result[0])/2,(result[3]+result[1])/2)
                click(btn_position[0],btn_position[1])
                await sleep(0.9)
                await self.set_status("stopped")
                break
            else:
                await sleep(1)

    async def set_status(self,status:str):
        if status == 'searching':
            if self.text_help not in self.pb_col.controls:
                self.pb_col.controls.insert(0,self.text_help)
            self.pb.value = None
        elif status == 'stopped':
            if self.text_help in self.pb_col.controls:
                self.pb_col.controls.remove(self.text_help)
            self.text_help.value = 'Поиск...'
            self.pb.value = 0
            self.text_help.update()
        elif status == 'found':
            if self.text_help not in self.pb_col.controls:
                self.pb_col.controls.insert(0,self.text_help)
            self.text_help.value = 'Игра найдена'
            self.pb.value = 100
            self.text_help.update()
        self.pb_col.update()
        self.pb.update()
        self.page.update()

class SettingFrame(Frame):
    def __init__(self,page:ft.Page):

        self.page = page

        

        super().__init__(
            obj=[], 
            label_text='Настройки',
            label_icon=ft.icons.SETTINGS
            )
    

def main(page:ft.Page):
    page.title = "Entry"
    page.window.resizable = False
    page.window.width = 400
    page.window.height = 500 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme(color_scheme_seed="yellow700")
    page.update()
    search_frame = SearchFrame(page)
    # setting_frame = SettingFrame(page)
    page.add(search_frame,setting_frame)

if __name__ == '__main__':
    ft.app(target=main)