import cv2 as cv
import numpy as np

#untuk mengatur size windows/layar
panjang_windows = 500
lebar_windows = 700
blank = np.ones((panjang_windows,lebar_windows,3), dtype='uint8') * 255

# Membuat kotak perseginya
#(pintu)
blank[100:330, 470:640] = 168,140,84

#(jendela)
blank[120:200, 500:610] = 82, 80, 5

#(paling depan)
blank[190:330, 200:470] = 88,92, 255

# Cerobong (bawah dan tengah)
blank[130:190, 260:300] = 0,0,255
blank[100:130, 250:310] = (116,39,23)

# Cerobong atas
contours = np.array([[250,100], [310,100], [300,80],[260,80]])
cv.drawContours(blank, [contours], 0, (177, 230, 147), -1)

# Membuat roda
# Roda yang besar
cv.circle(blank, (555,350), 60, (0,0,0), thickness=-1)
cv.circle(blank, (555,350), 40, (198, 198, 200), thickness=-1)

# Roda yang kecil
cv.circle(blank, (255,370), 40, (75, 57, 44), thickness=-1)
cv.circle(blank, (350,370), 40, (75, 57, 44), thickness=-1)

# Penghubung antar rodanya
cv.line(blank, (255, 370), (585,370), (255, 0, 255), thickness=5)

# Membuat moncong depan yang berbentuk segitiga
# Atur centernya
pt1 = (200, 190)
pt2 = (200, 330)
pt3 = (75, 330)

# Membuat titik-titik koordinatnya
cv.circle(blank, pt1, 1, (0,255,0), -1)
cv.circle(blank, pt2, 1, (0,255,0), -1)
cv.circle(blank, pt3, 1, (0,255,0), -1)

triangle_cnt = np.array( [pt1 ,pt2 ,pt3] )
cv.drawContours(blank, [triangle_cnt], 0, (177, 230, 147), -1)

#memberikan tulisan nama
text = 'Herlambang Kurniawan'
cv.putText(blank,text, (270,460), cv.FONT_HERSHEY_DUPLEX,1.0, (255,0,0), 1)

# cv.add(blank,stiker)
cv.imshow('Kereta Sepur Mini', blank)
cv.waitKey(0)
