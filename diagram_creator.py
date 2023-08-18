import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

IMAGE_FILE_NAME = "image.png"
SAVE_NAME = "save_image"
IMAGE_SCALE_FACTOR = 0.5
RECTANGLE_THICKNESS = 4

img = None

class ImageCreator:
    def __init__(self, root):
        global img
        
        self.root = root
        self.root.title("Match Image Creator")

        self.im = Image.open(IMAGE_FILE_NAME)
        width, height = self.im.size
        self.im = self.im.resize((int(width*IMAGE_SCALE_FACTOR), int(height*IMAGE_SCALE_FACTOR)))
        root.geometry(f"{int(width*IMAGE_SCALE_FACTOR)}x{int(height*IMAGE_SCALE_FACTOR)}")
        
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        img = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.root.bind('<Escape>', self.close_window)
        
        self.holding = False
        self.last_x, self.last_y = None, None

        self.points = []
        
    def start_drawing(self, event):
        self.holding = True
        self.last_x, self.last_y = event.x, event.y
        self.current_rectangle = None
        
    def draw(self, event):
        if self.holding and self.last_x is not None and self.last_y is not None:
            self.x, self.y = event.x, event.y
            self.canvas.delete(self.current_rectangle)
            self.current_rectangle = self.canvas.create_rectangle(self.last_x, self.last_y, self.x, self.y, width=RECTANGLE_THICKNESS)
            
    def stop_drawing(self, event):
        self.holding = False
        self.points.append([self.last_x, self.last_y, self.x, self.y])
        self.last_x, self.last_y = None, None

    def close_window(self, e):
        lines = [",".join([str(e) for e in line])+"\n" for line in self.points]
        with open(SAVE_NAME+".csv", "w") as f:
            f.writelines(lines)

        d = ImageDraw.Draw(self.im)
        for line in self.points:
            d.rectangle(line, outline="black", width=RECTANGLE_THICKNESS)
        self.im.save(SAVE_NAME+".png")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCreator(root)
    root.mainloop()
