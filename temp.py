from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *

# 함수 선언 부분
def mouseClick(event):
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def getColor():
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.",
                          minvalue=1, maxvalue=10)

# 전역 변수 선언 부분
window = None
canvas = None
x1, x2, y1, y2 = None, None, None, None  # 선의 시작점과 끝점
penColor = 'black'
penWidth = 5

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 비슷한 프로그램")

    # 캔버스 설정
    canvas = Canvas(window, height=300, width=300)
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
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

    # 도구 메뉴 (새로운 메뉴 추가)
    toolMenu = Menu(mainMenu) #"도구" 메뉴를 생성
    mainMenu.add_cascade(label="도구", menu=toolMenu) #"설정" 메뉴 바로 옆에 "도구" 메뉴 추가
    # cascade는 설정 바로 옆에 서브 메뉴를 추가하는 함수, 바로 옆에 생성

    window.mainloop()
