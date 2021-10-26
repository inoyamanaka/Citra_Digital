from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
import os
from ttkbootstrap import Style

root = Tk()
root.title("Image Browse App - 5200411434")
root.geometry("875x620")
root.config(bg="#323232")
style = Style(theme='darkly')

file_location=""

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
    original_image = image.resize((185, 185), Image.ANTIALIAS)
    photoImg_ori = ImageTk.PhotoImage(original_image)
    Label(left_frame, image=photoImg_ori).grid(row=1, column=0, padx=5, pady=5)
    display.configure(image=photoImg_ori)
    display.image = photoImg_ori

def preview_img(image):
    img_resize = image.resize((560, 475), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img_resize)
    Label(right_frame, image=photoImg).grid(row=1, column=0, padx=5, pady=20)
    display2.configure(image=photoImg)
    display2.image = photoImg

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

   hold = treshold.copy()
   tresh_img = Image.fromarray(hold)
   preview_img(tresh_img)

# MEMBUAT LEFT DAN RIGHT FRAME
left_frame = Frame(root, width=200, height=600, bg='#323232')
left_frame.grid(row=0, column=0, padx=10, pady=5,sticky ='n')
right_frame = Frame(root, width=650, height=400, bg='#323232')
right_frame.grid(row=0, column=1, padx=10, pady=5)

display = Label(left_frame)
display2 = Label(right_frame)

# BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
if file_location == "":
    image = Image.open("resources/noimage.jpg")
    # image di sebelah kiri
    mini_preview_ori(image)
    # image di sebelah kanan
    preview_img(image)

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

label_treshold = Label(right_frame,text="Treshold",width=15,height=2,bd=0,bg="#5ea880",relief="solid",)
label_treshold.grid(row=2, column=0,pady=4,sticky ='w')

# BAGIAN RIGHT FRAME BAWAH ATAU DI DALEM RIGHT FRAME
inside_right_frame = Frame(right_frame,width=180, height=20)
inside_right_frame.grid(row=3, column=0, padx=1, pady=5,sticky ='w')

# MEMBUAT SLIDER
scale = Scale(inside_right_frame,from_=0,to=255,orient=HORIZONTAL,length=255,bg="#5ea880",activebackground="#00c851",command=treshold)
scale.grid(row=0, column=0,pady=4,sticky ='w')

# MEMBUAT NILAI SLIDER ADA DI POSISI BERAPA
label_parameter = Label(inside_right_frame,text="0")
label_parameter.grid(row=0, column=1,pady=4,sticky ='w')

root.mainloop()
