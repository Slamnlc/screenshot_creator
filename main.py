import string
import subprocess
import tkinter as tk
import random

from PIL import ImageTk, Image

from config import SCREEN_SIZE, TRANSPARENCY, MOUSE_ICON, FULL_SCREEN_MODE, SCREEN_HEIGHT, SCREEN_WIDTH, \
    BACKGROUND_COLOR, PLATFORM, SCREENSHOT_PATH, SCREENSHOT_FORMAT
from functions import copy_to_clipboard


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.overrideredirect(True)
        self.geometry(SCREEN_SIZE)
        self.attributes("-alpha", TRANSPARENCY)
        self.attributes('-topmost', True)
        self.attributes('-transparent', True)
        self.attributes("-fullscreen", FULL_SCREEN_MODE)

        # self.canvas = self.get_canvas()
        self.canvas = self.get_canvas()
        self.canvas.pack()
        self.color = tk.StringVar(value='red')
        self.arrow = tk.StringVar(value=tk.LAST)

        self.bind('<Escape>', lambda x: self.destroy())
        self.bind("<Button-1>", self.click)
        self.bind("<Command-z>", self.undo)
        self.canvas.tag_bind('line', '<Button-1>', self.select_object)
        self.bind('<space>', self.take_screenshoot)

        self.canvas.bind("<B1-Motion>", self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.button_history = []
        self.draw_history = []
        self.select_history = []

        self.mouse_icon = ImageTk.PhotoImage(file=MOUSE_ICON)
        # self.cimg = self.canvas.create_image(40, 30, image=self.mouse_icon)
        self.canvas.pack()
        # self.canvas.bind('<Motion>', self.mousecoords)

        self.new_item = None
        self.start_point = None
        self.end_point = None

    def get_canvas(self):
        if FULL_SCREEN_MODE:
            return tk.Canvas(width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg=BACKGROUND_COLOR,
                             highlightthickness=0)
        else:
            return tk.Canvas(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=BACKGROUND_COLOR,
                             highlightthickness=0)

    def click(self, event):
        self.start_point = (event.x, event.y)
        print('start')
        if len(self.select_history) > 0:
            self.deselect_object(event)

    def drawing(self, event):
        self.canvas.delete(self.draw_history.pop()) if len(self.draw_history) > 0 else None
        line = (self.start_point[0], self.start_point[1], event.x, event.y)
        # self.new_item = self.canvas.create_line(*line, fill=self.color.get(), arrow=self.arrow.get(), width=2, tag='line')
        # self.new_item = self.canvas.create_rectangle(*line, outline=self.color.get(), width=2, tag='line',
        #                                              fill='')
        print('canm')
        self.create_rectangle(*line, fill='systemTransparent', outline='black', alpha=1)
        self.draw_history.append(self.new_item)

    def stop_drawing(self, event):
        self.draw_history = []
        self.button_history.append(self.new_item)
        self.end_point = (event.x, event.y)
        self.new_item = None

    def undo(self, event):
        self.canvas.delete(self.button_history.pop()) if len(self.button_history) > 0 else None

    def select_object(self, event):
        element_id = self.canvas.find_closest(event.x, event.y)
        coords = self.canvas.coords(element_id)
        if len(coords) > 2:
            rectangle = tuple(coords[i] + 15 if i > 1 else coords[i] - 15 for i in range(len(coords)))
            self.select_history.append(self.canvas.create_rectangle(*rectangle, dash=(6, 4)))

    def deselect_object(self, event):
        coords = tuple(map(lambda x: int(x), self.canvas.coords(self.select_history[0])))
        if event.x not in range(coords[0], coords[2]) or event.y not in range(coords[1], coords[3]):
            self.canvas.delete(self.select_history.pop())

    def move_up(self, event):
        self.canvas.move(self.draw_history[-1], 0, -2)

    def take_screenshoot(self, event):
        if self.start_point[0] > self.end_point[0]:
            region = (self.end_point[0], self.end_point[1],
                      self.start_point[0], self.start_point[1])
        else:
            region = (self.start_point[0], self.start_point[1],
                      self.end_point[0], self.end_point[1])

        tmp_file_name = ''
        self.attributes("-alpha", 0)
        if PLATFORM == 'mac':
            tmp_file_name = f"{SCREENSHOT_PATH}{''.join(random.choices(string.ascii_letters, k=10))}." \
                            f"{SCREENSHOT_FORMAT.lower()}"
            subprocess.call(['screencapture', '-xr', tmp_file_name])

        image = Image.open(fp=tmp_file_name)
        image.resize((self.winfo_screenwidth(), self.winfo_screenheight())).crop(region).save(tmp_file_name)

        print(region)
        self.destroy()
        copy_to_clipboard(tmp_file_name)

    def create_rectangle(self, x1: int, y1: int, x2: int, y2: int, **kwargs):
        if "alpha" in kwargs:
            alpha = int(kwargs.pop("alpha") * 255)
            if "fill" in kwargs:
                fill = kwargs.pop("fill")
            else:
                fill = "white"
            fill = self.canvas.master.winfo_rgb(fill) + (alpha,)
            image = Image.new("RGBA", (x2 - x1, y2 - y1), fill)
            image = ImageTk.PhotoImage(image)
            self.canvas.create_image(x1, y1, image=image, anchor="nw")
        return self.canvas.create_rectangle(self, x1, y1, x2, y2, kwargs)


    def mousecoords(self, event):
        pointxy = (event.x, event.y)
        print(pointxy)
        self.canvas.coords(self.cimg, pointxy)


if __name__ == '__main__':
    main_app = App()
    main_app.mainloop()
