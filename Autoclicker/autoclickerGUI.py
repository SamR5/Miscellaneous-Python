#!/usr/bin/python3
# -*- coding: utf-8 -*-

# autoclicker application with GUI
# when GUI not focused, press 'p' to pause or 's' to stop

import tkinter as tk
import pynput
import threading
import subprocess as sp

keyboard = pynput.keyboard.Controller()

class AutoClicker():
    """"""
    def __init__(self, master):
        self.master = master
        self.pause = False # to start/pause the autoclicker
        self.breakloop = False # stop autoclicker and use keyboard freely
        self.gui()

    def gui(self):
        """"""
        tk.Label(self.master, text="h").grid(row=0, column=0)
        self.hourSb = tk.Spinbox(self.master, from_=0, to=23, width=4)
        self.hourSb.grid(row=1, column=0)
        tk.Label(self.master, text="min").grid(row=0, column=1)
        self.minSb = tk.Spinbox(self.master, from_=0, to=59, width=4)
        self.minSb.grid(row=1, column=1)
        tk.Label(self.master, text="s").grid(row=0, column=2)
        self.secSb = tk.Spinbox(self.master, from_=0, to=59, width=4)
        self.secSb.grid(row=1, column=2)
        tk.Label(self.master, text="ms").grid(row=0, column=3)
        self.msSb = tk.Spinbox(self.master, from_=0, to=999, width=4)
        self.msSb.grid(row=1, column=3)
        
        tk.Button(self.master, text="Start", command=self.start)\
          .grid(row=2, column=0, columnspan=2)
        tk.Button(self.master, text="Stop", command=self.stop)\
          .grid(row=2, column=2, columnspan=2)
    
    def get_delay(self):
        """Get the delay between click from the spinboxes in ms"""
        time = int(self.hourSb.get()) * 3600 * 1000 +\
               int(self.minSb.get()) * 60 * 1000 +\
               int(self.secSb.get()) * 1000 +\
               int(self.msSb.get())
        return time
    
    def click(self, *args):
        """click once"""
        if self.pause:
            self.master.after(100, self.click)
            return
        elif self.breakloop:
            self.delay = 0
            return
        elif 0 < self.delay < 50:
            sp.call(["xdotool", "click",
                  "--repeat", str(int(500 / self.delay)),
                  "--delay", str(self.delay),
                  "1"])
        else:
            sp.Popen(["xdotool", "click", "1"])
        self.master.after(self.delay, self.click)
    
    def start(self, *args):
        """"""
        self.breakloop = True
        self.pause = False
        self.delay = self.get_delay()
        if self.delay == 0:
            return
        self.pause = False
        self.breakloop = False
        self.master.after(1000, self.click)
    
    def stop(self, *args):
        """"""
        self.pause = True
        self.breakloop = True

class KeyboardShortcut():
    """"""
    def __init__(self, app):
        self.app = app # app to communicate with
        with pynput.keyboard.Listener(on_press=self.start_stop) as kbLst:
            kbLst.join()
    
    def start_stop(self, *args):
        try:
            if str(args[0]) == "'p'":
                self.app.pause = not self.app.pause
            elif str(args[0]) == "'s'":
                self.app.breakloop = True
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Autoclicker")
    root.resizable(False, False)
    app = AutoClicker(root)
    
    th = threading.Thread(target=lambda: KeyboardShortcut(app))
    th.setDaemon(True)
    th.start()
    
    root.mainloop()
