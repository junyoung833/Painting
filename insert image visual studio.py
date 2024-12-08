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
    # 빈 캔버스 클릭 시 자유 그리기 모드 활성화
    active_image = None
    drawing_mode = True

def mouseDrag(event):
    global x1, y1, penWidth, penColor, drawing_mode
    if drawing_mode:  # 자유 그리기 모드
        x2, y2 = event.x, event.y
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)
        x1, y1 = x2, y2  # 시작점을 현재 위치로 갱신

def mouseDrop(event):
    global x1, y1, x2, y2, active_image, drawing_mode
    x2, y2 = event.x, event.y

    if not drawing_mode and active_image:  # 이미지 이동 모드
        dx, dy = x2 - x1, y2 - y1
        canvas.move(active_image, dx, dy)

def loadImage():
    global images  # 여러 이미지를 관리하기 위한 리스트
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)

        # 기본 크기로 이미지를 설정
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        # 이미지를 캔버스에 추가
        image_id = canvas.create_image(150, 150, anchor=CENTER, image=tk_img, tags="image")
        canvas.image_list.append(tk_img)  # 이미지 참조 유지 (GC 방지)
        images.append((image_id, img))  # 이미지 ID와 원본 이미지 저장

def resizeImage():
    global images, active_image
    if active_image:
        new_width = askinteger("이미지 너비", "새로운 너비를 입력하세요:", minvalue=10, maxvalue=800)
        new_height = askinteger("이미지 높이", "새로운 높이를 입력하세요:", minvalue=10, maxvalue=800)
        if new_width and new_height:
            for image_id, original_img in images:
                if image_id == active_image:
                    # 원본 이미지를 크기 조정
                    resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    tk_resized_img = ImageTk.PhotoImage(resized_img)

                    # 기존 이미지 업데이트
                    canvas.itemconfig(active_image, image=tk_resized_img)
                    canvas.image_list.append(tk_resized_img)  # GC 방지
                    images[images.index((image_id, original_img))] = (image_id, resized_img)  # 업데이트
                    break

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
images = []  # 여러 이미지를 관리하기 위한 리스트
active_image = None
drawing_mode = True  # 선 그리기 모드 기본값

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 프로그램 (이미지 추가 및 크기 조정)")

    # 캔버스 설정
    canvas = Canvas(window, height=600, width=800, bg="white")
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<B1-Motion>", mouseDrag)  # 드래그 시 자유 그리기
    canvas.bind("<ButtonRelease-1>", mouseDrop)  # 드래그 끝날 때 선 그리기 또는 이동
    canvas.pack()
    canvas.image_list = []  # 이미지 참조 유지 리스트

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
