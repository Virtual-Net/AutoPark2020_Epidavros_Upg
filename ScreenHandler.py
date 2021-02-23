from tkinter import *
import PIL.Image


class ScreenHandler:
    GUI = Tk()
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        console = Button(self.GUI, text='Done', command=endCommand)
        console.pack()

    def processincoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print(msg)
            except self.queue.empty:
                pass
    GUI.mainloop()
