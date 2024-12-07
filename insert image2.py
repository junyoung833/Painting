from tkinter import *
from tkinter.filedialog import askopenfilename  # 파일 열기 대화 상자를 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 위한 모듈
from tkinter.simpledialog import askinteger  # 정수 입력 대화 상자를 위한 모듈
from PIL import Image, ImageTk  # 이미지를 로드하고 캔버스에 출력하기 위한 PIL 모듈

# 함수 선언 부분
def mouseClick(event):
    """
    캔버스에서 마우스를 클릭했을 때 실행되는 함수.
    클릭 위치에 따라 선 그리기 모드 또는 이미지 이동 모드를 활성화함.
    """
    global x1, y1, active_image, drawing_mode
    x1, y1 = event.x, event.y  # 클릭한 위치 저장

#까지 기존 코드

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

#부터
def mouseDrop(event):
    """
    마우스를 놓았을 때 실행되는 함수.
    선을 그리거나 이미지를 이동하는 동작 수행.
    """
    global x1, y1, x2, y2, active_image, penWidth, penColor, drawing_mode
    x2, y2 = event.x, event.y  # 드롭 위치 저장
#까지 active_image, drawing_mode 추가됨

    if drawing_mode:  # 선 그리기 모드일 경우
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)  # 선 생성
    elif active_image:  # 이미지 이동 모드일 경우
        dx, dy = x2 - x1, y2 - y1  # 이동 거리 계산
        canvas.move(active_image, dx, dy)  # 이미지 이동

# --- 추가된 이미지 관련 기능 ---
def loadImage():
    """
    파일에서 이미지를 불러와 캔버스에 추가하는 함수.
    이미지 크기를 조정하고 캔버스에 삽입함.
    """
    global images  # 이미지 리스트
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])  # 이미지 파일 선택
    if file_path:
        img = Image.open(file_path)  # 이미지 열기

        # 기본 크기로 이미지 크기 조정
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        # 이미지를 캔버스에 추가하고 참조 리스트에 저장
        image_id = canvas.create_image(150, 150, anchor=CENTER, image=tk_img, tags="image")
        canvas.image_list.append(tk_img)  # GC 방지용 참조 리스트에 추가
        images.append((image_id, img))  # 이미지 ID와 원본 이미지 저장

def resizeImage():
    """
    선택된 이미지의 크기를 변경하는 함수.
    새로운 너비와 높이를 입력받아 이미지를 조정함.
    """
    global images, active_image
    if active_image:
        # 새로운 너비와 높이를 입력받음
        new_width = askinteger("이미지 너비", "새로운 너비를 입력하세요:", minvalue=10, maxvalue=800)
        new_height = askinteger("이미지 높이", "새로운 높이를 입력하세요:", minvalue=10, maxvalue=800)
        if new_width and new_height:
            for image_id, original_img in images:
                if image_id == active_image:
                    # 원본 이미지를 크기 조정
                    resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    tk_resized_img = ImageTk.PhotoImage(resized_img)

                    # 캔버스에서 이미지 갱신
                    canvas.itemconfig(active_image, image=tk_resized_img)
                    canvas.image_list.append(tk_resized_img)  # GC 방지용 참조 리스트에 추가
                    images[images.index((image_id, original_img))] = (image_id, resized_img)  # 리스트 업데이트
                    break

# --- 기존 선 색상 및 두께 설정 기능 ---
def getColor():
    """
    색상 선택 대화 상자를 통해 선 색상을 설정하는 함수.
    """
    global penColor
    color = askcolor()  # 색상 선택
    penColor = color[1]  # 선택된 색상 값 저장

def getWidth():
    """
    선 두께를 설정하는 함수.
    정수 입력 대화 상자를 통해 두께를 입력받음.
    """
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1, x2, y2 = None, None, None, None  # 선의 시작점과 끝점 좌표
penColor = 'black'
penWidth = 5
images = []  # 이미지 ID와 원본 이미지를 저장하는 리스트
active_image = None  # 선택된 이미지 ID
drawing_mode = True  # 기본값은 선 그리기 모드

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 프로그램 (이미지 추가 및 크기 조정)")

    # 캔버스 설정
    canvas = Canvas(window, height=600, width=800, bg="white")
    canvas.bind("<Button-1>", mouseClick)  # 마우스 클릭 이벤트
    canvas.bind("<ButtonRelease-1>", mouseDrop)  # 마우스 드롭 이벤트
    canvas.pack()
    canvas.image_list = []  # GC 방지를 위한 참조 리스트

    # 메뉴 설정
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    # 설정 메뉴
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)  # 선 색상 설정
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)  # 선 두께 설정

    # 도구 메뉴
    toolMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="도구", menu=toolMenu)
    toolMenu.add_command(label="이미지 불러오기", command=loadImage)  # 이미지 불러오기 추가
    toolMenu.add_command(label="이미지 크기 조정", command=resizeImage)  # 이미지 크기 조정 추가

    window.mainloop()
