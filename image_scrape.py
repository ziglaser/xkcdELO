import requests
import os
from bs4 import BeautifulSoup as bs
import wget
import random
from PIL import Image, ImageTk
import tkinter as tk
import shutil
import csv


comic_location = 'C:\\Users\\zglas\\Pictures\\xkcd'

results = []

def img_link(xkcd_link):
    soup = bs(requests.get(xkcd_link).content, "html.parser")
    return "https:" + soup.find(id='comic').find('img').attrs.get('src')


def clear_imgs():
    try:
        shutil.rmtree(comic_location)
    except FileNotFoundError:
        pass
    os.mkdir(comic_location)


def download_comic(num):
    download_address = img_link("https://www.xkcd.com/" + str(num))
    wget.download(download_address, out=comic_location)


def left_wins(comics):
    print(comics)
    results.append([comics[0], comics[1]])
    reconfigure_buttons()


def right_wins(comics):
    print(comics)
    results.append([comics[1], comics[0]])
    reconfigure_buttons()


def find_photos():
    clear_imgs()

    xkcd_limit = 2340
    images = []

    comic_index_1 = random.randint(1, xkcd_limit)
    download_comic(comic_index_1)
    images.append(Image.open(comic_location + "\\" + os.listdir(comic_location)[0]))
    title_1 = os.listdir(comic_location)[0]

    comic_index_2 = random.randint(1, xkcd_limit)
    download_comic(comic_index_2)
    if os.listdir(comic_location)[0] != title_1:
        images.append(Image.open(comic_location + "\\" + os.listdir(comic_location)[0]))
    else:
        images.append(Image.open(comic_location + "\\" + os.listdir(comic_location)[1]))

    photos = [ImageTk.PhotoImage(image) for image in images]
    return photos, (comic_index_1, comic_index_2)


# init
root = tk.Tk()

photos, comic_indices = find_photos()

# button with image binded to the same function
b1 = tk.Button(root, image=photos[0], command=lambda: left_wins(comic_indices))
b1.grid(row=0, column=0)
b2 = tk.Button(root, image=photos[1], command=lambda: right_wins(comic_indices))
b2.grid(row=0, column=1)


def reconfigure_buttons():
    photos, comic_indices = find_photos()
    b1.config(image=photos[0], command=lambda: left_wins(comic_indices))
    b2.config(image=photos[1], command=lambda: right_wins(comic_indices))
    tk.update()

# button with text closing window
b = tk.Button(root, text="Close", command=root.destroy)
b.grid(row=1)

# "start the engine"
root.mainloop()

with open('xkcd_h2h.csv', 'a+', newline='') as f:
    write = csv.writer(f)
    write.writerows(results)
