from tkinter import *
from tkinter import filedialog
import tkinter.font as font
import os
import tkinter as tik
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np

file_location = ""

def showImage():
    global file_location
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                     filetypes=(("PNG Files", "*.png"),("JPG File", "*.jpg"),
                                                ("All Files", "*.*")))
    file_location = np.copy(fln)
    img = Image.open(fln)
    resized_image = img.resize((670, 480), Image.ANTIALIAS)
    resized_img = ImageTk.PhotoImage(resized_image)
    lbl.configure(image=resized_img)
    lbl.image = resized_img

def convert_opencv_to_tkinter(img):
    img_pill = Image.fromarray(img)
    resized_image = img_pill.resize((670, 480), Image.ANTIALIAS)
    img_tkinter = ImageTk.PhotoImage(resized_image)
    lbl.configure(image=img_tkinter)
    lbl.image = img_tkinter

def red_channel():
    img = cv.imread(str(file_location))
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    (R,G,B) = cv.split(img_rgb)
    convert_opencv_to_tkinter(R)

def green_channel():
    img = cv.imread(str(file_location))
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    (R, G, B) = cv.split(img_rgb)
    convert_opencv_to_tkinter(G)

def blue_channel():
    img = cv.imread(str(file_location))
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    (R, G, B) = cv.split(img_rgb)
    convert_opencv_to_tkinter(B)

def img_to_normal():
    img = cv.imread(str(file_location))
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    convert_opencv_to_tkinter(img_rgb)

def img_to_visual(color):
    img = cv.imread(str(file_location))
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if color == "red":
        img_rgb[:, :, 1] = 0
        img_rgb[:, :, 2] = 0
    elif color == "green":
        img_rgb[:, :, 0] = 0
        img_rgb[:, :, 2] = 0
    elif color == "blue":
        img_rgb[:, :, 0] = 0
        img_rgb[:, :, 1] = 0

    convert_opencv_to_tkinter(img_rgb)


# Membuat object dengan class Tk sehingga dihasilkan widget untuk menampung button ,img ,dll
root = Tk()
lbl = Label(root)
lbl.pack()

# Membuat frame untuk Button yang posisinya di bawah
frm = Frame(root)
frm.pack(side=BOTTOM, padx=0, pady=15)

# Membuat frame untuk Button yang posisinya di atasnya yang paling bawah
frm2 = Frame(root)
frm2.pack(side=BOTTOM,padx=15,pady=0)


# MEMBUAT BUTTON
buttonFont = font.Font(family='ARIAL LIGHT', size=8, weight='normal')

btn_search = PhotoImage(file='resources/search1.png')
btn_get_image = Button(frm2, image=btn_search,width="85",height="75",relief="solid",bd='1',bg="#40DAB2", command=showImage,font=buttonFont)
btn_get_image.pack(side=tik.LEFT)

btn_to_red = Button(frm2, text="RED CHANNEL",bg="#05193C",width="15",relief="solid", command=red_channel,font=buttonFont,fg="white")
btn_to_red.pack(side=tik.LEFT,padx=20)

btn_to_green = Button(frm2, text="GREEN CHANNEL",bg="#05193C",width="15", command=green_channel,font=buttonFont,fg="white")
btn_to_green.pack(side=tik.LEFT,padx=20)

btn_to_blue = Button(frm2, text="BLUE CHANNEL",bg="#05193C",width="15", command=blue_channel,font=buttonFont,fg="white")
btn_to_blue.pack(side=tik.LEFT,padx=20)

btn_to_clear = Button(frm, text="ORIGINAL",bg="white",width="8",relief="solid", command=img_to_normal)
btn_to_clear.pack(side=tik.LEFT,padx=0)

btn_to_clear = Button(frm, text="R",bg="#FF2442",width="5",height='2',relief="solid", command=lambda:img_to_visual("red"))
btn_to_clear.pack(side=tik.LEFT,padx=10)
btn_to_clear = Button(frm, text="G",bg="#80ED99",width="5",height='2',relief="solid", command=lambda:img_to_visual("green"))
btn_to_clear.pack(side=tik.LEFT,padx=10)
btn_to_clear = Button(frm, text="B",bg="#3DB2FF",width="5",height='2',relief="solid", command=lambda:img_to_visual("blue"))
btn_to_clear.pack(side=tik.LEFT,padx=10)

exit_img = PhotoImage(file='resources/exit.png')
btn_exit = Button(frm2, image=exit_img,width="85",height="75",relief="solid",bg="#40DAB2", command=lambda: exit())
btn_exit.pack(side=tik.LEFT, padx=10)

# SET WINDOWS SIZE
root.title("Image Broser App-5200411434")
root.geometry("780x650")

root.mainloop()
