import tkinter as tk
from PIL import Image, ImageTk

img = None

MARGIN = 100 # can be this many pixels away from the correct position in any direction
HORIZONTAL_PADDING = 300
VERTICAL_PADDING = 100
FILE_NAME = "save_image"
SPACING_BETWEEN_IMAGES = 100

class Match:
    # coords, dimensions, and home_coords are all tuples of (x, y) coordinates
    def __init__(self, coords, dimensions, home_coords, image_segment, canvas):
        global img
        
        self.dimensions = dimensions
        self.correct_coords = [coord + dim/2 for coord, dim in zip(coords, dimensions)]
        self.home_coords = home_coords
        self.x = home_coords[0]
        self.y = home_coords[1]
        self.in_correct_spot = False
        self.image_segment = image_segment
        self.canvas = canvas

        self.photo_image = ImageTk.PhotoImage(image_segment)
        self.image_canvas_object = self.canvas.create_image(self.x, self.y, image=self.photo_image)

    def check_match(self):
        if self.distance_from(self.correct_coords[0], self.correct_coords[1]) < MARGIN:
            self.move_image(self.correct_coords[0], self.correct_coords[1])
            self.in_correct_spot = True
        else:
            self.move_image(self.home_coords[0], self.home_coords[1])

    def distance_from(self, x, y):
        return ((self.x - x)**2+(self.y - y)**2)**0.5

    def move_image(self, x, y):
        if not self.in_correct_spot:
            self.canvas.move(self.image_canvas_object, x - self.x, y - self.y)
            self.x = x
            self.y = y
        
class DiagramMatcher:
    def __init__(self, root):
        global img
        
        self.root = root
        self.root.title("Drag and Drop Matching")

        self.im = Image.open(FILE_NAME+".png")
        width, height = self.im.size
        root.geometry(f"{width+HORIZONTAL_PADDING}x{height+VERTICAL_PADDING}")
        
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        img = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        with open(FILE_NAME+".csv", "r") as f:
            lines = f.readlines()
            points_str = [line[:-1].split(",") for line in lines]
            points = [[int(i) for i in line] for line in points_str]

        self.matches = []
        image_number = 1
        for match_coords in points: # needs to be run first or later created rectangles will occlude earlier created match images
            self.canvas.create_rectangle(match_coords[0], match_coords[1], match_coords[2], match_coords[3], fill="grey")

        for match_coords in points:
            image_segment = self.im.crop(tuple(match_coords))
            self.matches.append(Match((match_coords[0], match_coords[1]),
                                      (match_coords[2] - match_coords[0], match_coords[3] - match_coords[1]),
                                      (width+HORIZONTAL_PADDING/2, image_number*SPACING_BETWEEN_IMAGES),
                                      image_segment,
                                      self.canvas))
            image_number += 1

    def on_button_press(self, event):
        self.drag_index = self.matches.index(sorted(self.matches, key=lambda match: match.distance_from(event.x, event.y))[0])

    def on_mouse_drag(self, event):
        self.matches[self.drag_index].move_image(event.x, event.y)

    def on_button_release(self, event):
        self.matches[self.drag_index].check_match()
        self.drag_index = len(self.matches)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramMatcher(root)
    root.mainloop()
