#!/usr/bin/python3
# -*- coding: utf-8 -*-

# python mouse autoclicker

import pynput
import time as t


mouse = pynput.mouse.Controller()

breakloop, pause = False, False
def stop1(*args):
    global breakloop
    if str(args[0]) == "Key.enter":
        breakloop = True
        mlistener.stop()
        return False

svg = []
def save(x, y, k, p):
    global svg
    if breakloop:
        return False
    # p = pressed
    if p:
        svg.append((x, y))

delay = float(input("Enter the delay between clicks: "))
print("Click a serie of points and press Enter and reclick to go")
with pynput.mouse.Listener(on_click=save) as mlistener,\
     pynput.keyboard.Listener(on_press=stop1) as kblistener:
    mlistener.join()
    kblistener.join()

def stop(*args):
    global breakloop, pause
    try:
        if str(args[0]) == "'p'":
            pause = not pause
            print("OFF" if pause else "ON")
        elif str(args[0]) == "'s'":
            breakloop = True
            return False
    except:
        pass

def loop(*args):
    for coord in svg:
        if breakloop == True:
            return False
        if pause:
            break
        mouse.position = coord
        mouse.press(pynput.mouse.Button.left)
        mouse.release(pynput.mouse.Button.left)
        t.sleep(delay)

breakloop = False

with pynput.mouse.Listener(on_click=loop) as mlistener,\
     pynput.keyboard.Listener(on_press=stop) as kblistener:
    mlistener.join()
    kblistener.join()
