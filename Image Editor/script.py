from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk, ImageDraw
import os
from ttkbootstrap import Style
from tkinter import ttk
import math


# MEMBUAT SEBUAH CLASS UNTUK WINDOWS_1
class Window_1:
    # MEMBUAT CONSTRUCTOR CLASSNYA
    def __init__(self, window_def=None):
        # MENGATUR AGARA KETIKA PARAMETER windows_def ITU TIDAK ADA MAKA PASS SAJA
        if window_def is None:
            pass
        # MENGATUR JIKA PARAMETER WINDOW_DEF ADA ISINYA MAKA DESTROY
        else:
            window_def.destroy()

        # MENGATUR SIZE DARI WINDOWNYA DAN STYLE DARI BOOSTRAPNYA
        self.window = Tk()
        self.window.title("Image Browse App - 5200411434")
        self.window.geometry("1335x720+25+25")
        self.window.config(bg="#323232")
        style = Style(theme='darkly')

        # MEMBUAT LEFT , MIDDLE , RIGHT FRAME
        self.left_frame = Frame(self.window, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')

        self.middle_frame = Frame(self.window, width=600, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')

        self.right_frame = Frame(self.window, width=100, height=550, bg='#222222')
        self.right_frame.grid(row=0, column=2, padx=5, pady=15, sticky='n')

        # BAGIAN LEFTFRAME AKAN DIBUAT PREVIEW GAMBAR DAN BUTTON BUAT MENGAMBIL GAMBAR DARI STORAGE ,FILTER ,MENU DAN EXIT
        self.gambar = Label(self.left_frame, height=13, width=25)
        self.gambar.grid(row=0, column=0, pady=0)

        # BUTTON AMBIL GAMBAR
        ttk.Style().configure('Outline.TButton', bordercolor="none", foreground="white", background="#2F8886", width=15,
                              font=('Helvetica', 10))
        self.icon_picture = PhotoImage(file="resources/icon/picture_icon.png")
        self.search = ttk.Button(self.left_frame, text="  Image Browser", image=self.icon_picture,
                                 style="Outline.TButton", command=self.get_image, compound="left")
        self.search.grid(row=1, column=0, padx=5, pady=0, ipadx=20)

        # create a new notebook
        self.tab = ttk.Notebook(self.left_frame)
        self.tab.grid(row=2, column=0, pady=20)

        # create a new frame
        self.frame1 = ttk.Frame(self.tab, width=275, height=280)
        self.frame2 = ttk.Frame(self.tab, width=275, height=280)
        self.frame3 = ttk.Frame(self.tab, width=275, height=280)
        self.frame4 = ttk.Frame(self.tab, width=275, height=280)
        self.frame5 = ttk.Frame(self.tab, width=275, height=280)

        # set the frame as a tab in the notebook
        self.tab.add(self.frame1, text='Filter 1 ')
        self.tab.add(self.frame2, text='Filter 2')
        self.tab.add(self.frame3, text='Filter 3')
        self.tab.add(self.frame4, text='Filter 4')
        self.tab.add(self.frame5, text='Filter 5 ')

        # RADIO BUTTON BUAT BAGIAN FILTERNYA
        self.tool_bar_1 = Frame(self.frame1, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar_1, image=self.icon_filter, text="Filter", compound='left', bg="#FD7014")
        self.filter.grid(row=0, column=0, ipadx=35, columnspan=2)

        # RB BAGIAN GRAYSCALE
        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_1, text="Grayscale", value=1, style='info.TRadiobutton',
                                           command=self.rgb_to_grayscale)
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')

        # RB BAGIAN BLUE CHANNEL
        self.btn_to_blue = ttk.Radiobutton(self.tool_bar_1, text="Blue Channel", value=2, style='info.TRadiobutton',
                                           command=lambda: self.take_channel("blue"))
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN ORIGINAL IMAGE
        self.btn_to_normal = ttk.Radiobutton(self.tool_bar_1, text="Original", value=3, style='info.TRadiobutton',
                                             command=self.img_to_normal)
        self.btn_to_normal.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN GREEN CHANNEL
        self.btn_to_green = ttk.Radiobutton(self.tool_bar_1, text="Green Channel", value=4, style='info.TRadiobutton',
                                            command=lambda: self.take_channel("green"))
        self.btn_to_green.grid(row=2, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN NEGATIVE IMAGE
        self.btn_negative = ttk.Radiobutton(self.tool_bar_1, text="Negative Image", value=5, style='info.TRadiobutton',
                                            command=self.image_negative)
        self.btn_negative.grid(row=3, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN RED CHANNEL
        self.btn_to_red = ttk.Radiobutton(self.tool_bar_1, text="Red Channel", value=6, style='info.TRadiobutton',
                                          command=lambda: self.take_channel("red"))
        self.btn_to_red.grid(row=3, column=1, padx=25, pady=10, sticky='w')

        # HISTOGRAM EQUALIZATION
        self.btn_to_red = ttk.Radiobutton(self.tool_bar_1, text="Histogram Equalize", value=6, style='info.TRadiobutton',
                                          command=lambda: self.take_channel("red"))
        self.btn_to_red.grid(row=4, column=0, padx=25, pady=10, sticky='w')

        # HISTOGRAM EQUALIZATION
        self.btn_to_red = ttk.Radiobutton(self.tool_bar_1, text="Soon", value=6,
                                          style='info.TRadiobutton',
                                          command=lambda: self.take_channel("red"))
        self.btn_to_red.grid(row=5, column=0, padx=25, pady=10, sticky='w')

        # HISTOGRAM EQUALIZATION
        self.btn_to_red = ttk.Radiobutton(self.tool_bar_1, text="Soon", value=6,
                                          style='info.TRadiobutton',
                                          command=lambda: self.take_channel("red"))
        self.btn_to_red.grid(row=6, column=0, padx=25, pady=10, sticky='w')

        # ====================================================================

        # RADIO BUTTON BUAT BAGIAN FILTERNYA
        self.tool_bar_2 = Frame(self.frame3, width=180, height=200, bg="#444444")
        self.tool_bar_2.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.icon_flip = PhotoImage(file="resources/icon/flip_icon.png")
        self.flip = Label(self.tool_bar_2, image=self.icon_flip, text=" Flip", compound='left', bg="#FD7014")
        self.flip.grid(row=0, column=0, ipadx=35, columnspan=2)

        # CB BUAT FLIP
        ttk.Style().configure('Squaretoggle.Toolbutton', background="#3f3f3f", font=('Helvetica', 10))
        self.on_horizontal = IntVar()
        self.on_vertical = IntVar()

        self.btn_to_hor = ttk.Checkbutton(self.tool_bar_2, onvalue=1, offvalue=0, text="Horizontal",
                                          variable=self.on_horizontal, style='success.Squaretoggle.Toolbutton',
                                          command=self.horizontal)
        self.btn_to_hor.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        self.btn_to_ver = ttk.Checkbutton(self.tool_bar_2, onvalue=1, offvalue=0, text="Vertical",
                                          variable=self.on_vertical, style='danger.Squaretoggle.Toolbutton',
                                          command=self.vertical)
        self.btn_to_ver.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        # ===========================================================================================================================
        # RADIO BUTTON BUAT BAGIAN FILTERNYA PADA TAB2
        self.tool_bar_3 = Frame(self.frame2, width=180, height=200, bg="#444444")
        self.tool_bar_3.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.icon_rotate = PhotoImage(file="resources/icon/rotation_icon.png")
        self.rotate = Label(self.tool_bar_3, image=self.icon_rotate, text=" Rotation", compound='left', bg="#FD7014")
        self.rotate.grid(row=0, column=0, ipadx=35, columnspan=2)

        rotate_var = IntVar()
        # Rotasi 90 Derajat
        self.btn_to_90 = ttk.Radiobutton(self.tool_bar_3, text="90 Derajat\t", value=7, style='info.TRadiobutton',
                                         command=lambda: self.rotated(90))
        self.btn_to_90.grid(row=1, column=0, pady=10, padx=25, sticky='w')

        # Rotasi 180 Derajat
        self.btn_to_180 = ttk.Radiobutton(self.tool_bar_3, text="180 Derajat", value=8, style='info.TRadiobutton',
                                          command=lambda: self.rotated(180))
        self.btn_to_180.grid(row=1, column=1, pady=10, padx=25, sticky='w')

        # Rotasi 270 Derajat
        self.btn_to_270 = ttk.Radiobutton(self.tool_bar_3, text="270 Derajat", value=9, style='info.TRadiobutton',
                                          command=lambda: self.rotated(270))
        self.btn_to_270.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        # Rotasi 360 Derajat
        self.btn_to_360 = ttk.Radiobutton(self.tool_bar_3, text="360 Derajat", value=10, style='info.TRadiobutton',
                                          command=lambda: self.rotated(360))
        self.btn_to_360.grid(row=2, column=1, pady=10, padx=25, sticky='w')

        # Costum angle
        self.tool_bar_3_1 = Frame(self.tool_bar_3, width=180, height=200, bg="#444444")
        self.tool_bar_3_1.grid(row=3, column=0, padx=10, pady=10,columnspan=2, sticky='w')

        self.costume_angle = ttk.Entry(self.tool_bar_3_1, style='info.TEntry')
        self.costume_angle.grid(row=0, column=0, sticky="w", padx=5)

        self.btn_angle = ttk.Button(self.tool_bar_3_1, text="Rotate", style='warning.Outline.TButton', width=6,
                                    command=lambda: self.rotated("costume"))
        self.btn_angle.grid(row=0, column=1, padx=5)

        # =======================================
        self.tool_bar_3_2 = Frame(self.frame2, width=180, height=200, bg="#444444")
        self.tool_bar_3_2.grid(row=2, column=0, padx=5, pady=10, ipadx=30,sticky='w')

        self.icon_translation = PhotoImage(file="resources/icon/rotation_icon.png")
        self.translation = Label(self.tool_bar_3_2, image=self.icon_rotate,width=75, text=" Translation", compound='left', bg="#FD7014")
        self.translation.grid(row=0, column=1, ipadx=35,padx=5,pady=3, columnspan=2,sticky="e")

        self.trans_width = ttk.Entry(self.tool_bar_3_2,text="width", style='info.TEntry',width=8)
        self.trans_width.insert(0, 'width')
        self.trans_width.grid(row=1, column=0, sticky="e", padx=5,pady=8)

        self.trans_height = ttk.Entry(self.tool_bar_3_2, style='info.TEntry', width=8)
        self.trans_height.insert(0, 'height')
        self.trans_height.grid(row=1, column=1, sticky="w", padx=2, pady=8)

        self.btn_trans = ttk.Button(self.tool_bar_3_2, text="Trans", style='warning.Outline.TButton', width=6,
                                    command=self.translation_img)
        self.btn_trans.grid(row=1, column=2, padx=1,sticky='e')

        # =========================================================================================================================================
        self.btn_to_save = ttk.Button(self.middle_frame, text="SAVE IMAGE", style='info.TButton', command=self.save)
        self.btn_to_save.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        # =========================================================================================================================================
        # MEMBUAT FRAME DI DALAM LEFT FRAME
        self.tool_bar_4 = Frame(self.left_frame, width=180, height=200, bg="#323232")
        self.tool_bar_4.grid(row=5, column=0, padx=10, pady=5, sticky='w')

        # BUTTON UNTUK GANTI MENU
        self.btn_window_2 = ttk.Button(self.tool_bar_4, text="MENU", width=20, style='success.Outline.TButton',
                                       command=lambda: Window_2(self.window))
        self.btn_window_2.grid(row=0, column=0, pady=5, padx=5)

        # BUTTON UNTUK EXIT
        self.btn_exit = ttk.Button(self.tool_bar_4, text="EXIT", width=20, style='danger.Outline.TButton',
                                   command=self.exit)
        self.btn_exit.grid(row=1, column=0, pady=5, padx=5)

        # ===================================================================================================
        # PADA BAGIAN RIGHT FRAME AKAN DIGUNAKAN UNTUK SLIDER THRESHOLD ,MULTIPLY DAN DIVIDE

        # MEMBUAT SLIDER THRESHOLD
        # LABEL THRESHOLD
        self.set_bar = PhotoImage(file="resources/icon/threshold_icon.png")
        self.label_treshold = Label(self.right_frame, image=self.set_bar, width=32, height=32, bd=0, relief="solid")
        self.label_treshold.grid(row=0, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value = 0
        self.scale = ttk.Scale(self.right_frame, variable=current_value, from_=0, to=255, orient=HORIZONTAL, length=250,
                               style="success.Horizontal.TScale", command=self.treshold)
        self.scale.grid(row=1, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter = Label(self.right_frame, text="0")
        self.label_parameter.grid(row=1, column=1, pady=4, sticky='w')

        # ============================================================================================================
        # MEMBUAT SLIDER MULTIPLY
        # LABEL MULTIPLY
        self.brightness = PhotoImage(file="resources/icon/brightness_icon.png")
        self.label_multiply = Label(self.right_frame, image=self.brightness, width=32, height=32, bd=0, relief="solid")
        self.label_multiply.grid(row=2, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value_multiply = IntVar()
        self.scale_multiply = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,
                                        style="danger.Horizontal.TScale", variable=current_value_multiply,
                                        command=self.multiply)
        self.scale_multiply.grid(row=3, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter_multiply = Label(self.right_frame, text="1.00")
        self.label_parameter_multiply.grid(row=3, column=1, pady=4, sticky='w')

        # ============================================================================================================
        # MEMBUAT SLIDER DIVIDE
        self.darkness = PhotoImage(file="resources/icon/darkness_icon.png")
        self.label_divide = Label(self.right_frame, image=self.darkness, width=32, height=32, bd=0, relief="solid")
        self.label_divide.grid(row=4, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value_divide = IntVar()
        self.scale_divide = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,
                                      style="info.Horizontal.TScale", variable=current_value_divide,
                                      command=self.divide)
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
        self.gambar.grid(row=0, column=0, padx=5, pady=5)

        # image preview  tengah
        self.image_r = self.image.resize((650, 600), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=10)

    # METHOD UNTUK MENGAMBIL GAMBAR
    def get_image(self):
        try:
            self.fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                                  filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                             ("All Files", "*.*")))
            self.file_location = np.copy(self.fln)
            self.image = Image.open(self.fln)
            self.image.save("output.png")
            self.mini_preview_ori(self.image)
            self.preview_img(self.image)
        except:
            pass

    # METHOD UNTUK MENAMPILKAN GAMBAR ORIGINAL
    def mini_preview_ori(self, image):
        self.image_l = image.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar_1 = Label(self.left_frame, image=self.image_l)
        self.gambar_1.grid(row=0, column=0, padx=5, pady=5)

    # METHOD UNTUK MENAMPILKAN GAMBAR HASIL FILTER
    def preview_img(self, image):
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

        self.on_vertical.set(0)
        self.on_horizontal.set(0)

        img.save("output.png")

        self.preview_img(img)

    # METHOD UNTUK FILTER GAMBAR YANG HANYA MENGAMBIL CHANNELL WARNA SAJA
    def take_channel(self, color):
        img = cv.imread(str(self.file_location))
        (B, G, R) = cv.split(img)
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
        self.img = cv.imread("output.png")
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
        gray.save("output.png")
        self.preview_img(gray)

    # MENTHOD UNTUK MENGUBAH NEGATIVE IMAGE
    def image_negative(self):
        img_bgr = cv.imread("output.png")
        img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
        img_neg = 255 - img_rgb
        img_negative = Image.fromarray(img_neg)
        img_negative.save("output.png")
        self.preview_img(img_negative)

    # METHOD UNTUK MENGATUR THRESHOLD
    def treshold(self, event):
        try:
            self.label_parameter.config(text=str(int(self.scale.get())))
            img = cv.imread("output.png", 0)
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
    def multiply(self, event):
        try:
            self.label_parameter_multiply.config(text=f'{(self.scale_multiply.get()):.2f}')

            img = cv.imread("output.png")
            img_multiply = img * self.scale_multiply.get()
            cv.imwrite('target.jpg', img_multiply)

            img = cv.imread('target.jpg')
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)
        except:
            pass

    # METHOD UNTUK MENGATUR DIVIDE
    def divide(self, event):
        try:
            self.label_parameter_divide.config(text=f'{(self.scale_divide.get()):.2f}')

            img = cv.imread("output.png")
            img_devided = img / self.scale_divide.get()
            cv.imwrite('target.jpg', img_devided)

            img = cv.imread('target.jpg')
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)
        except:
            pass

    def horizontal(self):
        if self.on_horizontal.get() == 0 or self.on_horizontal.get() == 1:
            if os.path.isfile("output.png"):
                location = "output.png"
            else:
                location = str(self.file_location)

            input_image = Image.open(location)
            input_pixels = input_image.load()

            # Create output image
            output_image = Image.new("RGB", input_image.size)
            draw = ImageDraw.Draw(output_image)

            for x in range(output_image.width):
                for y in range(output_image.height):
                    xp = input_image.height - x - 1
                    draw.point((x, y), input_pixels[xp, y])

            output_image.save("output.png")
            img_horizon = cv.imread('output.png')
            img = cv.cvtColor(img_horizon, cv.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.preview_img(img)

    def vertical(self):
        if self.on_vertical.get() == 0 or self.on_vertical.get() == 1:
            if os.path.isfile("output.png"):
                location = "output.png"
            else:
                location = str(self.file_location)
        input_image = Image.open(location)
        input_pixels = input_image.load()

        # Create output image
        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                yp = input_image.height - y - 1
                draw.point((x, y), input_pixels[x, yp])

        output_image.save("output.png")
        img_verti = cv.imread('output.png')
        img = cv.cvtColor(img_verti, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.preview_img(img)

    def rotated(self, angle):

        input_image = Image.open("output.png")

        if angle == "costume":
            angle = int(self.costume_angle.get())
            input_image = Image.open(str(self.file_location))

        input_pixels = input_image.load()

        # Create output image
        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)

        angle = math.radians(angle)
        center_x = input_image.width / 2
        center_y = input_image.height / 2

        for x in range(input_image.width):
            for y in range(input_image.height):
                # Compute coordinate in input image
                xp = int((x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x)
                yp = int((x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y)
                if 0 <= xp < input_image.width and 0 <= yp < input_image.height:
                    draw.point((x, y), input_pixels[xp, yp])

        output_image.save("output.png")
        img_rotate = cv.imread('output.png')
        img = cv.cvtColor(img_rotate, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.preview_img(img)

    def translation_img(self):
        src_img = cv.imread(str(self.file_location))
        shift_distance = (self.trans_width.get(), self.trans_height.get())

        h, w = src_img.shape[:2]
        x_distance = int(shift_distance[0])
        y_distance = int(shift_distance[1])

        ts_mat = np.array([[1, 0, x_distance], [0, 1, y_distance]])

        out_img = np.zeros(src_img.shape, dtype='u1')

        for i in range(h):
            for j in range(w):
                origin_x = j
                origin_y = i
                origin_xy = np.array([origin_x, origin_y, 1])

                new_xy = np.dot(ts_mat, origin_xy)
                new_x = new_xy[0]
                new_y = new_xy[1]

                if 0 < new_x < w and 0 < new_y < h:
                    out_img[new_y, new_x] = src_img[i, j]

        out_img = cv.cvtColor(out_img, cv.COLOR_BGR2RGB)
        output_image = Image.fromarray(out_img)
        output_image.save("output.png")
        img_trans = cv.imread('output.png')
        self.preview_img(output_image)

    def save(self):
        image = Image.open("output.png")
        files = [('PNG', '*.png'),
                 ('All Files', '*.*'),
                 ('JPG', '*.jpg')]
        file = filedialog.asksaveasfilename(initialdir="/", filetypes=files, defaultextension=files)
        image.save(file)

    def exit(self):
        # MENGHAPUS FILE GAMBAR HASIL DARI PENJUMLAHAN DAN PENGURANGAN CITRA JIKA ADA
        try:
            os.remove("output.png")
            os.remove("target.jpg")
            print("keluar dengan sukses")
        except:
            # print("Tidak ada gambar dengan nama itu")
            exit()
        exit()


# MEMBUAT SEBUAH CLASS UNTUK WINDOW ATAU MENU 2
class Window_2:
    # MEMBUAT CONSTRUCTOR
    def __init__(self, window):
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

        self.right_frame = Frame(self.window_2, width=525, height=550, bg='#323232')
        self.right_frame.grid(row=0, column=2, padx=15, pady=15)

        # MEMBUAT TOOLBARS
        self.tool_bar_2 = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=1, column=0, padx=10, pady=50, sticky='w')

        self.tool_bar_3 = Frame(self.left_frame, width=180, height=700, bg="#323232")
        self.tool_bar_3.grid(row=2, column=0, padx=17, pady=20, sticky='s')

        # MEMBUAT BUTTON UNTUK KEMBALI KE WINDOWS SEBELUMNYA
        self.menu = ttk.Button(self.left_frame, text="MENU", width=20, style='success.Outline.TButton',
                               command=lambda: Window_1(self.window_2))
        self.menu.grid(row=0, column=0, pady=15, padx=15, columnspan=2)
        # MEMBUAT RB UNTUK MELAKUKAN FILTER YAITU PENJUMLAHAN ATAU PENGURANGAN CITRA
        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar_2, image=self.icon_filter, text="Filter", compound='left', bg="#FD7014")
        self.filter.grid(row=0, column=0, ipadx=55, columnspan=2)
        # PENJUMLAHAN
        ttk.Style().configure('info.TRadiobutton', background="#3f3f3f", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_2, text="Penjumlahan", value=1, style='info.TRadiobutton',
                                           command=self.penjumlahan)
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')
        # PENGURANGAN
        self.btn_to_blue = ttk.Radiobutton(self.tool_bar_2, text="Pengurangan", value=2, style='info.TRadiobutton',
                                           command=self.pengurangan)
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')
        # MEMBUAT BUTTON EXIT
        self.btn_exit = ttk.Button(self.tool_bar_3, text="EXIT", width=20, style='danger.Outline.TButton',
                                   command=lambda: exit())
        self.btn_exit.grid(row=4, column=0, pady=10, padx=15, sticky='s')

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
        self.gambar_1 = Label(self.middle_frame, image=self.image_raw)
        self.gambar_1.grid(row=0, column=0, pady=10)
        self.gambar_1.bind('<Double 1>', lambda event: self.show_image(self.gambar_1))

        # MEMBUAT LABEL UNTUK GAMBAR KEDUA
        self.gambar_2 = Label(self.middle_frame, image=self.image_raw)
        self.gambar_2.grid(row=1, column=0, pady=10)
        self.gambar_2.bind('<Double 1>', lambda event: self.show_image(self.gambar_2))

        # MEMBUAT LABEL UNTUK GAMBAR HASIL OPERASI
        self.gambar_3 = Label(self.right_frame, image=self.image_result)
        self.gambar_3.grid(row=0, column=0, pady=10)

    # MEMBUAT METHOD UNTUK MENGAMBIL GAMBAR DARI STORAGE DAN MENAMPILKANYA
    def show_image(self, urutan):
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
        img_1 = cv.resize(img_1, (275, 275), interpolation=cv.INTER_AREA)
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
    def preview(self, image):
        image_new = image.resize((525, 500), Image.ANTIALIAS)
        image_new = ImageTk.PhotoImage(image_new)

        self.gambar_3.config(image=image_new)
        self.gambar_3.image = image_new


# MEMBUAT SEBUAH OBJECT MAIN WINDOW
main_window = Window_1()
main_window.window.mainloop()
