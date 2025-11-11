import os
import time
from tkinter import *
from PIL import Image, ImageTk


class LoadingScreen:
    def __init__(self, root=None, duration=2):
        self.root = root
        self.duration = duration  # seconds
        self.loading_screen = Tk() if root is None else Toplevel(root)
        self.width = 427
        self.height = 250

        # center the window
        screen_w = self.loading_screen.winfo_screenwidth()
        screen_h = self.loading_screen.winfo_screenheight()
        x = (screen_w / 2) - (self.width / 2)
        y = (screen_h / 2) - (self.height / 2)
        self.loading_screen.geometry(f"{self.width}x{self.height}+{int(x)}+{int(y)}")
        self.loading_screen.overrideredirect(True)

        # Load UI
        self.build_ui()

        # Animation state
        self.start_time = None
        self.current_dot = 0

    def build_ui(self):
        self.frame = Frame(self.loading_screen, width=self.width, height=self.height, bg='#00041A')
        self.frame.place(x=0, y=0)

        base_path = os.path.join(os.path.dirname(__file__), "images")
        bg_image_path = os.path.join(base_path, "bg.png")
        image_a_path = os.path.join(base_path, "image1.png")
        image_b_path = os.path.join(base_path, "image2.png")

        bg_image = Image.open(bg_image_path).resize((self.width, self.height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        Label(self.loading_screen, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)

        # Loading dot images
        dot_width = 20
        dot_height = 20
        image_a = Image.open(image_a_path).resize((dot_width, dot_height), Image.LANCZOS)
        image_b = Image.open(image_b_path).resize((dot_width, dot_height), Image.LANCZOS)

        # Preserve the image transparency
        bg_color = (0, 0, 0, 0)  # fully transparent
        image_a_rgba = Image.new("RGBA", (dot_width, dot_height), bg_color)
        image_a_rgba.paste(image_a, (0, 0), image_a)

        image_b_rgba = Image.new("RGBA", (dot_width, dot_height), bg_color)
        image_b_rgba.paste(image_b, (0, 0), image_b)

        # Convert to Tkinter images
        self.image_a = ImageTk.PhotoImage(image_a_rgba)
        self.image_b = ImageTk.PhotoImage(image_b_rgba)

        self.label_loading = Label(self.loading_screen, text="Loading...", fg="white", bg="#00041A")
        self.label_loading.configure(font=("Arial", 14))
        self.label_loading.place(x=175, y=120)

        # dots
        self.dots = [Label(self.loading_screen, image=self.image_b, border=0, relief=SUNKEN) for _ in range(4)]
        x_pos = 180
        for dot in self.dots:
            dot.place(x=x_pos, y=160)
            x_pos += 20

    def show(self):
        self.start_time = time.time()
        self.animate_dot()  # start animation loop
        self.loading_screen.mainloop()

    def animate_dot(self):
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.destroy()
            return

        # update dots
        for i, dot in enumerate(self.dots):
            dot.config(image=self.image_a if i == self.current_dot else self.image_b)
        self.current_dot = (self.current_dot + 1) % 4

        # schedule next update
        self.loading_screen.after(400, self.animate_dot)

    def destroy(self):
        self.loading_screen.destroy()




