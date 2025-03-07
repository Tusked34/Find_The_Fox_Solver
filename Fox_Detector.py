import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('fox_cropped.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(pytesseract.image_to_boxes(img))

hImg, wImg, _ = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    b = b.split(' ')
    print(b)
    x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(img,(x,hImg-y),(w,hImg-h),(0,0,255),3)

scale_percent = 70  # Pourcentage de réduction
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
img = cv2.resize(img, (width, height))

cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Time code tuto 15:30
# https://www.youtube.com/watch?v=6DjFscX4I_c&ab_channel=Murtaza%27sWorkshop-RoboticsandAI