import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

class Handler:
    def __init__(self, window):
        self.window = window
        self.window.title("Paint")
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draws = np.zeros((self.canvas_height, self.canvas_width, 3), dtype=np.uint8)
        self.draws.fill(255)
        self.on_screen = self.draws.copy()
        self.tools = tk.Toplevel(window)
        self.tools.title("Formas")
        self.tools.geometry("200x500")
        self.red_slider = tk.Scale(self.tools, label="Rojo", from_=0, to=255, orient=tk.HORIZONTAL)
        self.red_slider.pack(side=tk.TOP, fill=tk.X)
        self.green_slider = tk.Scale(self.tools, label="Verde", from_=0, to=255, orient=tk.HORIZONTAL)
        self.green_slider.pack(side=tk.TOP, fill=tk.X)
        self.blue_slider = tk.Scale(self.tools, label="Azul", from_=0, to=255, orient=tk.HORIZONTAL)
        self.blue_slider.pack(side=tk.TOP, fill=tk.X)
        self.thickness_scale = tk.Scale(self.tools, label="Grosor", from_=1, to=50, orient=tk.HORIZONTAL)
        self.thickness_scale.pack(side=tk.TOP, fill=tk.X)
        line_button = tk.Button(self.tools, text="Polilinea", width=20, command=lambda: self.select_tool("polilinea"))
        line_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        polyline_button = tk.Button(self.tools, text="Linea", width=20, command=lambda: self.select_tool("linea"))
        polyline_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        rectangle_button = tk.Button(self.tools, text="Rectángulo", width=20, command=lambda: self.select_tool("rectangulo"))
        rectangle_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        circle_button = tk.Button(self.tools, text="Círculo", width=20, command=lambda: self.select_tool("circulo"))
        circle_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        erase_button = tk.Button(self.tools, text="Borrar", width=20, command=lambda: self.select_tool("borrar"))
        erase_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        self.option = ""
        self.canvas.bind("<Button-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.selected_color = (0, 0, 0)
        self.thickness = 1
        
    
    def select_tool(self, option):
        self.option = option

    def select_color(self):
        self.selected_color = (self.red_slider.get(), self.green_slider.get(), self.blue_slider.get())
    
    def select_thickness(self):
        self.thickness = self.thickness_scale.get()

    def on_pressed(self, event):
        self.select_color()
        self.select_thickness()
        x, y = event.x, event.y
        self.inicio = (x,y)
        self.update_canvas()

    def on_release(self, event):
        x, y = event.x, event.y
        if self.option == "polilinea":
            cv2.line(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
            cv2.line(self.draws, self.inicio, (x,y), self.selected_color, self.thickness)
            self.inicio = (x,y)
        if self.option == "linea":
            cv2.line(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
            cv2.line(self.draws, self.inicio, (x,y), self.selected_color, self.thickness)
        if self.option == "rectangulo":
            cv2.rectangle(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
            cv2.rectangle(self.draws, self.inicio, (x,y), self.selected_color, self.thickness)
        if self.option == "circulo":
            d = int(((self.inicio[0] - event.x)**2 + (self.inicio[1] - event.y)**2) ** 0.5)
            r = d // 2
            center_x = (self.inicio[0] + event.x) // 2
            center_y = (self.inicio[1] + event.y) // 2
            s = (center_x, center_y)
            cv2.circle(self.draws, s, r, self.selected_color, self.thickness)
            cv2.circle(self.on_screen, s, r, self.selected_color, self.thickness)
        if self.option == "borrar":
            cv2.line(self.on_screen, self.inicio, (x,y), (255,255,255), self.thickness)
            cv2.line(self.draws, self.inicio, (x,y), (255,255,255), self.thickness)
        self.update_canvas()

        
    def on_motion(self, event):
        x, y = event.x, event.y
        self.on_screen = self.draws.copy()
        if self.option == "polilinea":
            cv2.line(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
            cv2.line(self.draws, self.inicio, (x,y), self.selected_color, self.thickness)
            self.inicio = (x,y)
        if self.option == "linea":
            cv2.line(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
        if self.option == "rectangulo":
            cv2.rectangle(self.on_screen, self.inicio, (x,y), self.selected_color, self.thickness)
        if self.option == "circulo":
            d = int(((self.inicio[0] - event.x)**2 + (self.inicio[1] - event.y)**2) ** 0.5)
            r = d // 2
            center_x = (self.inicio[0] + event.x) // 2
            center_y = (self.inicio[1] + event.y) // 2
            s = (center_x, center_y)
            cv2.circle(self.on_screen, s, r, self.selected_color, self.thickness)
        if self.option == "borrar":
            cv2.line(self.on_screen, self.inicio, (x,y), (255,255,255), self.thickness)
            cv2.line(self.draws, self.inicio, (x,y), (255,255,255), self.thickness)
            self.inicio = (x,y)
        self.update_canvas()
        
    def update_canvas(self):
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.on_screen))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
if __name__ == "__main__":
    window = tk.Tk()
    Handler(window)
    window.mainloop()