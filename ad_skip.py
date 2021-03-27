# ----------------------------------------------------------------------------------------------------------------
# Click Ad Skip button when playing YouTube in brower(기본 보기 모드 일때만 적용됨, 영화관, 풀화면 모드에서는 지원안됨)
# 두대 모니터 사용시에도 적용가능.
# 2021-03-27 Hwang Inchan
# ----------------------------------------------------------------------------------------------------------------
import pyautogui
import time
from PIL import Image
import pytesseract
#pip install pytesseract
#pip install opencv-python #주요 모듈 설치.
#pip install opencv-contrib-python #주요 및 추가 모듈 설치.
import cv2
import logging

#pip install mss
import mss
import mss.tools

#Monitor master, second
second_mon_no = 1 # setup my pc's second monitor number. This may be various by pc.

#logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# mon_count = [1, 2] # monitor count is 2.
# mon_count = [1] # monitor count is 1.

result = pyautogui.prompt('Please input how many monitors are displayed!(1 or 2)','Input')
if result == '2':
    mon_count = [1, 2] # monitor count is 2.
elif result == '1':
    mon_count = [1] # monitor count is 1.
else:
    system.exit()

curr_pos = pyautogui.position() #current position
print(curr_pos)

# ==========================================
# location of Ad Skip.
# master monitor setting(1229, 784)
# second monitor setting(-683, 777)
x = [1229, -683]
y = [749, 737]
y_adjust = [0, 30]
pyautogui.moveTo(x[0], y[0], duration=0.25)
pyautogui.moveTo(x[1], y[1], duration=0.25)

# width, height is fixed.
width1 = 126
height1 = 39
# ==========================================

#back to start position.
pyautogui.moveTo(curr_pos, duration=0.25) 

ad_skip_text = '광고건너뛰기' #korean

# If YouTube -  is none, exit.
try:
    w =  pyautogui.getWindowsWithTitle("YouTube")[0]
except PyGetWindowException:
    logging.info(PyGetWindowException)
else:
    logging.info(w)

w1 = pyautogui.getActiveWindow()
print(w1)

# loop for every 5sec.
while w is not None:
    text = ''
    file_name = ''

    w1 = pyautogui.getActiveWindow()
    print(w1)
    
    try:
        w = None # initialize.
        w =  pyautogui.getWindowsWithTitle("YouTube")[0]
        logging.info(w)
    except:
        logging.info(w)

    # Maximize Broswer.
    try:
        if w.isActive == False:
            w.activate()
    except:
        logging.info('Error in w.activate')
        w1 = pyautogui.getActiveWindow()
        # YouTube가 아닌 경우 최소화.
        if 'YouTube' not in w1.title:
            w1.minimize()

    try:
        if w.isMaximized == False:
            w.maximize()
    except:
        logging.info('Error in w.maximize')
        w1 = pyautogui.getActiveWindow()
        # YouTube가 아닌 경우 최소화.
        if 'YouTube' not in w1.title:
            w1.minimize()      
    
    for y1 in y_adjust:
        # Capture in Master Monitor.
        # 캡춰시 글자 주위 밖 공간이 생기도록 충분히 캡춰해야함.
        # 글자에 딱맞게 캡춰하거나 잘리면 안됨.

        # 캡춰후 글자 인식하여 "광고 건너뛰기" 일 경우
        #   해당 영역 중간 클릭.
        # 1229, 784
        # 1350 813
        # left=1229, top=784, width=121, height=29-->39    

        for i in mon_count:
            #img_bgr = cv2.imread('ad1.png', cv2.IMREAD_GRAYSCALE) #mastr captuer image.
            #img_bgr = cv2.imread('ad2.png', cv2.IMREAD_GRAYSCALE) #second captuer image.
            file_name = 'ad' + str(i) + str(y1) + '.png'
            logging.info(file_name)
            if i == 2:
                # For second monitor
                with mss.mss() as sct:
                    # Get information of monitor second monitor
                    monitor_number = second_mon_no
                    mon = sct.monitors[monitor_number]

                    # The screen part to capture
                    #1229, 784, 121, 39 Ad Skip
                    monitor = {
                        "top": y[1] + y1,
                        "left": x[1],
                        "width": width1,
                        "height": height1,
                        "mon": monitor_number,
                    }
                    output = file_name.format(**monitor) #ad2.png is for second monitor(filename is fixed).  

                # Capture in Second Monitor.
                # =======================================
                # Grab the data
                sct_img = sct.grab(monitor)

                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                #print(output)
                # =======================================
                img_bgr = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) 
                # img_bgr = cv2.imread('ad.png', cv2.IMREAD_COLOR)
                # convert from BGR to RGB format/mode
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                #cmd경로설정
                pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
                # psm 7 : Treat the image as a single text line.
                text = pytesseract.image_to_string(img_rgb, lang='kor+eng', config='--oem 3 --psm 7')            
            elif i == 1:
                # ad1.png is for master monitor(filename is fixed). 
                region1 = (x[0], y[0] + y1, width1, height1) 
                logging.info(region1)              
                img1_ad = pyautogui.screenshot(file_name, region=region1)                
                #cmd경로설정
                pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
                # psm 7 : Treat the image as a single text line.
                text = pytesseract.image_to_string(img1_ad, lang='kor+eng', config='--oem 3 --psm 7') 

            text = text.replace(' ','') #공백제거.
            logging.info(str(region1) + text)
            #print(text)
            if ad_skip_text in text:
                #print(text)
                logging.info(str(region1) + ad_skip_text)
                #mouse click
                # left=1229, top=784, width=121, height=29-->39
                pyautogui.moveTo(x[i-1] + width1 / 2, y[i-1] + y1 + height1 / 2, duration = 0.25)
                pyautogui.click()
    # while
    if w1 is not None:
        try:
            if w1.isActive == False:
                w1.activate()
            # YouTube가 아닐경우에만.
            if 'YouTube' not in w1.title:
                w1.restore() # previous active window size restore.
        except:
            logging.info('Error in w1.activate')
    time.sleep(5) # Delay 5sec.
