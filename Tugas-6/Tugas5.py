from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
import os
from ttkbootstrap import Style
from tkinter import ttk
np.seterr(divide='ignore', invalid='ignore')

class Window_1:
    def __init__(self, window_def = None):
        if window_def is None :
            pass
        else :
            window_def.destroy()

        self.window = Tk()
        self.window.title("Image Browse App - 5200411434")
        self.window.geometry("1295x700+25+25")
        self.window.config(bg="#323232")
        style = Style(theme='darkly')

    # MEMBUAT LEFT , MIDDLE , RIGHT FRAME
        self.left_frame  = Frame(self.window, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5,sticky='n')

        self.middle_frame = Frame(self.window, width=600, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5,sticky='n')

        self.right_frame = Frame(self.window, width=100, height=550, bg='#222222')
        self.right_frame.grid(row=0, column=2, padx=5, pady=15,sticky='n')

    # BAGIAN LEFTFRAME
        self.gambar = Label(self.left_frame,height=13,width=25)
        self.gambar.grid(row=0,column=0,pady=20)
    #===========================================================================================================================
        self.tool_bar = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        ttk.Style().configure('Outline.TButton',bordercolor="none",foreground="white",background="#2F8886",width=15, font=('Helvetica',10))
        self.icon_picture = PhotoImage(file="resources/icon/picture_icon.png")
        self.search = ttk.Button(self.tool_bar,text="  Image Browser",image=self.icon_picture,style="Outline.TButton",command=self.show_image,compound="left")
        self.search.grid(row=0, column=0, padx=5, pady=10,ipadx=5)

    #===========================================================================================================================
        self.tool_bar_2 = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar_2,image=self.icon_filter,text="Filter",compound='left',bg="#FD7014")
        self.filter.grid(row=0,column=0,ipadx=55,columnspan=2)

        ttk.Style().configure('info.TRadiobutton', background="#3f3f3f", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_2,text="Grayscale",value=1,style='info.TRadiobutton',command=self.rgb_to_grayscale)
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')

        self.btn_to_blue = ttk.Radiobutton(self.tool_bar_2, text="Blue Channel", value=2, style='info.TRadiobutton',command=lambda:self.take_channel("blue"))
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        self.btn_to_normal = ttk.Radiobutton(self.tool_bar_2, text="Original",value=3,style='info.TRadiobutton',command=self.img_to_normal)
        self.btn_to_normal.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        self.btn_to_green = ttk.Radiobutton(self.tool_bar_2, text="Green Channel", value=4, style='info.TRadiobutton',command=lambda:self.take_channel("green"))
        self.btn_to_green.grid(row=2, column=1, padx=25, pady=10, sticky='w')

        self.btn_negative = ttk.Radiobutton(self.tool_bar_2, text="Negative Image",value=5,style='info.TRadiobutton',command=self.image_negative)
        self.btn_negative.grid(row=3, column=0, pady=10, padx=25, sticky='w')

        self.btn_to_green = ttk.Radiobutton(self.tool_bar_2, text="Red Channel", value=6, style='info.TRadiobutton',command=lambda:self.take_channel("red"))
        self.btn_to_green.grid(row=3, column=1, padx=25, pady=10, sticky='w')


    #===========================================================================================================================
        self.tool_bar_3 = Frame(self.left_frame, width=180, height=200, bg="#323232")
        self.tool_bar_3.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.icon_menu = PhotoImage(file="resources/icon/menu_icon.png")
        self.btn_window_2 = Button(self.tool_bar_3,image=self.icon_menu, text="  MENU 2",height=40,width=180,compound='left',anchor='w', bd=0, bg="#11BFAE", relief="solid",command=lambda:Window_2(self.window))
        self.btn_window_2.grid(row=4, column=0,pady=5, sticky='w')

        self.icon_exit = PhotoImage(file="resources/icon/exit_icon.png")
        self.btn_exit = Button(self.tool_bar_3,image=self.icon_exit, text="  EXIT", bd=0,height=40,width=180, bg="#da4453",anchor='w', relief="solid",compound='left',command=lambda: exit())
        self.btn_exit.grid(row=5, column=0,pady=5, sticky='w')

    # BAGIAN RIGHT FRAME BAWAH ATAU DI DALEM RIGHT FRAME
        self.inside_right_frame = Frame(self.right_frame, width=300, height=200,bg="#222222")
        self.inside_right_frame.grid(row=0, column=0, padx=1, pady=5, sticky='n')

    # MEMBUAT SLIDER THRESHOLD
        self.label_treshold = Label(self.inside_right_frame, text="Treshold", width=10, height=1, bd=0, bg="#5ea880",relief="solid")
        self.label_treshold.grid(row=0, column=0, pady=4, sticky='n',ipady=3)

        current_value = IntVar()
        self.scale = ttk.Scale(self.inside_right_frame,variable=current_value, from_=0, to=255, orient=HORIZONTAL, length=250,style="success.Horizontal.TScale"
                               ,command=self.treshold)
        self.scale.grid(row=1, column=0, pady=4, sticky='w')

    # MEMBUAT NILAI SLIDER ADA DI POSISI BERAPA
        self.label_parameter = Label(self.inside_right_frame, text="0")
        self.label_parameter.grid(row=1, column=1, pady=4, sticky='w')
