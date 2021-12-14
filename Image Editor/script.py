from tkinter import *
import tkinter as tk
import numpy as np
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk, ImageDraw ,ImageFilter
import os
from ttkbootstrap import Style
from tkinter import ttk
import math
from tkscrolledframe import ScrolledFrame

class Filter:
    def __init__(self):
        pass
    def convolve(self,X, F):
        X_height = X.shape[0]
        X_width = X.shape[1]

        F_height = F.shape[0]
        F_width = F.shape[1]

        H = (F_height - 1) // 2
        W = (F_width - 1) // 2

        out = np.zeros((X_height, X_width))
        # iterate over all the pixel of image X
        for i in np.arange(H, X_height - H):
            for j in np.arange(W, X_width - W):
                sum = 0
                # iterate over the filter
                for k in np.arange(-H, H + 1):
                    for l in np.arange(-W, W + 1):
                        # get the corresponding value from image and filter
                        a = X[i + k, j + l]
                        w = F[H + k, W + l]
                        sum += (w * a)
                out[i, j] = sum
        return out

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

        Gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
        Gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])

        img_gaussian = cv.GaussianBlur(gray, (3, 3), 0)

        #=====================   CARA FROM SCARTCH  ============================
        # sobel_x = self.convolve(img_gaussian,Gx)
        # sobel_y = self.convolve(img_gaussian,Gy)
        #========================================================================

        # ===========================   LIBRARY ==================================
        sobel_x = cv.filter2D(src=img_gaussian, ddepth=-1, kernel=Gx)
        sobel_y = cv.filter2D(src=img_gaussian, ddepth=-1, kernel=Gy)
        # ========================================================================
        img_sobel = sobel_x + sobel_y

        return img_sobel

    def image_to_prewitt(self,img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_gaussian = cv.GaussianBlur(gray, (3, 3), 0)

        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

        # =====================   CARA FROM SCARTCH  =============================
        # img_prewittx = self.convolve(img_gaussian,kernelx)
        # img_prewitty = self.convolve(img_gaussian,kernely)
        # ========================================================================

        # ===========================   LIBRARY ==================================
        img_prewittx = cv.filter2D(img_gaussian, -1, kernelx)
        img_prewitty = cv.filter2D(img_gaussian, -1, kernely)
        # ========================================================================

        img_prewitt = img_prewittx + img_prewitty
        return img_prewitt

    def image_to_erosi(self,img,kernel):
        imgErode = cv.erode(img, kernel=kernel, iterations=1)
        return imgErode

    def image_to_dilasi(self,img,kernel):
        imgDilate = cv.dilate(img, kernel=kernel, iterations=1)
        return imgDilate

    def image_to_opening(self,img):
        se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        # img_canny = self.image_to_canny(img)
        img = self.image_to_erosi(img,se)
        img = self.image_to_dilasi(img,se)
        return img

    def image_to_closing(self,img):
        se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        img_canny = self.image_to_canny(img)
        img = self.image_to_dilasi(img_canny,se)
        img = self.image_to_erosi(img,se)
        return img
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

    def image_to_resize(self,img,new_width,new_height):
        input_pixels = img.load()
        new_size = (new_width, new_height)

        # Create output image
        output_image = Image.new("RGB", new_size)
        draw = ImageDraw.Draw(output_image)

        x_scale = img.width / output_image.width
        y_scale = img.height / output_image.height

        # Copy pixels
        for x in range(output_image.width):
            for y in range(output_image.height):
                xp, yp = math.floor(x * x_scale), math.floor(y * y_scale)
                draw.point((x, y), input_pixels[xp, yp])

        return output_image



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
        self.window.geometry("1400x800+1+1")
        self.window.config(bg="#323232")
        style = Style(theme='darkly')
        rb_s = 'info.TRadiobutton'

        self.filter_img = Filter()
        self.img_operation = Image_operation()

    # MEMBUAT LEFT , MIDDLE , RIGHT FRAME
        self.left_frame = tk.Frame(self.window, width=500, height=700, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')

        self.middle_frame = tk.Frame(self.window, width=800, height=600, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')

        self.right_frame = tk.Frame(self.window, width=100, height=550, bg='#222222')
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
                11. CANNY DETECTION
                12. SOBEL DETECTION
                13. PREWITT DETECTION
           - ROTATE IMAGE
           - TRANSLASI IMAGE
           - FLIP HORIZONTAL DAN FLIP VERIKAL
           - RESIZE IMAGE
           - BUTTON GANTI MENU
           - BUTTON EXIT """
        # -------------------------- LEFT FRAME SECTION------------------------#

    # LABEL UNTUK MENAMPUNG BUTTON SEARCH IMAGE
        self.gambar = Label(self.left_frame, height=13, width=25)
        self.gambar.grid(row=0, column=0, pady=0)

    # BUTTON AMBIL GAMBAR
        ttk.Style().configure('Outline.TButton', bordercolor="none", foreground="white", background="#2F8886", width=15,
                              font=('Helvetica', 10))
        self.icon_picture = PhotoImage(file="resources/icon/picture_icon.png")
        self.search = ttk.Button(self.left_frame, text="  Browser Image", image=self.icon_picture,
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
        self.filter.grid(row=0, column=0, ipadx=120,stick="w",columnspan=3)

        # RB BAGIAN GRAYSCALE
        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_gray = ttk.Radiobutton(self.tool_bar, text="Grayscale", value=1, style=rb_s,
                                           command=lambda:self.filter_apply("Gray"))
        self.btn_to_gray.grid(row=1, column=0, pady=15,padx=5, sticky='w')

        # RB BAGIAN BLUE CHANNEL
        self.btn_to_negative = ttk.Radiobutton(self.tool_bar, text="Negative", value=2, style=rb_s,
                                           command=lambda:self.filter_apply("Negative"))
        self.btn_to_negative.grid(row=1, column=1, pady=15,padx=5, sticky='w')

        # RB BAGIAN ORIGINAL IMAGE
        self.btn_to_normal = ttk.Radiobutton(self.tool_bar, text="Original", value=3, style=rb_s,
                                             command=self.image_normal)
        self.btn_to_normal.grid(row=1, column=2, pady=15,padx=5, sticky='w')

        # RB BAGIAN GREEN CHANNEL
        self.btn_to_green = ttk.Radiobutton(self.tool_bar, text="Green Channel", value=4, style=rb_s,
                                            command=lambda:self.filter_apply("Green"))
        self.btn_to_green.grid(row=2, column=0, pady=15,padx=5, sticky='w')

        # RB BAGIAN NEGATIVE IMAGE
        self.btn_blue = ttk.Radiobutton(self.tool_bar, text="Blue Channel", value=5, style=rb_s,
                                            command=lambda:self.filter_apply("Blue"))
        self.btn_blue.grid(row=2, column=1, pady=15,padx=5, sticky='w')

        # RB BAGIAN RED CHANNEL
        self.btn_to_red = ttk.Radiobutton(self.tool_bar, text="Red Channel", value=6, style=rb_s,
                                          command=lambda:self.filter_apply("Red"))
        self.btn_to_red.grid(row=2, column=2, pady=15,padx=5, sticky='w')

        # HSV
        self.btn_to_unsharp= ttk.Radiobutton(self.tool_bar, text="Unsharp", value=9,
                                          style=rb_s,command=lambda:self.filter_apply("Unsharp"))
        self.btn_to_unsharp.grid(row=3, column=0, pady=15,padx=5, sticky='w')

        # SHARPEN FILTER
        self.btn_to_sharpen = ttk.Radiobutton(self.tool_bar, text="Sharpen Filter", value=7, style=rb_s,
                                          command=lambda:self.filter_apply("Sharpen"))
        self.btn_to_sharpen.grid(row=3, column=1, pady=15,padx=5, sticky='w')

        # MEDIAN FILTER
        self.btn_to_median = ttk.Radiobutton(self.tool_bar, text="Mean Filter", value=8,
                                          style=rb_s,command=lambda:self.filter_apply("Mean_filter"))
        self.btn_to_median.grid(row=3, column=2, pady=15,padx=5, sticky='w')


        # MEAN / AVERAGE FILTER
        self.btn_to_mean = ttk.Radiobutton(self.tool_bar, text="Edge Detection", value=10,
                                          style=rb_s,command=lambda:self.filter_apply("Edge_detection"))
        self.btn_to_mean.grid(row=4, column=0, pady=15,padx=5, sticky='w')

        # GAUSSIAN FILTER
        self.btn_to_gaussian = ttk.Radiobutton(self.tool_bar, text="Gaussian Blur", value=11,
                                          style=rb_s,command=lambda:self.filter_apply("Gaussian"))
        self.btn_to_gaussian.grid(row=4, column=1, pady=15,padx=5, sticky='w')

        # UNSHARP FILTER
        self.btn_to_hsv = ttk.Radiobutton(self.tool_bar, text="HSV", value=12,
                                          style=rb_s, command=lambda:self.filter_apply("Hsv"))
        self.btn_to_hsv.grid(row=4, column=2, pady=15,padx=5, sticky='w')

        # FRAME UNTUK MENAMPUNG RADIO BUTTON YANG BERISI FILTER UNTUK EDGE DETECTION
        self.tool_bar_2 = Frame(self.frame1, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter_2 = PhotoImage(file="resources/icon/filter_icon.png")
        self.filter_2 = Label(self.tool_bar_2, image=self.icon_filter_2, text="Edge Detection", compound='left',
                              bg="#FD7014")
        self.filter_2.grid(row=0, column=0, ipadx=90, stick="w", columnspan=3)

        # RB BAGIAN CANNY
        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_canny = ttk.Radiobutton(self.tool_bar_2, text="Canny", value=13, style=rb_s,
                                            command=lambda: self.filter_apply("Canny"))
        self.btn_to_canny.grid(row=1, column=0, pady=10, padx=15, sticky='w')

        # RB BAGIAN SOBEL
        self.btn_to_sobel = ttk.Radiobutton(self.tool_bar_2, text="Sobel", value=14, style=rb_s,
                                            command=lambda: self.filter_apply("Sobel"))
        self.btn_to_sobel.grid(row=1, column=1, pady=10, padx=15, sticky='w')

        # RB BAGIAN PREWITT
        self.btn_to_prewitt = ttk.Radiobutton(self.tool_bar_2, text="Prewitt", value=15, style=rb_s,
                                              command=lambda: self.filter_apply("Prewitt"))
        self.btn_to_prewitt.grid(row=1, column=2, pady=10, padx=15, sticky='w')

# ==================================================================================================================#
# ==================================================== FILTER 2 ====================================================#
# ==================================================================================================================#

        # RADIO BUTTON BUAT BAGIAN FILTERNYA PADA TAB2

        # FRAME UNTUK MENAMPUNG RADIO BUTTON YANG BERISI FILTER
        self.tool_bar_r2 = Frame(self.frame2, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_r2.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter_r2 = PhotoImage(file="resources/icon/filter_icon.png")
        self.morph = Label(self.tool_bar_r2, image=self.icon_filter_2, text="Morfologi", compound='left',bg="#FD7014")
        self.morph.grid(row=0, column=0, ipadx=110,stick="w",columnspan=3)

        # RB BAGIAN EROSI
        ttk.Style().configure('info.TRadiobutton', background="#444444", foreground='white', font=('Helvetica', 8))
        self.btn_to_eros = ttk.Radiobutton(self.tool_bar_r2, text="Erosi", value=16, style=rb_s,
                                            command=lambda: self.filter_apply("Erosi"))
        self.btn_to_eros.grid(row=2, column=0, padx=15, pady=5, sticky='w',rowspan=2)

        # SPACE
        Label(self.tool_bar_r2, text="", anchor="n",bg="#3f3f3f").grid(row=1,column=1,pady=1)
        # COSTUME ANGLE
        ttk.Label(self.tool_bar_r2, text="St. El. Size", style='warning.Inverse.TLabel',anchor="n",width=21).grid(row=2,padx=10,column=1,ipadx=3, sticky="w")
        self.costume_st_element = ttk.Entry(self.tool_bar_r2, style='info.TEntry',text="",width=21)
        self.costume_st_element.grid(row=3, column=1, sticky="w", padx=10)

        # SPACE
        Label(self.tool_bar_r2, text="", anchor="n", bg="#3f3f3f").grid(row=4, column=1, pady=1)
        # RB BAGIAN DILASI
        self.btn_to_dilasi = ttk.Radiobutton(self.tool_bar_r2, text="Dilasi", value=17, style=rb_s,command=lambda: self.filter_apply("Dilasi"))
        self.btn_to_dilasi.grid(row=5, column=0, padx=15, pady=5, sticky='w',rowspan=2)

        # SPACE
        Label(self.tool_bar_r2, text="", anchor="n", bg="#3f3f3f").grid(row=1, column=1, pady=1)
        # COSTUME ANGLE
        ttk.Label(self.tool_bar_r2, text="St. El. Size", style='warning.Inverse.TLabel', anchor="n",width=21).grid(row=5, column=1,padx=10,ipadx=3, sticky="w")
        self.costume_st_element_2 = ttk.Entry(self.tool_bar_r2, style='info.TEntry', text="", width=21)
        self.costume_st_element_2.grid(row=6, column=1, sticky="w", padx=10)

        # SPACE
        Label(self.tool_bar_r2, text="", anchor="n", bg="#3f3f3f").grid(row=7, column=0)

        # FRAME UNTUK MENAMPUNG RADIO BUTTON YANG BERISI FILTER
        self.tool_bar_r3 = Frame(self.frame2, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_r3.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.icon_filter_r3 = PhotoImage(file="resources/icon/filter_icon.png")
        self.morph_2 = Label(self.tool_bar_r3, image=self.icon_filter_2, text="Morfologi", compound='left', bg="#FD7014")
        self.morph_2.grid(row=0, column=0, ipadx=110, stick="we", columnspan=3)

        # RB BAGIAN OPENING
        self.btn_to_opening = ttk.Radiobutton(self.tool_bar_r3, text="Opening", value=18, style=rb_s,
                                              command=lambda: self.filter_apply("Opening"))
        self.btn_to_opening.grid(row=1, column=0, padx=30, pady=15, sticky='we')
        # RB BAGIAN CLOSING
        self.btn_to_closing = ttk.Radiobutton(self.tool_bar_r3, text="Closing", value=19, style=rb_s,
                                           command=lambda: self.filter_apply("Closing"))
        self.btn_to_closing.grid(row=1, column=1, padx=30, pady=15, sticky='we')


#==================================================================================================================#
#==================================================== FILTER 3 ====================================================#
#==================================================================================================================#
        # FRAME ATAS BUAT KONTEN ROTASI
        self.tool_bar_2_1 = Frame(self.frame3, width=180, height=200, bg="#3f3f3f")
        self.tool_bar_2_1.grid(row=0, column=0,  pady=10,padx=5, sticky='w')

        self.icon_rotate = PhotoImage(file="resources/icon/rotation_icon.png")
        self.rotate = Label(self.tool_bar_2_1, image=self.icon_rotate, text=" Rotation", compound='left', bg="#FD7014")
        self.rotate.grid(row=0, column=0, ipadx=108, columnspan=3)

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
        space = Label(self.tool_bar_2_1,bg="#3f3f3f").grid(row=3,column=0)
        self.costume_angle = ttk.Entry(self.tool_bar_2_1, style='info.TEntry')
        self.costume_angle.grid(row=4, column=0, sticky="w", padx=15,pady=10)

        self.btn_angle = ttk.Button(self.tool_bar_2_1, text="Rotate", style='warning.Outline.TButton', width=6,
                                    command=lambda: self.operation_apply("custom"))
        self.btn_angle.grid(row=4, column=1, padx=5)

        # FRAME BAWAH BUAT KONTEN TRANSLASI
        self.tool_bar_2_2 = Frame(self.frame3, width=180, height=200, bg="#444444")
        self.tool_bar_2_2.grid(row=1, column=0, padx=5, pady=10,sticky='w')

        self.icon_translation = PhotoImage(file="resources/icon/flip_icon.png")
        self.trans = Label(self.tool_bar_2_2, image=self.icon_translation, text=" Translation", compound='left', bg="#FD7014")
        self.trans.grid(row=0, column=0, ipadx=100, columnspan=3)

        self.trans_width = ttk.Entry(self.tool_bar_2_2, style='info.TEntry',width=8)
        self.trans_width.insert(0, 'width')
        self.trans_width.grid(row=1, column=0, sticky="e", padx=13,pady=8)

        self.trans_height = ttk.Entry(self.tool_bar_2_2, style='info.TEntry', width=8)
        self.trans_height.insert(0, 'height')
        self.trans_height.grid(row=1, column=1, sticky="w", padx=4, pady=8)

        self.btn_trans = ttk.Button(self.tool_bar_2_2, text="Trans", style='warning.Outline.TButton', width=6,
                                    command=lambda:self.operation_apply("translation"))
        self.btn_trans.grid(row=1, column=2, padx=1,sticky='w')

# ==================================================================================================================#
# ==================================================== FILTER 3 ====================================================#
# ==================================================================================================================#

        # RADIO BUTTON BUAT BAGIAN FILTERNYA

        # MEMBUAT FRAME UNTUK MENAMPUNG SESUATU YANG BERHUBUNGAN DENGAN FLIP
        self.tool_bar_4 = Frame(self.frame4, width=180, height=200, bg="#444444")
        self.tool_bar_4.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.icon_flip = PhotoImage(file="resources/icon/flip_icon.png")
        self.flip = Label(self.tool_bar_4, image=self.icon_flip, text=" Flip", compound='left', bg="#FD7014")
        self.flip.grid(row=0, column=0, ipadx=125, columnspan=2)

        # CB BUAT FLIP
        ttk.Style().configure('Squaretoggle.Toolbutton', background="#3f3f3f", font=('Helvetica', 10))
        self.on_horizontal = IntVar()
        self.on_vertical = IntVar()

        self.btn_to_hor = ttk.Checkbutton(self.tool_bar_4, onvalue=1, offvalue=0, text="Horizontal",
                                          variable=self.on_horizontal, style='success.Squaretoggle.Toolbutton',
                                          command=lambda:self.operation_apply("horizontal"))
        self.btn_to_hor.grid(row=1, column=0, padx=20, pady=10,ipadx=11, sticky='w')

        self.btn_to_ver = ttk.Checkbutton(self.tool_bar_4, onvalue=1, offvalue=0, text="Vertical",
                                          variable=self.on_vertical, style='danger.Squaretoggle.Toolbutton',
                                          command=lambda:self.operation_apply("vertical"))
        self.btn_to_ver.grid(row=1, column=1, padx=25, pady=10, sticky='w')

        # FRAME BAWAH BUAT KONTEN SCALING / RESIZE
        self.tool_bar_4_2 = Frame(self.frame4, width=180, height=200, bg="#444444")
        self.tool_bar_4_2.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        self.icon_resize = PhotoImage(file="resources/icon/resize_icon.png")
        self.resize = Label(self.tool_bar_4_2, image=self.icon_resize, text=" Resize", compound='left', bg="#FD7014")
        self.resize.grid(row=0, column=0,columnspan=3, ipadx=115)

        self.new_width = ttk.Entry(self.tool_bar_4_2,style='info.TEntry', width=8)
        self.new_width.insert(0, 'width')
        self.new_width.grid(row=1, column=0, sticky="e", padx=5, pady=8)

        self.new_height = ttk.Entry(self.tool_bar_4_2, style='info.TEntry', width=8)
        self.new_height.insert(0, 'height')
        self.new_height.grid(row=1, column=1, sticky="w", padx=5, pady=8)

        self.btn_resize = ttk.Button(self.tool_bar_4_2, text="Resize", style='warning.Outline.TButton', width=6,
                                    command=lambda: self.operation_apply("resize"))
        self.btn_resize.grid(row=1, column=2, sticky="w", padx=5, pady=8)

#==================================================================================================================#
#==================================================== FILTER 4 ====================================================#
#==================================================================================================================#

#---------------------------------- MIDDLE FRAME SECTION ----------------------------------#
        """DI BAWAH INI MERUPAKAN SOURCE UNTUK BAGIAN CODE YANG ADA 
           PADA MIDDLE FRAME ATAU FRAME TENGAH YANG MENCANGKUP
           - PREVIEW GAMBAR
           - BUTTON SAVE
           - BUTTON COMPARE
           - BUTTON PREVIEW
           - BUTTON DELETE """
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

    # MEMBUAT BUTTON UNTUK MEMBANDINGKAN GAMBAR ORI DAN GAMBAR HASIL FILTER
        self.btn_to_delete = ttk.Button(self.tool_mid, text="DELETE IMAGE", style='info.TButton',command=self.input_nama)
        self.btn_to_delete.grid(row=0, column=2, sticky='w', padx=5, pady=5)

    # MEMBUAT BUTTON UNTUK MENAMPILKAN GAMBAR HASIL FILTER SAJA
        self.btn_to_preview = ttk.Button(self.tool_mid, text="PREVIEW", style='info.TButton',command=self.preview_layout)
        self.btn_to_preview.grid(row=0, column=3, sticky='w', padx=5, pady=5)

    # BAGIAN UNTUK MENAMPILKAN DEFAULT IMAGE (JIKA GAMBAR BELUM DIPILIH)
        self.image_def = Image.open("resources/noimage.jpg")
        self.image_ori = Image.open("resources/noimage.jpg")
        self.image_filter = Image.open("resources/noimage.jpg")

        self.total_gambar_compare = 2
        self.index = 0

        self.gambar_frame = Frame(self.middle_frame)
        self.gambar_frame.grid(column=0, row=0,sticky="n")

    # image preview sebelah kiri
        self.image_l = self.image_def.resize((185, 185), Image.ANTIALIAS)
        self.image_l = ImageTk.PhotoImage(self.image_l)
        self.gambar = Label(self.left_frame, image=self.image_l)
        self.gambar.grid(row=0, column=0, padx=5, pady=5)

    # IMAGE F
        self.image_r = self.image_def.resize((680, 630), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)
        self.gambar_2 = Label(self.gambar_frame, image=self.image_r)
        self.gambar_2.grid(row=0, column=0, padx=5, pady=7)

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
        self.compare_state = False
        self.kolom = 0
        self.baris = 2
        self.gambar_list = []
        self.img_path =[]
        self.nama_filter =[]
        self.i = 0
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
            self.image.save("outputori.png")

            self.img_path.append("outputori.png")
            self.nama_filter.append("Original")

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
            self.window.geometry("1530x800+1+1")
            self.sf = ScrolledFrame(self.gambar_frame, width=800, height=690)
            self.sf.grid(column=0, row=0)

            self.sf.bind_arrow_keys(self.gambar_frame)
            self.sf.bind_scroll_wheel(self.gambar_frame)

            self.frame = self.sf.display_widget(Frame)
            self.tambah_gambar()

        else :
            self.window.geometry("1380x800+1+1")

            self.image_r = image.resize((680, 630), Image.ANTIALIAS)
            self.image_r = ImageTk.PhotoImage(self.image_r)

            self.gambar_preview = Label(self.gambar_frame, image=self.image_r)
            self.gambar_preview.grid(row=0, column=0, padx=5, pady=7)

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

        if self.set_filter == "Gray":
            img_filter = self.filter_img.image_to_gray(img)
        elif self.set_filter == "Red":
            img_filter = self.filter_img.image_to_red(img)
        elif self.set_filter == "Green":
            img_filter = self.filter_img.image_to_green(img)
        elif self.set_filter == "Blue":
            img_filter = self.filter_img.image_to_blue(img)
        elif self.set_filter == "Hsv":
            img_filter = self.filter_img.image_to_hsv(img)
        elif self.set_filter == "Negative":
            img_filter = self.filter_img.image_to_negative(img)
        elif self.set_filter == "Gaussian":
            img_filter = self.filter_img.image_to_gaussian(img)
        elif self.set_filter == "Edge_detection":
            img_filter = self.filter_img.image_to_edge_detection(img)
        elif self.set_filter == "Mean_filter":
            img_filter = self.filter_img.image_to_mean_filter(img)
        elif self.set_filter == "Sharpen":
            img_filter = self.filter_img.image_to_sharpen(img)
        elif self.set_filter == "Unsharp":
            img_filter = self.filter_img.image_to_unsharp(img)

    # PAKE SLIDER
        elif self.set_filter == "Threshold":
            self.label_parameter.config(text=str(int(self.scale.get())))
            img_filter = self.filter_img.image_to_threshold(img, self.scale)
        elif self.set_filter == "Brightness":
            self.label_parameter_multiply.config(text=f'{(self.scale_multiply.get()):.2f}')
            img_filter = self.filter_img.image_to_bright(img, self.scale_multiply)
        elif self.set_filter == "Darkness":
            self.label_parameter_divide.config(text=f'{(self.scale_divide.get()):.2f}')
            img_filter = self.filter_img.image_to_dark(img, self.scale_divide)

    # BAGIAN EDGE DETECTION
        elif self.set_filter == "Canny":
            img_filter = self.filter_img.image_to_canny(img)
        elif self.set_filter == "Sobel":
            img_filter = self.filter_img.image_to_sobel(img)
        elif self.set_filter == "Prewitt":
            img_filter = self.filter_img.image_to_prewitt(img)

    # BAGIAN MORFOLOGI
        elif self.set_filter == "Erosi":
            k = int(self.costume_st_element.get())
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (k, k))
            img_filter = self.filter_img.image_to_erosi(img,kernel)
        elif self.set_filter == "Dilasi":
            k = int(self.costume_st_element_2.get())
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (k, k))
            img_filter = self.filter_img.image_to_dilasi(img,kernel)
        elif self.set_filter == "Closing":
            img_filter = self.filter_img.image_to_closing(img)
        elif self.set_filter == "Opening":
            img_filter = self.filter_img.image_to_opening(img)

        try:
            cv.imwrite("output.png", img_filter)
            cv.imwrite(f"output{self.i}.png", img_filter)
        except:
            img_filter.save("output.png")
            img_filter.save(f"output{self.i}.png")

        img_display = Image.open("output.png")
        if self.compare_state == True:
            self.img_path.append(f"output{self.i}.png")
            self.nama_filter.append(self.set_filter)
            self.tambah_gambar()
            self.i += 1

        else:
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
        elif self.set_operation == "horizontal":
            img_operate = self.img_operation.image_to_flip_horizontal(img)
        elif self.set_operation == "vertical":
            img_operate = self.img_operation.image_to_flip_vertical(img)

        # UNTUK IMAGE TRANSLATION
        elif self.set_operation == "translation":
            location = str(self.file_location)
            d_width = self.trans_width.get()
            d_height = self.trans_height.get()
            img_operate = self.img_operation.image_to_trans(location,d_width,d_height)

        # UNTUK IMAGE RESIZED
        elif self.set_operation == "resize":
            new_width = int(self.new_width.get())
            new_height = int(self.new_height.get())
            img_operate = self.img_operation.image_to_resize(img, new_width, new_height)


        try:
            cv.imwrite(f"output{self.i}.png", img_operate)
            cv.imwrite(f"output.png", img_operate)
        except:
            img_operate.save("output.png")
            img_operate.save(f"output{self.i}.png")

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
        self.compare_state = True
        try:
            self.gambar_frame.destroy()
            self.gambar_frame.forget
            self.gambar_2.destroy()
            self.gambar_preview.destroy()
        except:
            print("gagal")
            pass

        self.gambar_frame = Frame(self.middle_frame,width=800)
        self.gambar_frame.grid(row=0, column=0, padx=10, pady=5)

        try:
            img = Image.open("output.png")
        except:
            img = self.image_def
            self.fln = self.image_ori

        self.preview_img(img)

    def tambah_gambar(self):
        kolom = 0
        baris = 0
        self.img_list = []
        print("path :", self.img_path)

        for i in range (0,len(self.img_path)):
            img = Image.open(self.img_path[i])
            img = img.resize((375, 350), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.img_list.append(img)

        for i in range(0,len(self.img_list)+1):
            try:
                ttk.Label(self.frame, text=f"{self.nama_filter[i]}", style='warning.Inverse.TLabel', anchor="n").grid(row=baris, column=kolom,ipadx=35)
                ttk.Label(self.frame,image=self.img_list[i]).grid(row=baris+1, column=kolom, padx=5, pady=10, ipadx=5)
                kolom += 1

                if kolom == 2:
                    kolom = 0
                    baris += 2
            except:
                print("gagal")
                pass
        self.kolom = 0

    def input_nama(self):
        top = Toplevel(self.window)
        top.geometry("450x150")
        top.title("Child Window")
        Label(top,text="nama filter :").grid(row=0,column=0)
        nama_filter = ttk.Entry(top, style='info.TEntry', width=25)
        nama_filter.insert(0,'')
        nama_filter.grid(row=0, column=1, sticky="w", padx=2, pady=8)

        Button(top,text='delete',command=lambda:self.hapus_gambar(nama_filter.get())).grid(row=0,column=2)

    def hapus_gambar(self,nama_filter):
        index = 0
        for i in self.nama_filter:
            if i == nama_filter:
                self.nama_filter.remove(nama_filter)
                self.img_list.pop(index)
                self.img_path.pop(index)
                self.compare()
            index += 1

    def preview_layout(self):
        self.state = False
        self.compare_state = False
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
            os.remove("outputori.png")
            for i in range (0,10):
                os.remove(f"output{i}.png")
        except:
            print("Tidak ada gambar dengan nama itu")
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
