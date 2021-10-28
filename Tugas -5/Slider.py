from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
import os
from ttkbootstrap import Style

def show_image():
    global file_location
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                     filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                ("All Files", "*.*")))

    file_location = np.copy(fln)
    image = Image.open(fln)
    mini_preview_ori(image)
    preview_img(image)

def mini_preview_ori(image):
    global image_l
    image_l = image.resize((185, 185), Image.ANTIALIAS)
    image_l = ImageTk.PhotoImage(image_l)
    Label(left_frame, image=image_l).grid(row=0, column=0, padx=5, pady=20)

def preview_img(image):
    global image_r
    image_r = image.resize((560, 475), Image.ANTIALIAS)
    image_r = ImageTk.PhotoImage(image_r)
    Label(right_frame, image=image_r).grid(row=0, column=0, padx=5, pady=20)

def img_to_normal():
    img = Image.open(str(file_location))
    preview_img(img)

def rgb_to_grayscale():
    img = cv.imread(str(file_location))
    grayscale = np.zeros(img.shape)

    R = img[:,:,0]
    G = img[:,:,1]
    B = img[:,:,2]

    R = R * 0.299
    G = G * 0.587
    B = B * 0.114

    total = R+G+B
    grayscale = img.copy()

    for i in range(3):
        grayscale[:,:,i] = total

    gray_img = grayscale.copy()
    gray = Image.fromarray(gray_img)
    preview_img(gray)

def treshold(var):
   label_parameter.config(text = str(var))
   img = cv.imread(str(file_location),0)
   treshold = np.zeros(img.shape)

   for i in range(img.shape[0]):
       for j in range(img.shape[1]):
           pixel = img[i, j]
           if pixel < int(var):
               treshold[i,j] = 0 * 255
           else:
               treshold[i, j] = 1 * 255

   tresh_img = Image.fromarray(treshold)
   preview_img(tresh_img)

# MEMBUAT WINDOW UNTUK MENAMPUNG WIDGET
window = Tk()
window.title("Image Browse App - 5200411434")
window.geometry("875x620")
window.config(bg="#323232")
style = Style(theme='darkly')
file_location=""

# MEMBUAT LEFT DAN RIGHT FRAME
left_frame = Frame(window, width=200, height=600, bg='#323232')
left_frame.grid(row=0, column=0, padx=10, pady=5,sticky ='n')
right_frame = Frame(window, width=650, height=400, bg='#323232')
right_frame.grid(row=0, column=1, padx=10, pady=5)

# BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
image = Image.open("resources/noimage.jpg")

image_l = image.resize((185, 185), Image.ANTIALIAS)
image_l = ImageTk.PhotoImage(image_l)
def_img_l = Label(left_frame,image=image_l)
def_img_l.grid(row=0, column=0, padx=5, pady=20)

image_r = image.resize((560, 475), Image.ANTIALIAS)
image_r = ImageTk.PhotoImage(image_r)
def_img_r = Label(right_frame,image=image_r)
def_img_r.grid(row=0, column=0, padx=5, pady=20)

# BAGIAN LEFTFRAME
tool_bar = Frame(left_frame, width=180, height=185,bg="#3f3f3f")
tool_bar.grid(row=2, column=0, padx=1, pady=5,sticky ='w')

search = Button(tool_bar, text="Browse Image",width=25,height=2,bd=0,bg="#ff7043",relief="solid", command=show_image)
search.grid(row=1, column=0,pady=20,padx=10, ipadx=5 )

btn_to_gray = Button(tool_bar, text="Grayscale",width=25,height=2,bd=0,bg="#78909c",relief="solid", command=rgb_to_grayscale)
btn_to_gray.grid(row=2, column=0,pady=20,padx=3, ipadx=5)

btn_to_normal = Button(tool_bar, text="Original",width=25,height=2,bd=0,bg="#4285f4",relief="solid", command=img_to_normal)
btn_to_normal.grid(row=3, column=0,pady=20,padx=3, ipadx=5)

btn_exit= Button(tool_bar, text="Exit",width=25,height=2,bd=0,bg="#da4453",relief="solid", command=lambda:exit())
btn_exit.grid(row=4, column=0,pady=20,padx=3, ipadx=5)

# BAGIAN RIGHT FRAME BAWAH ATAU DI DALEM RIGHT FRAME
label_treshold = Label(right_frame,text="Treshold",width=15,height=2,bd=0,bg="#5ea880",relief="solid",)
label_treshold.grid(row=1, column=0,pady=4,sticky ='w')

inside_right_frame = Frame(right_frame,width=180, height=20)
inside_right_frame.grid(row=2, column=0, padx=1, pady=5,sticky ='w')

# MEMBUAT SLIDER
scale = Scale(inside_right_frame,from_=0,to=255,orient=HORIZONTAL,length=255,bg="#5ea880",activebackground="#00c851",command=treshold)
scale.grid(row=0, column=0,pady=4,sticky ='w')

# MEMBUAT NILAI SLIDER ADA DI POSISI BERAPA
label_parameter = Label(inside_right_frame,text="0")
label_parameter.grid(row=0, column=1,pady=4,sticky ='w')

window.mainloop()
