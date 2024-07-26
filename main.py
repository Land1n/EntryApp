import flet as ft
from asyncio import sleep
# from AI import search_btn
from pyautogui import click
# from UI import Frame

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

from ultralytics import YOLO
import cv2 
import numpy as np
import pyautogui

model = YOLO("assets/EntryAI.pt")

def search_btn():
    img = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    result = model(img)
    cls = result[0].boxes.cls.cpu().numpy().astype(int)
    if len(cls) > 0:
        box = result[0].boxes.xyxy.cpu().numpy().astype(int)
        box = box[0]
        return box
    return []


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
    
class MainPage(ft.Column):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page

        self.search_frame = SearchFrame(self.page)
        self.setting_frame = SettingFrame(self.page)

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [ self.search_frame, self.setting_frame ]
def main(page:ft.Page):
    page.title = "Entry"
    page.window.resizable = False
    page.window.width = 400
    page.window.height = 500 
    page.theme = ft.Theme(color_scheme_seed="yellow700")
    page.add(MainPage(page))
    

ft.app(target=main)