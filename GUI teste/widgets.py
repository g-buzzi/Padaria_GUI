import tkinter as tk


class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, text = "Botão", text_fill = "#000000", text_font = "Arial 12 bold", command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, bg=bg)
        self.command = command
        self.__width = width
        self.__height = height
        self.__cornerradius = cornerradius
        self.__padding = padding
        self.__color = color
        self.__bg = bg
        self.__text = text
        self.__text_fill = text_fill
        self.__text_font = text_font

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        self.create_shape()
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def create_shape(self, inverted = False):
        if inverted:
            fill = self.__text_fill
            text_color = self.__color
        else:
            fill = self.__color
            text_color = self.__text_fill
            self.delete("all")
        rad = 2 * self.__cornerradius
        self.create_polygon((self.__padding, self.__height - self.__cornerradius - self.__padding, self.__padding, self.__cornerradius + self.__padding, self.__padding + self.__cornerradius, self.__padding, self.__width - self.__padding - self.__cornerradius, self.__padding, self.__width - self.__padding, self.__cornerradius + self.__padding, self.__width - self.__padding, self.__height - self.__cornerradius - self.__padding, self.__width - self.__padding - self.__cornerradius, self.__height - self.__padding, self.__padding + self.__cornerradius, self.__height - self.__padding), fill = fill, outline= fill)
        self.create_arc((self.__padding, self.__padding + rad, self.__padding + rad, self.__padding), start=90, extent=90, fill= fill, outline= fill)
        self.create_arc((self.__width - self.__padding - rad, self.__padding, self.__width - self.__padding, self.__padding + rad), start=0, extent=90, fill= fill, outline= fill)
        self.create_arc((self.__width - self.__padding, self.__height - rad - self.__padding, self.__width - self.__padding - rad, self.__height - self.__padding), start=270, extent=90, fill= fill, outline= fill)
        self.create_arc((self.__padding, self.__height - self.__padding - rad, self.__padding + rad, self.__height - self.__padding), start=180, extent=90, fill= fill, outline= fill)
        x0,y0,x1,y1 = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.create_text(x0 + x1/2, y0 + y1/2, text= self.__text, fill = text_color, font= self.__text_font)
        self.configure(width=width, height=height)

    def _on_press(self, event):
        self.create_shape(True)

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()
        self.create_shape()



"""

def botar_texto():
    print("Algo deu certo")

window = tk.Tk()
botao = RoundedButton(window, 100, 100, 10, 0,"#3a312c", "#FFFFFF", text = "Ingredientes", text_fill = "#f99525", command = botar_texto)
botao.pack()
window.mainloop()
"""