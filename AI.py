from ultralytics import YOLO
import cv2 
import numpy as np
import pyautogui

model = YOLO("EntryAI.pt")

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
