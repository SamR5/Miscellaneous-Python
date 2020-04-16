#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import time as t
import datetime as dt


class Timer():
    """Class representing a timer"""
    def __init__(self, master):
        self.master = master
        self._start = t.time()
        self.pausedTime = self._start
        self._running = 0
        self.laps = 1
        self.lapsLabelsList = []
        self.lapBox = tk.Listbox(self.master, font='courier', width=25)
        self.lapBox.grid(row=4, column=1, columnspan=2, pady=10)
        self.gui()

    def start_pause(self):
        """Start/pause the stopwatch"""
        if not self._running:
            self._start = t.time()
            self.pausedTime = self._start
            self.lastLap = self._start
            try:
                self.lastLap -= self.pausedTime - t.time()
            except:
                pass
            self._running = 1
            self.SPLab.set("Pause")
            self.LRLab.set("Lap")
            self._update()
        else:
            self._running = 0
            self.SPLab.set("Start")
            self.LRLab.set("Reset")
            self.pausedTime = t.time()

    def lap_reset(self):
        """Save a lap or reset the timer"""
        if self._running:
            # difference from the last lap
            try:
                theTime = t.time() - self.lastLap
                h = int(theTime//3600)
                m = int(theTime//60 - h * 60)
                s = str(theTime - m * 60).split('.')
                s = s[0].zfill(2) + '.' + s[1][:2].zfill(2)
                h, m = str(h).zfill(2), str(m).zfill(2)
                if h == '00':
                    differenceFromLast = ":".join((m, s))
                else:
                    differenceFromLast =  ":".join((h, m, s))

            except: # for the first lap
                differenceFromLast = self._elapsedtime.get()
            
            self.lapBox.insert(-1, str(str(self.laps) + ".").ljust(5, " ") +\
                               self._elapsedtime.get() + '   ' +\
                               differenceFromLast)
            self.lapBox.see(0)
            self.laps += 1
            self.lastLap = t.time()
        else:
            self._elapsedtime.set("00:00.0")
            self._running = 0
            self.laps = 1
            self.lapBox.delete(0, 'end')

    def save(self):
        """Save the laps in a txt file"""
        fullNow = dt.datetime.now()
        now = "".join((str(fullNow.year)[2:],
                       str(fullNow.month).zfill(2),
                       str(fullNow.day).zfill(2))) + " " +\
              "-".join((str(fullNow.hour).zfill(2),
                        str(fullNow.minute).zfill(2),
                        str(fullNow.second).zfill(2)))              
        with open(now + ".txt", 'w') as mylaps:
            for lap in range(self.laps-2, -1, -1):
                mylaps.write(self.lapBox.get(lap) + "\n")
    
    def _update(self): 
        """Update the label with elapsed time."""
        if self._running:
            theTime = round(t.time() - self._start, 2)
            h = int(theTime//3600)
            m = int(theTime//60 - h * 60)
            s = str(theTime - m * 60).split('.')
            s = s[0].zfill(2) + '.' + s[1][:2].zfill(2)
            h, m = str(h).zfill(2), str(m).zfill(2)
            if h == '00':
                self._elapsedtime.set(":".join((m, s)))
            else:
                self._elapsedtime.set(":".join((h, m, s)))
            
            self.master.after(20, self._update)
    
    def gui(self):
        """"""
        self._elapsedtime = tk.StringVar()
        self._elapsedtime.set("00:00.00")
        self.SPLab = tk.StringVar()
        self.SPLab.set("Start")
        self.LRLab = tk.StringVar()
        self.LRLab.set("Reset")
        self.startB = tk.Button(self.master, textvariable=self.SPLab,
                                width=10, relief="groove", bg="blue",
                                fg='green', font=("calibri", 10, "bold"),
                                command=self.start_pause)
        self.resetB = tk.Button(self.master, textvariable=self.LRLab,
                                width=10, bg="blue", relief="groove",
                                font=("calibri", 10, "bold"), fg='green',
                                command=self.lap_reset)
        self.saveB = tk.Button(self.master, text='Save', bg='blue', fg='green',
                               font=("calibri", 10, "bold"),
                               command=self.save)
    
        self.startB.grid(row=2, column=1, padx=10, pady=5)
        self.resetB.grid(row=2, column=2, padx=10, pady=5)
        self.saveB.grid(row=5, column=1, columnspan=2, pady=5)
    
        self.chrono = tk.Label(self.master, textvariable=self._elapsedtime,
                               justify="center", font=("calibri", 25),
                               bg='green', fg="blue")
        self.chrono.grid(row=1, column=1, columnspan=2, pady=15)
        tk.Label(self.master, bg='green').grid(row=1, column=0, padx=15)
        tk.Label(self.master, bg='green').grid(row=1, column=3, padx=15)
        tk.Label(self.master, bg='green').grid(row=0, column=1, pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Timer")
    root.configure(bg='green')
    T = Timer(master=root)
    root.resizable(False, False)
    root.mainloop()

