# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 23:47:51 2024

@author: USER
"""

import cv2
import numpy as np
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

# 함수 선언 부분
def mouseClick(event):
    """
    캔버스에서 마우스를 클릭했을 때 실행되는 함수.
    클릭 위치에 따라 선 그리기 모드 또는 이미지 이동 모드를 활성화함.
    """
    global x1, y1, active_image, drawing_mode
    x1, y1 = event.x, event.y  # 클릭한 위치 저장

    # 클릭한 위치에 이미지가 있는지 확인
    clicked_item = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if clicked_item:  # 이미지가 있을 경우
        for item in clicked_item:
            if "image" in canvas.gettags(item):  # 'image' 태그를 가진 항목이 있는지 확인
                active_image = item
                drawing_mode = False  # 이미지 이동 모드 활성화
                return
    # 이미지가 없는 경우 선 그리기 모드 활성화
    active_image = None
    drawing_mode = True

def mouseDrag(event):
    """
    캔버스에서 마우스를 드래그할 때 실행되는 함수.
    선을 그리거나 이미지를 이동하는 동작을 수행.
    """
    global x1, y1, penWidth, penColor, img, penColor_rgb, eraserMode, active_image, drawing_mode
    x2, y2 = event.x, event.y

    if drawing_mode:  # 선 그리기 모드
        if eraserMode:  # 지우개 모드
            erase_size = penWidth
            canvas.create_rectangle(x2 - erase_size, y2 - erase_size, x2 + erase_size, y2 + erase_size, fill="white", outline="white")
            cv2.rectangle(img, (x2 - erase_size, y2 - erase_size), (x2 + erase_size, y2 + erase_size), (255, 255, 255), -1)
        else:  # 일반 선 그리기
            canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor, capstyle=ROUND, smooth=True)
            cv2.line(img, (x1, y1), (x2, y2), penColor_rgb, thickness=penWidth)
        x1, y1 = x2, y2
    elif active_image:  # 이미지 이동 모드
        dx, dy = x2 - x1, y2 - y1
        canvas.move(active_image, dx, dy)
        x1, y1 = x2, y2

def mouseDrop(event):
    """
    마우스를 놓았을 때 실행되는 함수.
    선을 그리거나 이미지를 이동하는 동작 수행.
    """
    global x1, y1, active_image, drawing_mode
    x1, y1 = None, None
    active_image = None  # 드롭 이후 이미지 비활성화
    drawing_mode = True  # 기본값으로 복원

def fillColor(event):
    """
    클릭한 위치의 색상을 변경하는 함수.
    """
    global img
    x, y = event.x, event.y
    target_color = img[y, x].tolist()  # 클릭한 위치의 색상 가져오기
    fill_color = askcolor()[0]  # 색상 선택
    if fill_color:
        fill_color_bgr = (int(fill_color[2]), int(fill_color[1]), int(fill_color[0]))
        mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
        cv2.floodFill(img, mask, (x, y), fill_color_bgr, loDiff=(10, 10, 10), upDiff=(10, 10, 10))
        update_canvas()

def update_canvas():
    """
    OpenCV 이미지를 Tkinter Canvas로 업데이트.
    """
    global img, canvas_image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.itemconfig(canvas_image, image=img_tk)
    canvas.img_tk = img_tk  # 참조 유지

# --- 추가된 이미지 관련 기능 ---
def loadImage():
    """
    파일에서 이미지를 불러와 캔버스에 추가하는 함수.
    """
    global images
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path).resize((100, 100), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        image_id = canvas.create_image(150, 150, anchor=CENTER, image=tk_img, tags="image")
        canvas.image_list.append(tk_img)
        images.append((image_id, img))

def resizeImage():
    """
    선택된 이미지의 크기를 변경하는 함수.
    """
    global images, active_image
    if active_image:
        new_width = askinteger("이미지 너비", "새로운 너비를 입력하세요:", minvalue=10, maxvalue=800)
        new_height = askinteger("이미지 높이", "새로운 높이를 입력하세요:", minvalue=10, maxvalue=800)
        if new_width and new_height:
            for image_id, original_img in images:
                if image_id == active_image:
                    resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    tk_resized_img = ImageTk.PhotoImage(resized_img)
                    canvas.itemconfig(active_image, image=tk_resized_img)
                    canvas.image_list.append(tk_resized_img)
                    images[images.index((image_id, original_img))] = (image_id, resized_img)
                    break

def toggle_eraser():
    """
    지우개 모드를 활성화하거나 비활성화하는 함수.
    """
    global eraserMode
    eraserMode = not eraserMode
    if eraserMode:
        eraser_button.config(relief=RAISED, bg="lightgrey")
    else:
        eraser_button.config(relief=FLAT, bg="SystemButtonFace")

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1 = None, None
penColor = 'black'
penColor_rgb = (0, 0, 0)
penWidth = 5
img = np.ones((300, 300, 3), dtype=np.uint8) * 255
eraserMode = False
images = []
active_image = None
drawing_mode = True

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("OpenCV 기반 그림판")
    canvas = Canvas(window, height=600, width=800, bg="white")
    canvas.pack()
    canvas.image_list = []  # GC 방지를 위한 참조 리스트

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas_image = canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk

    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<B1-Motion>", mouseDrag)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.bind("<Button-3>", fillColor)

    # 메뉴 설정
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)

    toolMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="도구", menu=toolMenu)
    toolMenu.add_command(label="이미지 불러오기", command=loadImage)
    toolMenu.add_command(label="이미지 크기 조정", command=resizeImage)

    eraser_button = Button(window, text="지우개", command=toggle_eraser)
    eraser_button.pack(side=LEFT, padx=10)

    window.mainloop()
