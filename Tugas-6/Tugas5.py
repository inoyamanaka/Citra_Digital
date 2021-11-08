from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
import os
from ttkbootstrap import Style
from tkinter import ttk

# MEMBUAT SEBUAH CLASS UNTUK WINDOWS_1
class Window_1:
    # MEMBUAT CONSTRUCTOR CLASSNYA
    def __init__(self, window_def = None):
        # MENGATUR AGARA KETIKA PARAMETER windows_def ITU TIDAK ADA MAKA PASS SAJA
        if window_def is None :
            pass
        # MENGATUR JIKA PARAMETER WINDOW_DEF ADA ISINYA MAKA DESTROY
        else :
            window_def.destroy()

        # MENGATUR SIZE DARI WINDOWNYA DAN STYLE DARI BOOSTRAPNYA
        self.window = Tk()
        self.window.title("Image Browse App - 5200411434")
        self.window.geometry("1305x650+25+25")
        self.window.config(bg="#323232")
        style = Style(theme='darkly')

    # MEMBUAT LEFT , MIDDLE , RIGHT FRAME
        self.left_frame  = Frame(self.window, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5,sticky='n')

        self.middle_frame = Frame(self.window, width=600, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5,sticky='n')

        self.right_frame = Frame(self.window, width=100, height=550, bg='#222222')
        self.right_frame.grid(row=0, column=2, padx=5, pady=15,sticky='n')

    # BAGIAN LEFTFRAME AKAN DIBUAT PREVIEW GAMBAR DAN BUTTON BUAT MENGAMBIL GAMBAR DARI STORAGE ,FILTER ,MENU DAN EXIT
        self.gambar = Label(self.left_frame,height=13,width=25)
        self.gambar.grid(row=0,column=0,pady=0)

        # BUTTON AMBIL GAMBAR
        ttk.Style().configure('Outline.TButton',bordercolor="none",foreground="white",background="#2F8886",width=15, font=('Helvetica',10))
        self.icon_picture = PhotoImage(file="resources/icon/picture_icon.png")
        self.search = ttk.Button(self.left_frame,text="  Image Browser",image=self.icon_picture,style="Outline.TButton",command=self.get_image,compound="left")
        self.search.grid(row=1, column=0, padx=5, pady=0,ipadx=20)

        # RADIO BUTTON BUAT BAGIAN FILTERNYA
        self.tool_bar_2 = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=2, column=0, padx=10, pady=50, sticky='w')

        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar_2,image=self.icon_filter,text="Filter",compound='left',bg="#FD7014")
        self.filter.grid(row=0,column=0,ipadx=55,columnspan=2)

        # RB BAGIAN GRAYSCALE
        ttk.Style().configure('info.TRadiobutton', background="#3f3f3f", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_2,text="Grayscale",value=1,style='info.TRadiobutton',command=self.rgb_to_grayscale)
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')

        # RB BAGIAN BLUE CHANNEL
        self.btn_to_blue = ttk.Radiobutton(self.tool_bar_2, text="Blue Channel", value=2, style='info.TRadiobutton',command=lambda:self.take_channel("blue"))
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN ORIGINAL IMAGE
        self.btn_to_normal = ttk.Radiobutton(self.tool_bar_2, text="Original",value=3,style='info.TRadiobutton',command=self.img_to_normal)
        self.btn_to_normal.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN GREEN CHANNEL
        self.btn_to_green = ttk.Radiobutton(self.tool_bar_2, text="Green Channel", value=4, style='info.TRadiobutton',command=lambda:self.take_channel("green"))
        self.btn_to_green.grid(row=2, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN NEGATIVE IMAGE
        self.btn_negative = ttk.Radiobutton(self.tool_bar_2, text="Negative Image",value=5,style='info.TRadiobutton',command=self.image_negative)
        self.btn_negative.grid(row=3, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN RED CHANNEL
        self.btn_to_red = ttk.Radiobutton(self.tool_bar_2, text="Red Channel", value=6, style='info.TRadiobutton',command=lambda:self.take_channel("red"))
        self.btn_to_red.grid(row=3, column=1, padx=25, pady=10, sticky='w')

    #===========================================================================================================================

        # MEMBUAT FRAME DI DALAM LEFT FRAME
        self.tool_bar_3 = Frame(self.left_frame, width=180, height=200, bg="#323232")
        self.tool_bar_3.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # BUTTON UNTUK GANTI MENU
        self.btn_window_2 = Button(self.tool_bar_3, text="MENU", width=20, height=2, bd=0, bg="#57CC99", relief="solid",command=lambda:Window_2(self.window))
        self.btn_window_2.grid(row=4, column=0,pady=5,padx=5)

        # BUTTON UNTUK EXIT
        self.btn_exit = Button(self.tool_bar_3, text="Exit", width=20, height=2, bd=0, bg="#da4453", relief="solid",command=lambda: exit())
        self.btn_exit.grid(row=5, column=0, pady=5, padx=5)

#===================================================================================================
    # PADA BAGIAN RIGHT FRAME AKAN DIGUNAKAN UNTUK SLIDER THRESHOLD ,MULTIPLY DAN DIVIDE

    # MEMBUAT SLIDER THRESHOLD
        # LABEL THRESHOLD
        self.label_treshold = Label(self.right_frame, text="Treshold", width=10, height=1, bd=0, bg="#5ea880",relief="solid")
        self.label_treshold.grid(row=0, column=0, pady=4, sticky='n',ipady=3)

        # SLIDER
        current_value = 0
        self.scale = ttk.Scale(self.right_frame,variable=current_value, from_=0, to=255, orient=HORIZONTAL, length=250,style="success.Horizontal.TScale",command=self.treshold)
        self.scale.grid(row=1, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter = Label(self.right_frame, text="0")
        self.label_parameter.grid(row=1, column=1, pady=4, sticky='w')

# ============================================================================================================
    # MEMBUAT SLIDER MULTIPLY
        # LABEL MULTIPLY
        self.label_multiply = Label(self.right_frame, text="Multiply", width=10, height=1, bd=0, bg="#e74c3c",relief="solid")
        self.label_multiply.grid(row=2, column=0, pady=4, sticky='n',ipady=3)

        # SLIDER
        current_value_multiply = IntVar()
        self.scale_multiply = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL,length=250,style="danger.Horizontal.TScale",variable=current_value_multiply,command=self.multiply)
        self.scale_multiply.grid(row=3, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter_multiply = Label(self.right_frame, text="1.00")
        self.label_parameter_multiply.grid(row=3, column=1, pady=4, sticky='w')

# ============================================================================================================
        # MEMBUAT SLIDER DIVIDE
        self.label_divide = Label(self.right_frame, text="Divide", width=10, height=1, bd=0, bg="#3498db",relief="solid")
        self.label_divide.grid(row=4, column=0, pady=4, sticky='n',ipady=3)

        #SLIDER
        current_value_divide = IntVar()
        self.scale_divide = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,style="info.Horizontal.TScale", variable=current_value_divide,command=self.divide)
        self.scale_divide.grid(row=5, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter_divide = Label(self.right_frame, text="1.00")
        self.label_parameter_divide.grid(row=5, column=1, pady=4, sticky='w')
# ============================================================================================================

    # BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
        self.image = Image.open("resources/noimage.jpg")

    # image preview sebelah kiri
        self.image_l = self.image.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar = Label(self.left_frame, image=self.image_l)
        self.gambar.grid(row=0, column=0, padx=5, pady=0)

    # image preview  tengah
        self.image_r = self.image.resize((650, 600), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=10)


    # METHOD UNTUK MENGAMBIL GAMBAR
    def get_image(self):
        self.fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                              filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                              ("All Files", "*.*")))
        self.file_location = np.copy(self.fln)
        self.image = Image.open(self.fln)
        self.mini_preview_ori(self.image)
        self.preview_img(self.image)

    # METHOD UNTUK MENAMPILKAN GAMBAR ORIGINAL
    def mini_preview_ori(self,image):
        self.image_l = image.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar_1 = Label(self.left_frame,image=self.image_l)
        self.gambar_1.grid(row=0, column=0, pady=20)

    # METHOD UNTUK MENAMPILKAN GAMBAR HASIL FILTER
    def preview_img(self,image):
        self.image_r = image.resize((650, 600), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=10)

    # METHOD UNTUK MENGHILANGKAN SEMUA FILTER YANG ADA PADA GAMBAR
    def img_to_normal(self):
        img = Image.open(self.fln)

        self.scale.set(0)
        self.label_parameter.config(text='0')

        self.scale_multiply.set(0)
        self.label_parameter_multiply.config(text='1.00')

        self.scale_divide.set(0)
        self.label_parameter_divide.config(text='1.00')

        self.preview_img(img)

    # METHOD UNTUK FILTER GAMBAR YANG HANYA MENGAMBIL CHANNELL WARNA SAJA
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

    # METHOD UNTUK FILTER GRAYSCALE
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

    # MENTHOD UNTUK MENGUBAH NEGATIVE IMAGE
    def image_negative(self):
        img_bgr = cv.imread(self.fln)
        img_rgb = cv.cvtColor(img_bgr,cv.COLOR_BGR2RGB)
        img_neg = 255 - img_rgb
        img_negative = Image.fromarray(img_neg)
        self.preview_img(img_negative)

    # METHOD UNTUK MENGATUR THRESHOLD
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

    # METHOD UNTUK MENGATUR MULTIPLY
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

    # METHOD UNTUK MENGATUR DIVIDE
    def divide(self,event):
        try:
            self.label_parameter_divide.config(text=f'{(self.scale_divide.get()):.2f}')

            img = cv.imread(str(self.file_location))
            img_devided = img / self.scale_divide.get()
            cv.imwrite('target.jpg', img_devided)

            img = cv.imread('target.jpg')
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)
        except:
            pass