# ============================================================================================================
    # MEMBUAT SLIDER MULTIPLY
        self.label_multiply = Label(self.inside_right_frame, text="Multiply", width=10, height=1, bd=0, bg="#e74c3c",relief="solid")
        self.label_multiply.grid(row=2, column=0, pady=4, sticky='n',ipady=3)

        current_value_multiply = IntVar()
        self.scale_multiply = ttk.Scale(self.inside_right_frame, from_=0, to=5, orient=HORIZONTAL,length=250,style="danger.Horizontal.TScale",variable=current_value_multiply,command=self.multiply)
        self.scale_multiply.grid(row=3, column=0, pady=4, sticky='w')

        # MEMBUAT NILAI SLIDER ADA DI POSISI BERAPA
        self.label_parameter_multiply = Label(self.inside_right_frame, text="0")
        self.label_parameter_multiply.grid(row=3, column=1, pady=4, sticky='w')
# ============================================================================================================
        # MEMBUAT SLIDER DEVIDE
        self.label_devide = Label(self.inside_right_frame, text="Devide", width=10, height=1, bd=0, bg="#3498db",relief="solid")
        self.label_devide.grid(row=4, column=0, pady=4, sticky='n',ipady=3)

        current_value_devided = IntVar()
        self.scale_devide = ttk.Scale(self.inside_right_frame, from_=0, to=5, orient=HORIZONTAL, length=250,style="info.Horizontal.TScale", variable=current_value_devided,command=self.devided)
        self.scale_devide.grid(row=5, column=0, pady=4, sticky='w')

        # MEMBUAT NILAI SLIDER ADA DI POSISI BERAPA
        self.label_parameter_devided = Label(self.inside_right_frame, text="0")
        self.label_parameter_devided.grid(row=5, column=1, pady=4, sticky='w')
