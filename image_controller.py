import cv2

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import time

class ImageController():
    instances = {}
    active_instance_name = None

    @staticmethod
    def get_instance(winname):
        assert(isinstance(winname, str))
        if winname not in ImageController.instances.keys():
            ImageController.instances[winname] = ImageController(winname)
        ImageController.active_instance_name = winname
        return ImageController.instances[winname]

    @staticmethod
    def get_active_instance():
        return ImageController.get_instance(ImageController.active_instance_name)

    @staticmethod
    def imshow(winname, image):
        ImageController.get_instance(winname)._imshow(image)

    @staticmethod
    def waitKeyEx(delay):
        # self.frame.master = win
        ImageController.get_active_instance()._waitKeyEx(delay)

    def __init__(self, winname):
        self.root = tk.Tk()
        self.root.title(winname)

        self.frame = tk.Frame(master=self.root, bg="red")

        # Load an image in the script
        self.img_ratio = 4/4
        self.canvas_shape_hw = [720, int(720*self.img_ratio)]
        self.canvas = tk.Canvas(master=self.frame, height=self.canvas_shape_hw[0], width=self.canvas_shape_hw[1], bg="blue")
        self.imgtk = None
        self.zoom_factor = None
        img = np.zeros(shape=(100, 100, 3), dtype=np.uint8)
        self._imshow(img)


        self.ctrl_frame = tk.Frame(master=self.frame, bg="green")

        self.frame.pack()
        self.canvas.pack(side=tk.LEFT)
        self.ctrl_frame.pack()

    def callback(self):
        pass

    def _addbutton(self, text='Button', command=None):
        tk.Button(self.ctrl_frame, text=text, command=command).pack(padx=10, pady=10, )

    def _imshow(self, img, mode="fit"):
        ch, cw = self.canvas_shape_hw[:2]
        ih, iw = img.shape[:2]
        if mode == "fit":
            self.zoom_factor = min(ch/ih, cw/iw)
        elif mode == "fill":
            self.zoom_factor = max(ch/ih, cw/iw)

        img = cv2.resize(img, None, fx=self.zoom_factor, fy=self.zoom_factor, interpolation=cv2.INTER_LINEAR)

        self.imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.canvas.create_image(self.canvas_shape_hw[1] // 2, self.canvas_shape_hw[0] // 2, anchor=tk.CENTER,
                                 image=self.imgtk)

    def _waitKeyEx(self, delay):
        # TODO: mimic cv2.waitLeyEx behavior
        def keydown(event):
            print("keydown", event)
        def keyup(event):
            print("keyup", event)

        self.root.bind("<KeyPress>", keydown)
        self.root.bind("<KeyRelease>", keyup)

        if delay > 0:
            self.root.after(delay, lambda: self.root.destroy())

        self.root.mainloop()

