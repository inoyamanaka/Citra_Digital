from tkinter import *
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk, ImageDraw ,ImageFilter
import os
from ttkbootstrap import Style
from tkinter import ttk
import math

class Filter:
    def __init__(self):
        pass

    def image_to_threshold(self,img,scale):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        _,treshold = cv.threshold(img,scale.get(), 255, cv.THRESH_BINARY)
        return treshold

    def image_to_bright(self,img,scale):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img = img * scale.get()
        return img

    def image_to_dark(self,img,scale):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img = img / scale.get()
        return img

    def image_to_gray(self,img):
        img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        return img

    def image_to_blue(self,img):
       return  img[:, :, 2]

    def image_to_green(self,img):
        return img[:, :, 1]

    def image_to_red(self,img):
        return img[:, :, 0]

    def image_to_hsv(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        return img

    def image_to_negative(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img_neg = 255 - img
        return img_neg

    def image_to_gaussian(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        figure_size = 9
        img = cv.GaussianBlur(img, (figure_size, figure_size),0)
        return img

    def image_to_edge_detection(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        mask = np.array([[-1, -1, -1],
                         [-1,  8, -1],
                         [-1, -1, -1]])

        img = cv.filter2D(src=img, ddepth=-1, kernel=mask)
        return  img

    def image_to_mean_filter(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        mask = np.ones((3,3),dtype=int)
        mask = mask / 9
        img = cv.filter2D(src=img, ddepth=-1, kernel=mask)
        return img

    def image_to_sharpen(self,img):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        mask = np.array([[0,-1,0],
                         [-1,5,-1],
                         [0,-1,0]])

        img = cv.filter2D(src=img, ddepth=-1, kernel=mask)
        return img

    def image_to_unsharp(self,img):
        # img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        image2 = Image.fromarray(img.astype('uint8'))
        new_image = image2.filter(ImageFilter.UnsharpMask(radius=2, percent=150))

        new_image.save("output.png")
        
           def image_to_canny(self,img):
        img = cv.Canny(img, 100, 200)
        return img

    def image_to_sobel(self,img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_gaussian = cv.GaussianBlur(gray, (3, 3), 0)

        img_sobelx = cv.Sobel(img_gaussian, cv.CV_8U, 1, 0, ksize=5)
        img_sobely = cv.Sobel(img_gaussian, cv.CV_8U, 0, 1, ksize=5)
        img_sobel = img_sobelx + img_sobely

        return img_sobel

    def image_to_prewitt(self,img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_gaussian = cv.GaussianBlur(gray, (3, 3), 0)

        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        img_prewittx = cv.filter2D(img_gaussian, -1, kernelx)
        img_prewitty = cv.filter2D(img_gaussian, -1, kernely)

        img_prewitt = img_prewittx + img_prewitty

        return img_prewitt

class Image_operation:
    def __int__(self):
        pass

    def image_to_rotated(self,img,angle):
        input_pixels = img.load()
        output_image = Image.new("RGB",size=img.size)
        draw = ImageDraw.Draw(output_image)

        angle = math.radians(angle)
        center_x = img.width / 2
        center_y = img.height / 2

        for x in range(img.width):
            for y in range(img.height):
                # Compute coordinate in input image
                xp = int((x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x)
                yp = int((x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y)
                if 0 <= xp < img.width and 0 <= yp < img.height:
                    draw.point((x, y), input_pixels[xp, yp])

        return output_image

    def image_to_flip_horizontal(self,img):
        input_pixels = img.load()
        output_image = Image.new("RGB", img.size)
        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                xp = img.height - x - 1
                draw.point((x, y), input_pixels[xp, y])

        return output_image

    def image_to_flip_vertical(self, img):
        input_pixels = img.load()

        output_image = Image.new("RGB", img.size)
        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                yp = img.height - y - 1
                draw.point((x, y), input_pixels[x, yp])

        return output_image

    def image_to_trans(self,img,d_width,d_height):
        src_img = cv.imread(img)
        h, w = src_img.shape[:2]

        x_distance = int(d_width)
        y_distance = int(d_height)

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

        return out_img



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
        self.window.geometry("1400x750+1+1")
        self.window.config(bg="#323232")
        style = Style(theme='darkly')

        self.filter_img = Filter()
        self.img_operation = Image_operation()

    # MEMBUAT LEFT , MIDDLE , RIGHT FRAME
        self.left_frame = Frame(self.window, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')

        self.middle_frame = Frame(self.window, width=800, height=600, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')

        self.right_frame = Frame(self.window, width=100, height=550, bg='#222222')
        self.right_frame.grid(row=0, column=2, padx=5, pady=15, sticky='n')

        # -------------------------- LEFT FRAME SECTION-----------------------#
        """DI BAWAH INI MERUPAKAN SOURCE UNTUK BAGIAN CODE YANG ADA 
           PADA MIDDLE FRAME ATAU FRAME TENGAH YANG MENCANGKUP
           - PREVIEW GAMBAR ORI VERSI KECIL
           - RADIO BUTTON FILTER BERUPA :
                1.  GRAYSCALE
                2.  RGB CHANNEL
                3.  ORIGINAL
                4.  NEGATIVE
                5.  HSV 
                6.  SHARPEN 
                7.  GAUSSIAN 
                8.  AVERAGE 
                9.  MEDIAN 
                10. UNSHARP
           - ROTATE IMAGE
           - TRANSLASI IMAGE
           - FLIP HORIZONTAL DAN FLIP VERIKAL
           - BUTTON GANTI MENU
           - BUTTON EXIT """
        # -------------------------- LEFT FRAME SECTION-----------------------#

    # LABEL UNTUK MENAMPUNG BUTTON SEARCH IMAGE
        self.gambar = Label(self.left_frame, height=13, width=25)
        self.gambar.grid(row=0, column=0, pady=0)

    # BUTTON AMBIL GAMBAR
        ttk.Style().configure('Outline.TButton', bordercolor="none", foreground="white", background="#2F8886", width=15,
                              font=('Helvetica', 10))
        self.icon_picture = PhotoImage(file="resources/icon/picture_icon.png")
        self.search = ttk.Button(self.left_frame, text="  Image Browser", image=self.icon_picture,
                                 style="Outline.TButton", command=self.get_image, compound="left")
        self.search.grid(row=1, column=0, padx=5, pady=0, ipadx=20)

    # MEMBUAT NOTEBOOK UNTUK MENAMPUNG TAB
        self.tab = ttk.Notebook(self.left_frame)
        self.tab.grid(row=2, column=0, pady=20)

        # MEMBUAT SEBUAH FRAME TAB
        self.frame1 = ttk.Frame(self.tab, width=275, height=280)
        self.frame2 = ttk.Frame(self.tab, width=275, height=280)
        self.frame3 = ttk.Frame(self.tab, width=275, height=280)
        self.frame4 = ttk.Frame(self.tab, width=275, height=280)
        self.frame5 = ttk.Frame(self.tab, width=275, height=280)

        # MENGATUR AGAR FRAMENYA MENJADI SEBUAH TAB DI NOTEBOOK
        self.tab.add(self.frame1, text='Filter 1 ')
        self.tab.add(self.frame2, text='Filter 2')
        self.tab.add(self.frame3, text='Filter 3')
        self.tab.add(self.frame4, text='Filter 4')
        self.tab.add(self.frame5, text='Filter 5 ')

# ==================================================================================================================#
# ============================================== LEFT FRAME TOOLBARS ===============================================#
# ==================================================================================================================#

    # MEMBUAT FRAME DI DALAM LEFT FRAME
        self.tool_bar_4 = Frame(self.left_frame, width=180, height=200, bg="#323232")
        self.tool_bar_4.grid(row=5, column=0, padx=10, pady=5, sticky='w')

    # BUTTON UNTUK GANTI KE VIDEO
        self.btn_window_2 = ttk.Button(self.tool_bar_4, text="VIDEO"
                                                             "", width=20, style='warning.Outline.TButton',
                                       command=lambda: Window_3(self.window))
        self.btn_window_2.grid(row=0, column=0, pady=3, padx=5)

    # BUTTON UNTUK GANTI MENU
        self.btn_window_2 = ttk.Button(self.tool_bar_4, text="MENU", width=20, style='success.Outline.TButton',
                                       command=lambda: Window_2(self.window))
        self.btn_window_2.grid(row=1, column=0, pady=3, padx=5)

    # BUTTON UNTUK EXIT
        self.btn_exit = ttk.Button(self.tool_bar_4, text="EXIT", width=20, style='danger.Outline.TButton',
                                   command=self.exit)
        self.btn_exit.grid(row=2, column=0, pady=3, padx=5)


#==================================================================================================================#
#==================================================== FILTER 1 ====================================================#
#==================================================================================================================#

        # RADIO BUTTON BUAT BAGIAN FILTERNYA

        # FRAME UNTUK MENAMPUNG RADIO BUTTON YANG BERISI FILTER
        self.tool_bar = Frame(self.frame1, width=180, height=200, bg="#3f3f3f")
        self.tool_bar.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter = Label(self.tool_bar, image=self.icon_filter, text="Filter", compound='left', bg="#FD7014")
        self.filter.grid(row=0, column=0, ipadx=35, columnspan=2)

        # RB BAGIAN GRAYSCALE
        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar, text="Grayscale", value=1, style='info.TRadiobutton',
                                           command=lambda:self.filter_apply("gray"))
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')

        # RB BAGIAN BLUE CHANNEL
        self.btn_to_blue = ttk.Radiobutton(self.tool_bar, text="Blue Channel", value=2, style='info.TRadiobutton',
                                           command=lambda:self.filter_apply("blue"))
        self.btn_to_blue.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN ORIGINAL IMAGE
        self.btn_to_normal = ttk.Radiobutton(self.tool_bar, text="Original", value=3, style='info.TRadiobutton',
                                             command=self.image_normal)
        self.btn_to_normal.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN GREEN CHANNEL
        self.btn_to_green = ttk.Radiobutton(self.tool_bar, text="Green Channel", value=4, style='info.TRadiobutton',
                                            command=lambda:self.filter_apply("green"))
        self.btn_to_green.grid(row=2, column=1, padx=25, pady=10, sticky='w')

        # RB BAGIAN NEGATIVE IMAGE
        self.btn_negative = ttk.Radiobutton(self.tool_bar, text="Negative Image", value=5, style='info.TRadiobutton',
                                            command=lambda:self.filter_apply("negative"))
        self.btn_negative.grid(row=3, column=0, pady=10, padx=25, sticky='w')

        # RB BAGIAN RED CHANNEL
        self.btn_to_red = ttk.Radiobutton(self.tool_bar, text="Red Channel", value=6, style='info.TRadiobutton',
                                          command=lambda:self.filter_apply("red"))
        self.btn_to_red.grid(row=3, column=1, padx=25, pady=10, sticky='w')

        # HSV
        self.btn_to_hsv = ttk.Radiobutton(self.tool_bar, text="HSV", value=9,
                                          style='info.TRadiobutton',
                                          command=lambda:self.filter_apply("hsv"))
        self.btn_to_hsv.grid(row=4, column=0, padx=25, pady=10, sticky='w')

        # SHARPEN FILTER
        self.btn_to_sharpen = ttk.Radiobutton(self.tool_bar, text="Sharpen Filter", value=7, style='info.TRadiobutton',
                                          command=lambda:self.filter_apply("sharpen"))
        self.btn_to_sharpen.grid(row=4, column=1, padx=25, pady=10, sticky='w')

        # MEDIAN FILTER
        self.btn_to_median = ttk.Radiobutton(self.tool_bar, text="Mean Filter", value=8,
                                          style='info.TRadiobutton',
                                          command=lambda:self.filter_apply("mean_filter"))
        self.btn_to_median.grid(row=5, column=0, padx=25, pady=10, sticky='w')


        # MEAN / AVERAGE FILTER
        self.btn_to_mean = ttk.Radiobutton(self.tool_bar, text="Edge Detection", value=10,
                                          style='info.TRadiobutton',
                                          command=lambda:self.filter_apply("edge_detection"))
        self.btn_to_mean.grid(row=5, column=1, padx=25, pady=10, sticky='w')

        # GAUSSIAN FILTER
        self.btn_to_gaussian = ttk.Radiobutton(self.tool_bar, text="Gaussian Blur", value=11,
                                          style='info.TRadiobutton',command=lambda:self.filter_apply("gaussian"))
        self.btn_to_gaussian.grid(row=6, column=0, padx=25, pady=10, sticky='w')

        # UNSHARP FILTER
        self.btn_to_unsharp = ttk.Radiobutton(self.tool_bar, text="Unsharp", value=12,
                                          style='info.TRadiobutton', command=lambda:self.filter_apply("unsharp"))
        self.btn_to_unsharp.grid(row=6, column=1, padx=25, pady=10, sticky='w')


# ==================================================================================================================#
# ==================================================== FILTER 2 ====================================================#
# ==================================================================================================================#
        # RADIO BUTTON BUAT BAGIAN FILTERNYA PADA TAB2

        # FRAME ATAS BUAT KONTEN ROTASI
        self.tool_bar_2_1 = Frame(self.frame2, width=180, height=200, bg="#444444")
        self.tool_bar_2_1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.icon_rotate = PhotoImage(file="resources/icon/rotation_icon.png")
        self.rotate = Label(self.tool_bar_2_1, image=self.icon_rotate, text=" Rotation", compound='left', bg="#FD7014")
        self.rotate.grid(row=0, column=0, ipadx=35, columnspan=2)

        rotate_var = IntVar()
        # Rotasi 90 Derajat
        self.btn_to_90 = ttk.Radiobutton(self.tool_bar_2_1, text="90 Derajat\t", value=7, style='info.TRadiobutton',
                                         command=lambda: self.operation_apply(90))
        self.btn_to_90.grid(row=1, column=0, pady=10, padx=25, sticky='w')

        # Rotasi 180 Derajat
        self.btn_to_180 = ttk.Radiobutton(self.tool_bar_2_1, text="180 Derajat", value=8, style='info.TRadiobutton',
                                          command=lambda: self.operation_apply(180))
        self.btn_to_180.grid(row=1, column=1, pady=10, padx=25, sticky='w')

        # Rotasi 270 Derajat
        self.btn_to_270 = ttk.Radiobutton(self.tool_bar_2_1, text="270 Derajat", value=9, style='info.TRadiobutton',
                                          command=lambda: self.operation_apply(270))
        self.btn_to_270.grid(row=2, column=0, pady=10, padx=25, sticky='w')

        # Rotasi 360 Derajat
        self.btn_to_360 = ttk.Radiobutton(self.tool_bar_2_1, text="360 Derajat", value=10, style='info.TRadiobutton',
                                          command=lambda: self.operation_apply(360))
        self.btn_to_360.grid(row=2, column=1, pady=10, padx=25, sticky='w')

        # COSTUME ANGLE
        self.costume_angle = ttk.Entry(self.tool_bar_2_1, style='info.TEntry')
        self.costume_angle.grid(row=3, column=0, sticky="w", padx=5)

        self.btn_angle = ttk.Button(self.tool_bar_2_1, text="Rotate", style='warning.Outline.TButton', width=6,
                                    command=lambda: self.operation_apply("custom"))
        self.btn_angle.grid(row=3, column=1, padx=5)

        # FRAME BAWAH BUAT KONTEN TRANSLASI
        self.tool_bar_2_2 = Frame(self.frame2, width=180, height=200, bg="#444444")
        self.tool_bar_2_2.grid(row=1, column=0, padx=5, pady=10, ipadx=30,sticky='w')

        self.icon_translation = PhotoImage(file="resources/icon/rotation_icon.png")
        self.translation = Label(self.tool_bar_2_2, image=self.icon_rotate,width=75, text=" Translation", compound='left', bg="#FD7014")
        self.translation.grid(row=0, column=1, ipadx=35,padx=5,pady=3, columnspan=2,sticky="e")

        self.trans_width = ttk.Entry(self.tool_bar_2_2,text="width", style='info.TEntry',width=8)
        self.trans_width.insert(0, 'width')
        self.trans_width.grid(row=1, column=0, sticky="e", padx=5,pady=8)

        self.trans_height = ttk.Entry(self.tool_bar_2_2, style='info.TEntry', width=8)
        self.trans_height.insert(0, 'height')
        self.trans_height.grid(row=1, column=1, sticky="w", padx=2, pady=8)

        self.btn_trans = ttk.Button(self.tool_bar_2_2, text="Trans", style='warning.Outline.TButton', width=6,
                                    command=lambda:self.operation_apply("translation"))
        self.btn_trans.grid(row=1, column=2, padx=1,sticky='e')

# ==================================================================================================================#
# ==================================================== FILTER 3 ====================================================#
# ==================================================================================================================#

        # RADIO BUTTON BUAT BAGIAN FILTERNYA

        # MEMBUAT FRAME UNTUK MENAMPUNG SESUATU YANG BERHUBUNGAN DENGAN FLIP
        self.tool_bar = Frame(self.frame3, width=180, height=200, bg="#444444")
        self.tool_bar.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.icon_flip = PhotoImage(file="resources/icon/flip_icon.png")
        self.flip = Label(self.tool_bar, image=self.icon_flip, text=" Flip", compound='left', bg="#FD7014")
        self.flip.grid(row=0, column=0, ipadx=35, columnspan=2)

        # CB BUAT FLIP
        ttk.Style().configure('Squaretoggle.Toolbutton', background="#3f3f3f", font=('Helvetica', 10))
        self.on_horizontal = IntVar()
        self.on_vertical = IntVar()

        self.btn_to_hor = ttk.Checkbutton(self.tool_bar, onvalue=1, offvalue=0, text="Horizontal",
                                          variable=self.on_horizontal, style='success.Squaretoggle.Toolbutton',
                                          command=lambda:self.operation_apply("horizontal"))
        self.btn_to_hor.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        self.btn_to_ver = ttk.Checkbutton(self.tool_bar, onvalue=1, offvalue=0, text="Vertical",
                                          variable=self.on_vertical, style='danger.Squaretoggle.Toolbutton',
                                          command=lambda:self.operation_apply("vertical"))
        self.btn_to_ver.grid(row=1, column=1, padx=25, pady=10, sticky='w')

#==================================================================================================================#
#==================================================== FILTER 4 ====================================================#
#==================================================================================================================#
        # SOON
        # self.tool_bar_frame_4 = Frame(self.frame4, width=180, height=200, bg="#444444")
        # self.tool_bar_frame_4.grid(row=2, column=0, padx=5, pady=10, ipadx=30,sticky='w')

#---------------------------------- MIDDLE FRAME SECTION ----------------------------------#
        """DI BAWAH INI MERUPAKAN SOURCE UNTUK BAGIAN CODE YANG ADA 
           PADA MIDDLE FRAME ATAU FRAME TENGAH YANG MENCANGKUP
           - PREVIEW GAMBAR
           - BUTTON SAVE
           - BUTTON COMPARE
           - BUTTON PREVIEW """
#---------------------------------- MIDDLE FRAME SECTION ----------------------------------#

    # FRAME UNTUK MENAMPUNG BUTTON
        self.tool_mid = Frame(self.middle_frame)
        self.tool_mid.grid(row=1, column=0, sticky='w', padx=5, pady=5)

    # MEMBUAT BUTTON UNTUK MENYIMPAN GAMBAR HASIL FILTER
        self.btn_to_save = ttk.Button(self.tool_mid, text="SAVE IMAGE", style='info.TButton', command=self.save)
        self.btn_to_save.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    # MEMBUAT BUTTON UNTUK MEMBANDINGKAN GAMBAR ORI DAN GAMBAR HASIL FILTER
        self.btn_to_compare = ttk.Button(self.tool_mid, text="COMPARE IMAGE", style='info.TButton', command=self.compare)
        self.btn_to_compare.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    # MEMBUAT BUTTON UNTUK MENAMPILKAN GAMBAR HASIL FILTER SAJA
        self.btn_to_preview = ttk.Button(self.tool_mid, text="PREVIEW", style='info.TButton',command=self.preview_layout)
        self.btn_to_preview.grid(row=0, column=2, sticky='w', padx=5, pady=5)

    # BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
        self.image_def = Image.open("resources/noimage.jpg")
        self.image_ori = Image.open("resources/noimage.jpg")
        self.image_filter = Image.open("resources/noimage.jpg")

    # image preview sebelah kiri
        self.image_l = self.image_def.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar = Label(self.left_frame, image=self.image_l)
        self.gambar.grid(row=0, column=0, padx=5, pady=5)

    # IMAGE F
        self.image_r = self.image_def.resize((680, 630), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.middle_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=7)


        # self.middle_frame_1 = Frame(self.middle_frame)
        # self.middle_frame_1.grid(row=0, column=0)

        self.gambar_frame = Frame(self.middle_frame)
        self.gambar_frame.grid(column=0, row=0)


#---------------------------------- RIGHT FRAME SECTION ----------------------------------#
        """DI BAWAH INI MERUPAKAN SOURCE UNTUK BAGIAN CODE YANG ADA 
           PADA MIDDLE FRAME ATAU FRAME TENGAH YANG MENCANGKUP :
           - SLIDER THRESHOLDING
           - SLIDER BRIGHTNESS
           - SLIDER DARKNESS """
#---------------------------------- RIGHT FRAME SECTION ----------------------------------#

    # ------------- MEMBUAT SLIDER THRESHOLD ------------- #
        # LABEL
        self.set_bar = PhotoImage(file="resources/icon/threshold_icon.png")
        self.label_treshold = Label(self.right_frame, image=self.set_bar, width=32, height=32, bd=0, relief="solid")
        self.label_treshold.grid(row=0, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value = 0
        self.scale = ttk.Scale(self.right_frame, variable=current_value, from_=0, to=255, orient=HORIZONTAL, length=250,
                               style="success.Horizontal.TScale",command=self.img_to_threshold)
        self.scale.grid(row=1, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter = Label(self.right_frame, text="0")
        self.label_parameter.grid(row=1, column=1, pady=4, sticky='w')

    # ------------- MEMBUAT SLIDER MULTIPLY ------------- #
        # LABEL
        self.brightness = PhotoImage(file="resources/icon/brightness_icon.png")
        self.label_multiply = Label(self.right_frame, image=self.brightness, width=32, height=32, bd=0, relief="solid")
        self.label_multiply.grid(row=2, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value_multiply = IntVar()
        self.scale_multiply = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,
                                        style="danger.Horizontal.TScale", variable=current_value_multiply,
                                        command=self.img_to_bright)
        self.scale_multiply.grid(row=3, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter_multiply = Label(self.right_frame, text="1.00")
        self.label_parameter_multiply.grid(row=3, column=1, pady=4, sticky='w')

    # ------------- MEMBUAT SLIDER DIVIDE ------------- #
        # LABEL
        self.darkness = PhotoImage(file="resources/icon/darkness_icon.png")
        self.label_divide = Label(self.right_frame, image=self.darkness, width=32, height=32, bd=0, relief="solid")
        self.label_divide.grid(row=4, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value_divide = IntVar()
        self.scale_divide = ttk.Scale(self.right_frame, from_=1, to=10, orient=HORIZONTAL, length=250,
                                      style="info.Horizontal.TScale", variable=current_value_divide,
                                      command=self.img_to_dark)
        self.scale_divide.grid(row=5, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter_divide = Label(self.right_frame, text="1.00")
        self.label_parameter_divide.grid(row=5, column=1, pady=4, sticky='w')

        self.state = False
        # ============================================================================================================

#==================================================================================================================#
#====================================================  METHOD  ====================================================#
#==================================================================================================================#

 # METHOD UNTUK MENGAMBIL GAMBAR
    def get_image(self):
        try:
            self.fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File",
                                                  filetypes=(("PNG Files", "*.png"), ("JPG File", "*.jpg"),
                                                             ("All Files", "*.*")))
            self.file_location = np.copy(self.fln)
            self.image = Image.open(self.fln)
            self.image.save("output.png")
            self.preview_img_mini(self.image)
            self.preview_img(self.image)
        except:
            pass

 # METHOD UNTUK MENAMPILKAN GAMBAR ORIGINAL
    def preview_img_mini(self, image):
        self.image_mini = image.resize((185, 185), Image.ANTIALIAS)
        self.image_mini = ImageTk.PhotoImage(self.image_mini)

        self.img_mini_display = Label(self.left_frame, image=self.image_mini)
        self.img_mini_display.grid(row=0, column=0, padx=5, pady=5)

 # METHOD UNTUK MENAMPILKAN GAMBAR HASIL FILTER
    def preview_img(self, image):

        if self.state == True:
            self.window.geometry("1530x750+1+1")

            try:
                self.image_ori = Image.open(self.fln)
                self.image_filter = image
            except:
                self.image_ori = self.image_def
                self.image_filter = self.image_def

            # labelOri
            ttk.Label(self.gambar_frame, text="Original", style='warning.Inverse.TLabel', anchor="n").grid(row=0, column=0, ipadx=35)

            self.image_compare1 = self.image_ori.resize((390, 390), Image.ANTIALIAS)
            self.image_compare1 = ImageTk.PhotoImage(self.image_compare1)

            self.gambar_c1 = Label(self.gambar_frame, image=self.image_compare1)
            self.gambar_c1.grid(row=1, column=0, padx=5, pady=10, ipadx=5)

            # labelFilter
            ttk.Label(self.gambar_frame, text="Filter", style='warning.Inverse.TLabel', anchor="n").grid(row=0, column=1, ipadx=35)

            self.image_compare2 = self.image_filter.resize((390, 390), Image.ANTIALIAS)
            self.image_compare2 = ImageTk.PhotoImage(self.image_compare2)

            self.gambar_c2 = Label(self.gambar_frame, image=self.image_compare2)
            self.gambar_c2.grid(row=1, column=1, padx=5, pady=10, ipadx=5)

        else :
            self.window.geometry("1380x750+1+1")

            self.image_r = image.resize((680, 630), Image.ANTIALIAS)
            self.image_r = ImageTk.PhotoImage(self.image_r)

            self.gambar_preview = Label(self.gambar_frame, image=self.image_r)
            self.gambar_preview.grid(row=0, column=0, padx=5, pady=7)

            try:
                pass
                # self.gambar_2 = Label(self.middle_frame, image=self.image_r)
                # self.gambar_2.grid(row=0, column=0, padx=1, pady=1)
            except:
                pass
  # METHOD UNTUK MEMANGGIL FILTER DARI CLASS LAIN
    def img_to_threshold(self,event):
        self.filter_apply("threshold")
    def img_to_bright(self,event):
        self.filter_apply("brightness")
    def img_to_dark(self,event):
        self.filter_apply("darkness")

    def filter_apply(self,filter_set):
        self.set_filter = filter_set
        img = cv.imread(self.fln)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        if self.set_filter == "gray":
            img_filter = self.filter_img.image_to_gray(img)
        elif self.set_filter == "red":
            img_filter = self.filter_img.image_to_red(img)
        elif self.set_filter == "green":
            img_filter = self.filter_img.image_to_green(img)
        elif self.set_filter == "blue":
            img_filter = self.filter_img.image_to_blue(img)
        elif self.set_filter == "hsv":
            img_filter = self.filter_img.image_to_hsv(img)
        elif self.set_filter == "negative":
            img_filter = self.filter_img.image_to_negative(img)
        elif self.set_filter == "gaussian":
            img_filter = self.filter_img.image_to_gaussian(img)
        elif self.set_filter == "edge_detection":
            img_filter = self.filter_img.image_to_edge_detection(img)
        elif self.set_filter == "mean_filter":
            img_filter = self.filter_img.image_to_mean_filter(img)
        elif self.set_filter == "sharpen":
            img_filter = self.filter_img.image_to_sharpen(img)
        elif self.set_filter == "unsharp":
            img_filter = self.filter_img.image_to_unsharp(img)
        elif self.set_filter == "threshold":
            self.label_parameter.config(text=str(int(self.scale.get())))
            img_filter = self.filter_img.image_to_threshold(img, self.scale)
        elif self.set_filter == "brightness":
            self.label_parameter_multiply.config(text=f'{(self.scale_multiply.get()):.2f}')
            img_filter = self.filter_img.image_to_bright(img, self.scale_multiply)
        elif self.set_filter == "darkness":
            self.label_parameter_multiply.config(text=f'{(self.scale_divide.get()):.2f}')
            img_filter = self.filter_img.image_to_dark(img, self.scale_divide)

        try:
            cv.imwrite("output.png", img_filter)
        except:
            img_filter.save("output.png")
        img_display = Image.open("output.png")
        self.preview_img(img_display)

    def operation_apply(self,operation_set):
        self.set_operation = operation_set
        img = cv.imread('output.png')
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # UNTUK IMAGE ROTATION
        if self.set_operation == 90:
            img_operate = self.img_operation.image_to_rotated(img,90)
        elif self.set_operation == 180:
            img_operate = self.img_operation.image_to_rotated(img,180)
        elif self.set_operation == 270:
            img_operate = self.img_operation.image_to_rotated(img,270)
        elif self.set_operation == 360:
            img_operate = self.img_operation.image_to_rotated(img,360)
        elif self.set_operation == "custom":
            img_operate = self.img_operation.image_to_rotated(img,int(self.costume_angle.get()))

        # UNTUK IMAGE FLIP
        if self.set_operation == "horizontal":
            img_operate = self.img_operation.image_to_flip_horizontal(img)
        elif self.set_operation == "vertical":
            img_operate = self.img_operation.image_to_flip_vertical(img)

        # UNTUK IMAGE TRANSLATION
        if self.set_operation == "translation":
            location = str(self.file_location)
            d_width = self.trans_width.get()
            d_height = self.trans_height.get()
            img_operate = self.img_operation.image_to_trans(location,d_width,d_height)

        try:
            cv.imwrite("output.png", img_operate)
        except:
            img_operate.save("output.png")

        img_display = Image.open("output.png")
        self.preview_img(img_display)


  # METHOD UNTUK MENGHILANGKAN SEMUA FILTER YANG ADA PADA GAMBAR
    def image_normal(self):
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

    def filter_show(self,image_filter):
        # MENYIMPAN HASILNYA
        img = Image.fromarray(image_filter)
        img.save("output.png")
        self.preview_img(img)

    def save(self):
        image = Image.open("output.png")
        files = [('PNG', '*.png'),
                 ('All Files', '*.*'),
                 ('JPG', '*.jpg')]
        file = filedialog.asksaveasfilename(initialdir="/", filetypes=files, defaultextension=files)
        image.save(file)

    def compare(self):
        self.state = True
        try:
            self.gambar_2.destroy()
            self.gambar_preview.destroy()
            self.gambar_frame.destroy()
        except:
            print("gagal")
            pass

        self.gambar_frame = Frame(self.middle_frame,width=800)
        self.gambar_frame.grid(row=0, column=0, padx=10, pady=107)

        try:
            img = Image.open("output.png")
        except:
            img = self.image_def
            self.fln = self.image_ori

        self.preview_img(img)

    def preview_layout(self):
        self.state = False
        try:
            self.gambar_frame.destroy()
            self.gambar_c2.destroy()
            self.gambar_c1.destroy()
        except:
            pass
            print("hapus")

        self.gambar_frame = Frame(self.middle_frame,bg='#323232')
        self.gambar_frame.grid(row=0, column=0)

        try:
            img = Image.open("output.png")
        except:
            img = self.image_def

        self.preview_img(img)

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

# MEMBUAT SEBUAH CLASS UNTUK WINDOW ATAU MENU 2
class Window_3:
    # MEMBUAT CONSTRUCTOR
    def __init__(self,window):
        # MENGATUR UKURAN ATAU DIMENSI WINDOW

        window.destroy()
        self.window_3 = Tk()
        self.window_3.title("Image Browse App - 5200411434")
        self.window_3.geometry("1295x650+25+25")
        style = Style(theme='darkly')
        self.set_filter = Filter()

        # MEMBUAT LEFT ,MIDDLE DAN RIGHT FRAME
        self.left_frame = Frame(self.window_3, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=15, pady=5)

        self.middle_frame = Frame(self.window_3, width=700, height=550, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=15, pady=15)

        self.right_frame = Frame(self.window_3, width=300, height=550, bg='#323232')
        self.right_frame.grid(row=0, column=2, padx=15, pady=15)

        # MEMBUAT TOOLBARS
        self.tool_bar_2 = Frame(self.left_frame, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=1, column=0, padx=10, pady=50, sticky='w')

        # MEMBUAT BUTTON UNTUK PLAY
        self.play = ttk.Button(self.left_frame, text="Play", width=20, style='success.Outline.TButton',
                               command=self.video)
        self.play.grid(row=0, column=0, pady=3, padx=5, columnspan=2)

        # MEMBUAT BUTTON UNTUK GANTI MENU
        self.menu = ttk.Button(self.left_frame, text="MENU", width=20, style='success.Outline.TButton')
        self.menu.grid(row=2, column=0, pady=3, padx=5, columnspan=2)

        # MEMBUAT BUTTON UNTUK EXIT
        self.exit = ttk.Button(self.left_frame, text="EXIT", width=20, style='danger.Outline.TButton',
                               command=self.exit)
        self.exit.grid(row=3, column=0, pady=3, padx=5, columnspan=2)

        # # RADIO BUTTON BUAT BAGIAN FILTERNYA
        self.tool_bar_1 = Frame(self.right_frame, bg="#3f3f3f")
        self.tool_bar_1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.is_camera_on = True

        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar_1, text="Grayscale", value=1, style='info.TRadiobutton',command=lambda:self.set_filters("gray"))
        self.btn_to_gray.grid(row=1, column=0, padx=25, pady=10, sticky='w')

        self.btn_to_rgb = ttk.Radiobutton(self.tool_bar_1, text="RGB", value=2, style='info.TRadiobutton',command=lambda:self.set_filters("rgb"))
        self.btn_to_rgb.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        self.btn_to_hsv = ttk.Radiobutton(self.tool_bar_1, text="HSV", value=3, style='info.TRadiobutton',command=lambda: self.set_filters("hsv"))
        self.btn_to_hsv.grid(row=2, column=0, padx=25, pady=10, sticky='w')

        self.btn_to_edge_detection = ttk.Radiobutton(self.tool_bar_1, text="Edge Detection", value=4, style='info.TRadiobutton',
                                          command=lambda: self.set_filters("edge_detection"))
        self.btn_to_edge_detection .grid(row=2, column=1, padx=25, pady=10, sticky='w')

        self.btn_to_sharp = ttk.Radiobutton(self.tool_bar_1, text="Sharpner", value=5,
                                                     style='info.TRadiobutton',
                                                     command=lambda: self.set_filters("sharpner"))
        self.btn_to_sharp.grid(row=3, column=1, padx=25, pady=10, sticky='w')

        # LABEL THRESHOLD
        self.label_treshold = ttk.Radiobutton(self.tool_bar_1, text="Threshold", style='info.TRadiobutton',value=6,command=lambda: self.set_filters("threshold"))
        self.label_treshold.grid(row=3, column=0, pady=4, sticky='n', ipady=3)

        # SLIDER
        current_value = 0
        self.scale = ttk.Scale(self.right_frame, variable=current_value, from_=0, to=255, orient=HORIZONTAL, length=250,
                               style="success.Horizontal.TScale")
        self.scale.grid(row=4, column=0, pady=4, sticky='w')

        # PARAMETER
        self.label_parameter = Label(self.right_frame, text="0")
        self.label_parameter.grid(row=4, column=1, pady=4, sticky='w')

    def set_filters(self,filter):
        if self.is_camera_on == True:
            self.cap = cv.VideoCapture(0)
            self.lmain = Label(self.middle_frame)
            self.is_camera_on = False

        self.filters = filter

    def video(self):

        _, self.frame = self.cap.read()
        self.frame = cv.flip(self.frame, 1)
        self.label_parameter.config(text=str(int(self.scale.get())))

        if self.filters == "rgb":
            cv2image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
        elif self.filters == "gray":
            cv2image = self.set_filter.image_to_gray(self.frame)
        elif self.filters == "edge_detection":
            cv2image = self.set_filter.image_to_edge_detection(self.frame)
        elif self.filters == "sharpner":
            cv2image = self.set_filter.image_to_sharpen(self.frame)
        elif self.filters == "hsv":
            cv2image = self.set_filter.image_to_hsv(self.frame)
        elif self.filters == "threshold":
            self.frame = cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY)

            ret, thresh1 = cv.threshold(self.frame, self.scale.get(), 255, cv.THRESH_BINARY)
            cv2image = thresh1


        img = Image.fromarray(cv2image)
        imgtk = img.resize((650, 600), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)

        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.grid(row=0, column=0, padx=5, pady=10)
        self.lmain.after(1, self.video)

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


# MEMBUAT SEBUAH OBJECT MAIN WINDOW

main_window = Window_1()
main_window.window.mainloop()