# ============================================================================================================

    # BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
        self.image = Image.open("resources/noimage.jpg")

    # image preview sebelah kiri
        self.image_l = self.image.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar = Label(self.left_frame, image=self.image_l)
        self.gambar.grid(row=0, column=0, padx=5, pady=20)

    # image preview  tengah
        self.image_r = self.image.resize((650, 500), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=10)


    def show_image(self):
        self.fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                              filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                              ("All Files", "*.*")))

        self.file_location = np.copy(self.fln)
        self.image = Image.open(self.fln)
        self.mini_preview_ori(self.image)
        self.preview_img(self.image)

    def mini_preview_ori(self,image):
        self.image_l = image.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar_1 = Label(self.left_frame,image=self.image_l)
        self.gambar_1.grid(row=0, column=0, pady=20)

    def preview_img(self,image):
        self.image_r = image.resize((650, 500), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=10)

    def img_to_normal(self):
        img = Image.open(self.fln)

        self.scale.set(0)
        self.label_parameter.config(text='0')

        self.scale_multiply.set(0)
        self.label_parameter_multiply.config(text='0')

        self.scale_devide.set(0)
        self.label_parameter_devided.config(text='0')

        self.preview_img(img)

    def take_channel(self,color):
        img = cv.imread(str(self.file_location))
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        (R,G,B) = cv.split(img_rgb)
        if color == "red":
            R = Image.fromarray(R)
            self.preview_img(R)
        elif color == "green":
            G = Image.fromarray(G)
            self.preview_img(G)
        elif color == "blue":
            B = Image.fromarray(B)
            self.preview_img(B)

    def rgb_to_grayscale(self):
        self.img = cv.imread(str(self.file_location))
        grayscale = np.zeros(self.img.shape)

        R = self.img[:, :, 0]
        G = self.img[:, :, 1]
        B = self.img[:, :, 2]

        R = R * 0.299
        G = G * 0.587
        B = B * 0.114

        total = R + G + B
        grayscale = self.img.copy()

        for i in range(3):
            grayscale[:, :, i] = total

        gray = Image.fromarray(grayscale)
        self.preview_img(gray)

    def treshold(self,event):
        try:
            self.label_parameter.config(text=str(int(self.scale.get())))
            img = cv.imread(str(self.file_location), 0)
            treshold = np.zeros(img.shape)

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    pixel = img[i, j]
                    if pixel < int(self.scale.get()):
                        treshold[i, j] = 0 * 255
                    else:
                        treshold[i, j] = 1 * 255

            tresh_img = Image.fromarray(treshold)
            self.preview_img(tresh_img)
        except:
            pass

    def image_negative(self):
        img_bgr = cv.imread(self.fln)
        img_rgb = cv.cvtColor(img_bgr,cv.COLOR_BGR2RGB)
        img_neg = 1 - img_rgb
        img_negative = Image.fromarray(img_neg)
        self.preview_img(img_negative)

    def multiply(self,event):
        try:
            self.label_parameter_multiply.config(text=f'{(self.scale_multiply.get()):.2f}')

            img = cv.imread(str(self.file_location))
            img_multiply = img * self.scale_multiply.get()
            cv.imwrite('target.jpg', img_multiply)

            img = cv.imread('target.jpg')
            img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)
        except:
            pass

    def devided(self,event):
        try:
            self.label_parameter_devided.config(text=f'{(self.scale_devide.get()):.2f}')

            img = cv.imread(str(self.file_location))
            img_devided = img / self.scale_devide.get()
            cv.imwrite('target.jpg', img_devided)

            img = cv.imread('target.jpg')
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)
        except:
            pass

