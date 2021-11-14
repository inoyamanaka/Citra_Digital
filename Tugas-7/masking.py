from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
from tkinter import ttk
from ttkbootstrap import Style
import numpy as np

class Window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600+10+10")
        self.window.title("Browser-5200411434")
        style = Style(theme="darkly")

        # Membuat Frame
        self.left_frame = Frame(self.window, bg='#323232')
        self.left_frame.grid(row=0, column=0, padx=10, sticky='n')

        self.middle_frame = Frame(self.window, bg='#323232')
        self.middle_frame.grid(row=0, column=1, padx=10)

        self.right_frame = Frame(self.window, bg='#323232',width=700)
        self.right_frame.grid(row=0, column=2,ipadx=10 ,padx=10, sticky='n')

        # Image Background Kota dan Langit
        self.image_bg = Image.open("cloudy-city.png")
        self.image_bg = self.image_bg.resize((550, 500), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image_bg)
        self.background = Label(self.left_frame, image=self.image_bg)
        self.background.grid(row=0, column=0)

        # Image Pesawat jet
        self.image_pesawat = Image.open("jet.jpg")
        self.image_pesawat = self.image_pesawat.resize((150, 100), Image.ANTIALIAS)
        self.image_pesawat = ImageTk.PhotoImage(self.image_pesawat)
        self.pesawat = Label(self.middle_frame, image=self.image_pesawat)
        self.pesawat.grid(row=0, column=0)

        # Mengatur Threshold dari pesawat
        self.tool = Frame(self.middle_frame)
        self.tool.grid(row=1, column=0)

        # SLIDER
        current_value_divide = IntVar()
        self.scale = ttk.Scale(self.middle_frame, from_=0, to=255, orient=HORIZONTAL, length=250,
                                 style="info.Horizontal.TScale", variable=current_value_divide, command=self.threshold)
        self.scale.grid(row=2, column=0, pady=4, sticky='w',padx=10)

        # PARAMETER
        self.label_parameter = Label(self.middle_frame, text="1.00")
        self.label_parameter.grid(row=2, column=1, pady=4, sticky='w')

        # BUTTON UNTUK APPLY
        self.btn_submit = ttk.Button(self.middle_frame, text="Apply", width=20, style='success.Outline.TButton',
                                   command=self.apply)
        self.btn_submit.grid(row=3, column=0, pady=5, padx=5)

    def preview(self,image):
        self.image_r = image.resize((150, 100), Image.ANTIALIAS)
        self.image_r = ImageTk.PhotoImage(self.image_r)

        self.pesawat = Label(self.middle_frame, image=self.image_r)
        self.pesawat.grid(row=0, column=0)

    # METHOD UNTUK MENGATUR THRESHOLD
    def threshold(self,event):
        try:
            self.label_parameter.config(text=str(int(self.scale.get())))
            img = cv.imread("jet.jpg", 0)
            treshold = np.zeros((img.shape), dtype=np.uint8)

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    pixel = img[i, j]
                    if pixel < int(self.scale.get()):
                        treshold[i, j] = 1 * 255
                    else:
                        treshold[i, j] = 0 * 255

            self.img_tres = treshold
            self.tresh_img = Image.fromarray(treshold)
            self.preview(self.tresh_img)
        except:
            pass

    def to_rgb(self,img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img

    def apply(self):
        img_ori = cv.imread("jet.jpg")
        image_sky = cv.imread("cloudy-city.png")
        bg = image_sky[0:img_ori.shape[0], 0:img_ori.shape[1]]

        # MEMBUAT MASKING
        mask = self.img_tres
        mask_inv = cv.bitwise_not(mask)

        print(f"ukuran gambar threshold :{mask.shape}")
        print(f"ukuran gambar background :{bg.shape}")

        # MENGAMBIL BACKGROUNDNYA + TEMPAT UNTUK PESAWAT GAMBAR HITAM
        img1_bg = cv.bitwise_and(bg, bg ,mask=mask_inv)

        # MENGAMBIL GAMBAR PESAWAT YANG MENGAKIBATKAN BG HITAM
        img2_fg = cv.bitwise_and(img_ori, img_ori, mask=mask)

        # MENGGABUNGKAN GAMBAR
        dst = cv.add(img1_bg, img2_fg)
        image_sky[0:mask.shape[0], 0:mask.shape[1]] = dst

        # MENHUBAH GAMBAR KE DALAM BENTUK RGB
        img1_bg = self.to_rgb(img1_bg)
        img2_fg = self.to_rgb(img2_fg)
        img_dst = self.to_rgb(dst)
        image_sky = self.to_rgb(image_sky)

        # UNTUK MENAMPILKAN GAMBAR MASKING BACKGROUND
        bg = img1_bg.resize((150, 100), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        self.bg_img = Label(self.middle_frame, image=self.bg,text="Masking Background",compound="top")
        self.bg_img.grid(row=4, column=0,pady=5)

        # UNTUK MENAMPILKAN GAMBAR MASKING PESAWAT
        fg = img2_fg.resize((150, 100), Image.ANTIALIAS)
        self.fg = ImageTk.PhotoImage(fg)
        self.fg_img = Label(self.middle_frame, image=self.fg,text="Masking Pesawat",compound="top")
        self.fg_img.grid(row=5, column=0,pady=5)

        # UNTUK MENAMPILKAN GAMBAR GABUNGAN DALAM BENTUK PENJUMLAHAN CITRA ANTARA GAMBAR BG DAN FG
        dst = img_dst.resize((150, 100), Image.ANTIALIAS)
        self.dst = ImageTk.PhotoImage(dst)
        self.dst_img = Label(self.middle_frame, image=self.dst,text="Sum Background Pesawat",compound="top")
        self.dst_img.grid(row=6, column=0,pady=5)

        # MENGGABUNGKAN KEMBALI GAMBAR DARI HASIL PNEJUMALAHAN CITRA KE GAMBAR AWAL / SKY-CLOUD
        fusion = image_sky.resize((550, 500), Image.ANTIALIAS)
        self.sky = ImageTk.PhotoImage(fusion)
        self.fusion_image = Label(self.right_frame, image=self.sky)
        self.fusion_image.grid(row=0, column=0,padx=5)


main_window = Window()
main_window.window.mainloop()