# MEMBUAT SEBUAH CLASS UNTUK WINDOW ATAU MENU 2
class Window_2:
# MEMBUAT CONSTRUCTOR
    def __init__(self,window):
    # MENGATUR UKURAN ATAU DIMENSI WINDOW
        window.destroy()
        self.window_2 = Tk()
        self.window_2.title("Image Browse App - 5200411434")
        self.window_2.geometry("1295x650+25+25")
        style = Style(theme='darkly')

    # MEMBUAT LEFT ,MIDDLE DAN RIGHT FRAME
        self.left_frame = Frame(self.window_2, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=15, pady=5)

        self.middle_frame = Frame(self.window_2, width=700, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=15, pady=15)

        self.right_frame = Frame(self.window_2,width=525, height=550,bg='#323232')
        self.right_frame.grid(row=0,column=2, padx=15, pady=15)

    # MEMBUAT TOOLBARS
        self.tool_bar_2 = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=1, column=0, padx=10, pady=50, sticky='w')

        self.tool_bar_3 = Frame(self.left_frame, width=180, height=700, bg="#323232")
        self.tool_bar_3.grid(row=2, column=0, padx=17, pady=20 ,sticky='s')

    # MEMBUAT BUTTON UNTUK KEMBALI KE WINDOWS SEBELUMNYA
        self.menu = Button(self.left_frame, text="MENU 1", width=20, height=2, bd=0, bg="#ff7043", relief="solid",command=lambda:Window_1(self.window_2))
        self.menu.grid(row=0, column=0, pady=15, padx=15, columnspan=2)
    # MEMBUAT RB UNTUK MELAKUKAN FILTER YAITU PENJUMLAHAN ATAU PENGURANGAN CITRA
        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar_2, image=self.icon_filter, text="Filter", compound='left', bg="#FD7014")
        self.filter.grid(row=0, column=0, ipadx=55, columnspan=2)
    # PENJUMLAHAN
        ttk.Style().configure('info.TRadiobutton', background="#3f3f3f", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_2, text="Penjumlahan", value=1, style='info.TRadiobutton',command=self.penjumlahan)
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')
    # PENGURANGAN
        self.btn_to_blue = ttk.Radiobutton(self.tool_bar_2, text="Pengurangan", value=2, style='info.TRadiobutton',command=self.pengurangan)
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')
    # MEMBUAT BUTTON EXIT
        self.btn_exit = Button(self.tool_bar_3, text="Exit", width=20, height=2, bd=0, bg="#da4453", relief="solid",command=lambda: exit())
        self.btn_exit.grid(row=4, column=0, pady=10, padx=15 ,sticky='s')

    # MEMBUAT INPUTAN UNTUK GAMBAR

        # MEMBACA ALAMAT GAMBAR
        img_ori = Image.open("resources/noimage.jpg")

        # MENGECILKANYA DENGAN UKURAN 275,275
        image_raw = img_ori.resize((275, 275), Image.ANTIALIAS)
        self.image_raw = ImageTk.PhotoImage(image_raw)

        # MEMBESARKAN DENGAN UKURAN 525,500
        image_result = img_ori.resize((525, 500), Image.ANTIALIAS)
        self.image_result = ImageTk.PhotoImage(image_result)

        # MEMBUAT LABEL UNTUK GAMBAR PERTAMA
        self.gambar_1 = Label(self.middle_frame,image=self.image_raw)
        self.gambar_1.grid(row=0,column=0,pady=10)
        self.gambar_1.bind('<Double 1>', lambda event:self.show_image(self.gambar_1))

        # MEMBUAT LABEL UNTUK GAMBAR KEDUA
        self.gambar_2 = Label(self.middle_frame, image=self.image_raw)
        self.gambar_2.grid(row=1, column=0,pady=10)
        self.gambar_2.bind('<Double 1>', lambda event:self.show_image(self.gambar_2))

        # MEMBUAT LABEL UNTUK GAMBAR HASIL OPERASI
        self.gambar_3 = Label(self.right_frame,image=self.image_result)
        self.gambar_3.grid(row=0, column=0, pady=10)

    # MEMBUAT METHOD UNTUK MENGAMBIL GAMBAR DARI STORAGE DAN MENAMPILKANYA
    def show_image(self,urutan):
        # JIKA GAMBAR PERTAMA DI DOUBLE CLICK
        if urutan == self.gambar_1:
            self.fln_1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                              filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                         ("All Files", "*.*")))
            image = Image.open(self.fln_1)

        # JIKA GAMBAR KEDUA DI DOUBLE CLICK
        elif urutan == self.gambar_2:
            self.fln_2 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                                    filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                               ("All Files", "*.*")))
            image = Image.open(self.fln_2)

    # MENGECILKAN GAMBAR DAN MENAMPILKANYA
        image_l = image.resize((275, 275), Image.ANTIALIAS)
        image_l = ImageTk.PhotoImage(image_l)
        urutan.config(image=image_l)
        urutan.show = image_l

    # MEMBUAT METHOD UNTUK MELAKUKAN PENJUMLAHAN CITRA
    def penjumlahan(self):
    # MEMINDAI LOKASI GAMBAR 1 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_1 = cv.imread(self.fln_1)
        img_1 = cv.resize(img_1, (275,275), interpolation=cv.INTER_AREA)
    # MEMINDAI LOKASI GAMBAR 2 DAN  MENYESUAIKAN DIMENSI GAMBARNYA
        img_2 = cv.imread(self.fln_2)
        img_2 = cv.resize(img_2, (275, 275), interpolation=cv.INTER_AREA)
    # MENJUMLAHKAN NILAI PIXEL ATAU MATRIK YANG ADA PADA GAMBAR 1 DAN GAMBAR 2
        new_img = img_1 + img_2
        new_img = Image.fromarray(new_img)
        self.preview(new_img)

    # MEMBUAT METHOD UNTUK MELAKUKAN PENGURANGAN CITRA
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

    # MENAMPILKAN GAMBAR HASIL PENJUMLAHAN / PENGURANGAN CITRA
    def preview(self,image):
        image_new = image.resize((525, 500), Image.ANTIALIAS)
        image_new = ImageTk.PhotoImage(image_new)

        self.gambar_3.config(image=image_new)
        self.gambar_3.image = image_new


# MEMBUAT SEBUAH OBJECT MAIN WINDOW
main_window = Window_1()
main_window.window.mainloop()

# MENGHAPUS FILE GAMBAR HASIL DARI PENJUMLAHAN DAN PENGURANGAN CITRA JIKA ADA
try:
    os.remove("target.jpg")
except:
    exit()
