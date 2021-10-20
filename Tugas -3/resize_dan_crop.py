import cv2 as cv
import matplotlib.pyplot as plt

# Gambar Original
img = cv.imread("resources/soccer_kid_large.jpg")
image_rgb = cv.cvtColor(img ,cv.COLOR_BGR2RGB)

# Resize Gambar
scala = 0.6
width = int(scala * image_rgb.shape[1])
height = int(scala * image_rgb.shape[0])
dimension = (width ,height)

resize_img = cv.resize(image_rgb,dimension ,interpolation=cv.INTER_BITS)

# Menyimpan hasil resized ke file baru
cv.imwrite("resources/soccer_kid_small.jpg" ,cv.cvtColor(resize_img ,cv.COLOR_BGR2RGB))

# Menampilkan Dimensi Gambar
print(f'Dimensi Foto Sebelum Dikecilkan 60% : {image_rgb.shape}')
print(f'Dimensi Foto Sesudah Dikecilkan 60% : {resize_img.shape}')

# Menampilkan Gambar Menggunakan Pyplot
plt.subplot(1, 2, 1)
plt.title("Before")
plt.imshow(image_rgb)

plt.subplot(1, 2, 2)
plt.title("After")
plt.imshow(resize_img)

plt.show()

# menggandakan Object bola
bola = resize_img[748:862 ,782:898]
print("bola" ,bola.shape)
print('resize',resize_img.shape)

# menempelkan bola pada gambar soccer_kid_small
resize_img[788:902 ,58:174] = bola
plt.title("Bola Ganda")

# menambahkan nama
cv.putText(resize_img ,"5200411434" ,(1011,860) ,cv.FONT_ITALIC ,2.0, (255,0,0), 3)
plt.imshow(resize_img)
plt.show()

# menyimpan file doubleBall
cv.imwrite("resources/soccer_kid_small_doubleBall.jpg" ,cv.cvtColor(resize_img ,cv.COLOR_BGR2RGB))