class Window_2:
    def __init__(self,window):
        window.destroy()
        self.window_2 = Tk()
        self.window_2.title("Image Browse App - 5200411434")
        self.window_2.geometry("1200x700+25+25")
        style = Style(theme='darkly')

    # MEMBUAT FRAME
        self.left_frame = Frame(self.window_2, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')

        self.middle_frame = Frame(self.window_2, width=700, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=20, pady=15)

        self.right_frame = Frame(self.window_2,width=525, height=550,bg='#323232')
        self.right_frame.grid(row=0,column=2, padx=15, pady=15)
    # MEMBUAT TOOLBARS
        self.tool_bar = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar.grid(row=1, column=0, padx=17, pady=20, sticky='w')

    # MEMBUAT BUTTON UNTUK KEMBALI KE WINDOWS SEBELUMNYA
        self.search = Button(self.tool_bar, text="MENU 1", width=20, height=2, bd=0, bg="#ff7043", relief="solid",command=lambda:Window_1(self.window_2))
        self.search.grid(row=0, column=0, padx=15, pady=10)

        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar, image=self.icon_filter, text="Filter", compound='left', bg="#FD7014")
        self.filter.grid(row=1, column=0, ipadx=55, columnspan=2)

        ttk.Style().configure('info.TRadiobutton', background="#3f3f3f", foreground='white', font=('Helvetica', 8))
        self.rad_penjumlahan = ttk.Radiobutton(self.tool_bar, text="Penjumlahan", value=1, style='info.TRadiobutton',command=self.penjumlahan)
        self.rad_penjumlahan.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.rad_pengurangan = ttk.Radiobutton(self.tool_bar, text="Pengurangan", value=2, style='info.TRadiobutton',command=self.pengurangan)
        self.rad_pengurangan.grid(row=3, column=0,padx=10, pady=10, sticky='w')
        # MEMBUAT BUTTON EXIT
        self.btn_exit = Button(self.tool_bar, text="Exit", width=20, height=2, bd=0, bg="#da4453", relief="solid",command=lambda: exit())
        self.btn_exit.grid(row=4, column=0, pady=10, padx=15)

    # MEMBUAT INPUTAN UNTUK GAMBAR
        self.image = Image.open("resources/noimage.jpg")

        # image preview sebelah kiri
        self.image_tengah = self.image.resize((300, 300), Image.ANTIALIAS)
        self.image_tengah = ImageTk.PhotoImage(self.image_tengah)

        self.gambar_1 = Label(self.middle_frame,image=self.image_tengah)
        self.gambar_1.grid(row=0,column=0,pady=10)
        self.gambar_1.bind('<Double 1>', lambda event:self.show_image(urutan=self.gambar_1))

        self.gambar_2 = Label(self.middle_frame, image=self.image_tengah)
        self.gambar_2.grid(row=1, column=0,pady=10)
        self.gambar_2.bind('<Double 1>', lambda event:self.show_image(urutan = self.gambar_2))

        self.image_kanan = self.image.resize((525, 500), Image.ANTIALIAS)
        self.image_kanan = ImageTk.PhotoImage(self.image_kanan)
        self.gambar_3 = Label(self.right_frame,image=self.image_kanan)
        self.gambar_3.grid(row=0, column=0, pady=10)

    def show_image(self,urutan):
        if urutan == self.gambar_1:
            self.fln_1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                              filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                         ("All Files", "*.*")))
            image = Image.open(self.fln_1)
        elif urutan == self.gambar_2:
            self.fln_2 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                                    filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                               ("All Files", "*.*")))
            image = Image.open(self.fln_2)
        # self.file_location = np.copy(self.fln)

        image_l = image.resize((300, 300), Image.ANTIALIAS)
        image_l = ImageTk.PhotoImage(image_l)
        urutan.config(image=image_l)
        urutan.image = image_l

    def penjumlahan(self):
    # MEMINDAI LOKASI GAMBAR 1 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_1 = cv.imread(self.fln_1)
        img_1 = cv.resize(img_1, (300,300), interpolation=cv.INTER_AREA)
    # MEMINDAI LOKASI GAMBAR 2 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_2 = cv.imread(self.fln_2)
        img_2 = cv.resize(img_2, (300, 300), interpolation=cv.INTER_AREA)
    # MENJUMLAHKAN NILAI PIXEL ATAU MATRIK YANG ADA PADA GAMBAR 1 DAN GAMBAR 2
        new_img = img_1 + img_2

        new_img = Image.fromarray(new_img)
        self.preview(new_img)

    def pengurangan(self):
        # MEMINDAI LOKASI GAMBAR 1 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_1 = cv.imread(self.fln_1)
        img_1 = cv.resize(img_1, (300, 300), interpolation=cv.INTER_AREA)
        # MEMINDAI LOKASI GAMBAR 2 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_2 = cv.imread(self.fln_2)
        img_2 = cv.resize(img_2, (300, 300), interpolation=cv.INTER_AREA)
        # MENJUMLAHKAN NILAI PIXEL ATAU MATRIK YANG ADA PADA GAMBAR 1 DAN GAMBAR 2
        new_img = img_1 - img_2

        new_img = Image.fromarray(new_img)
        self.preview(new_img)

    def preview(self,image):
        image_new = image.resize((525, 500), Image.ANTIALIAS)
        image_new = ImageTk.PhotoImage(image_new)

        self.gambar_3.config(image=image_new)
        self.gambar_3.image = image_new


main_window = Window_1()
main_window.window.mainloop()

# MENGHAPUS FILE GAMBAR JIKA ADA
try:
    os.remove("target.jpg")
except:
    exit()
