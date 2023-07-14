import argparse
import cv2
import numpy as np
import pytesseract as pt
import tkinter as tk
from PIL import ImageGrab
from time import sleep
from translate import Translator

# translate package takes different language codes than tesseract
# so map translate: tesseract codes
# TODO: add more languages :)
languages = {
    "en": "eng",  # english
    "da": "dan",  # danish
    "de": "deu",  # german
    "es": "spa",  # spanish
}


class App:
    def __init__(self, from_lang, to_lang="en", wait_time=3, x=400, y=100, y_offset=38):
        """Creates translator app

        :param from_lang: Two-letter language code of origin language
        :param to_lang: Two-letter language code of desired result language,
            defaults to "en"
        :param wait_time: Time in seconds to wait between screen captures,
            defaults to 3.
        :param x: Width in pixels of init window
        :param y: Height in pixels of init window
        :param y_offset: Currently unused. Height in pixels of menu bar
            with which to offset Y coordinates for screen capture, defaults to 38
        """
        self.x, self.y, self.y_offset = x, y, y_offset
        self.to_lang = to_lang
        self.from_lang = from_lang
        self.wait_time = wait_time

        self.translator = Translator(to_lang=self.to_lang, from_lang=self.from_lang)

        # create init window
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.4)
        self.root.wm_attributes("-topmost", True)
        self.root.title("Subtitle Translator")
        # center window on screen
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        self.root.geometry(f"{x}x{y}+{(ws-x)//2}+{(hs-y)//2}")
        # create text and background on window
        self.canvas_bg = tk.Canvas(self.root, background="green", highlightthickness=0)
        self.canvas = tk.Canvas(
            self.root, background="green", highlightthickness=0, width=x, height=y
        )
        text = self.canvas.create_text(
            x / 2,
            y / 2,
            text="Resize this window around subtitles\nClick here when done",
            font="Helvetica 18 bold",
            anchor=tk.CENTER,
            justify="center",
            fill="white",
        )
        self.canvas_bg.pack(fill="both", expand=True)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # show window and set button click action
        self.root.deiconify()
        self.canvas.tag_bind(text, "<ButtonPress-1>", self.on_click)

    def on_click(self, event):
        self.x, self.y, self.w, self.h = (
            self.root.winfo_x(),
            self.root.winfo_y(),
            self.root.winfo_width(),
            self.root.winfo_height(),
        )
        # clean up init window
        self.root.withdraw()
        self.canvas_bg.destroy()
        self.canvas.destroy()
        # set attributes for transparent window
        self.root.attributes("-alpha", 1)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparent", True)
        self.root.config(bg="systemTransparent")
        self.label = None

        self.loop()

    def get_image(self):
        # TODO: unclear if this requires an offset to account for menu bar
        image = ImageGrab.grab(
            (
                self.x,
                self.y,
                # self.y + self.y_offset,
                self.x + self.w,
                self.y + self.h,
                # self.y + self.h + self.y_offset,
            )
        ).convert("RGB")
        # Filter image with blur and threshold to improve OCR quality
        image = cv2.cvtColor(np.array(image)[:, :, ::-1], cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        threshold, filtered = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # white on black -> black on white
        filtered = 255 - filtered
        return filtered

    def get_text(self, image):
        text = pt.image_to_string(image, lang=languages[self.from_lang])
        translated = self.translator.translate(text)
        return translated

    def show_text(self, text):
        # add caption to window
        self.label = tk.Label(
            self.root,
            text=text,
            font="Helvetica 18",
            bg="black",
            fg="white",
        )
        self.label.config(anchor=tk.CENTER)
        self.label.pack()
        # place window on top of others
        self.root.wm_attributes("-topmost", True)
        # TODO: add close button
        self.root.deiconify()

    def hide_text(self):
        self.root.withdraw()
        if self.label:
            self.label.destroy()

    def loop(self):
        """Main loop: capture image, OCR and translate text, show new subtitles"""
        while True:
            image = self.get_image()
            text = self.get_text(image)
            self.show_text(text)
            sleep(self.wait_time)
            self.hide_text()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # TODO: add this selection to tk ui
    parser = argparse.ArgumentParser(
        prog="python subtitle_translator.py",
        description="Live translation with screen capture and OCR",
    )
    parser.add_argument(
        "-f",
        "--from-lang",
        default="da",
        help="Two-letter language code of origin language (default 'da')",
        choices=languages.keys(),
    )
    parser.add_argument(
        "-t",
        "--to-lang",
        default="en",
        help="Two-letter language code of desired result languagen (default 'en')",
        choices=languages.keys(),
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        default=3,
        type=int,
        help="Time in seconds to wait between screen captures (default 3)",
    )
    args = parser.parse_args()

    app = App(args.from_lang, args.to_lang, wait_time=args.wait_time)
    app.run()
