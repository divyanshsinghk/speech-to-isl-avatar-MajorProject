import os
import time
from PIL import Image, ImageTk
import tkinter as tk

IMAGE_DIR = "fingerspelling_images"

def display_fingerspelling(signs):
    root = tk.Tk()
    root.title("ISL Fingerspelling Output")

    label = tk.Label(root)
    label.pack()

    for sign in signs:
        if sign.startswith("FS_"):
            letter = sign[3]
            img_path = os.path.join(IMAGE_DIR, f"{letter}.png")

            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((300, 300))
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
                root.update()
                time.sleep(1)

    root.mainloop()
