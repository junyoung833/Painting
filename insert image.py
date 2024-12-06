from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk

# 함수 선언 부분
def mouseClick(event):
    global x1, y1, active_image, drawing_mode
    x1, y1 = event.x, event.y

    # 클릭한 위치에 이미지가 있는지 판별
    clicked_item = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if clicked_item:  # 이미지가 있는 경우
        for item in clicked_item:
            if "image" in canvas.gettags(item):  # 이미지 태그 확인
                active_image = item
                drawing_mode = False  # 이미지 이동 모드 활성화
                return
    # 빈 캔버스 클릭 시 선 그리기 모드 활성화
    active_image = None
    drawing_mode = True

def mouseDrop(event):
    global x1, y1, x2, y2, active_image, penWidth, penColor, drawing_mode
    x2, y2 = event.x, event.y

    if drawing_mode:  # 선 그리기 모드
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)
    elif active_image:  # 이미지 이동 모드
        dx, dy = x2 - x1, y2 - y1
        canvas.move(active_image, dx, dy)

def loadImage():
    global img, tk_img, active_image
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)

        # 기본 크기로 이미지를 설정
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        # 이미지를 캔버스에 추가
        active_image = canvas.create_image(150, 150, anchor=CENTER, image=tk_img, tags="image")
        canvas.image = tk_img  # 이미지 참조 유지 (GC 방지)

def resizeImage():
    global img, tk_img, active_image
    if active_image:
        new_width = askinteger("이미지 너비", "새로운 너비를 입력하세요:", minvalue=10, maxvalue=800)
        new_height = askinteger("이미지 높이", "새로운 높이를 입력하세요:", minvalue=10, maxvalue=800)
        if new_width and new_height:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            canvas.itemconfig(active_image, image=tk_img)
            canvas.image = tk_img  # 이미지 참조 유지 (GC 방지)

def getColor():
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1, x2, y2 = None, None, None, None
penColor = 'black'
penWidth = 5
img = None
tk_img = None
active_image = None
drawing_mode = True  # 선 그리기 모드 기본값

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 프로그램 (이미지 추가 및 크기 조정)")

    # 캔버스 설정
    canvas = Canvas(window, height=600, width=800, bg="white")
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)  # 드래그 끝날 때 선 그리기 또는 이동
    canvas.pack()

    # 메뉴 설정
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    # 설정 메뉴
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)

    # 도구 메뉴
    toolMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="도구", menu=toolMenu)
    toolMenu.add_command(label="이미지 불러오기", command=loadImage)
    toolMenu.add_command(label="이미지 크기 조정", command=resizeImage)

    window.mainloop()
