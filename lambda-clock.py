import os
from datetime import datetime
import time
from colorsys import hsv_to_rgb
from random import random

import colors
import fonts

# TODO: Command line arguments
# TODO: Date 
# TODO: New fonts
# TODO: New Colors

characters = {
    # hexadecimal numbers are equal to the numbers without \n in the comments
    "1": 0x46108e, # "00100\n01100\n00100\n00100\n11111",
    "2": 0xe8889f, # "01110\n10001\n00010\n00100\n11111",
    "3": 0x1e0f83e, # "11110\n00001\n11110\n00001\n11110",
    "4": 0x118f821, # "10001\n10001\n11110\n00001\n00001",
    "5": 0xf8783e, # "01111\n10000\n11110\n00001\n11110",
    "6": 0xe87a2e, # "01110\n10000\n11110\n10001\n01110",
    "7": 0x1e11110, # "11110\n00010\n00100\n01000\n10000",
    "8": 0xe8ba2e, # "01110\n10001\n01110\n10001\n01110",
    "9": 0xe8bc2e, # "01110\n10001\n01111\n00001\n01110",
    "0": 0xe8c62e, # "01110\n10001\n10001\n10001\n01110",
    ":": 0x20080, # "00000\n00100\n00000\n00100\n00000",
}

def clearConsole():
    # clear the console
    # if the system is windows use cls
    # if linux use clear
    os.system('cls' if os.name=='nt' else 'clear')

def complete(s):
    # complete the converted string to 25 chars (5*5)
    # by adding zeros to begining of the string
    return "0" * (25 - len(s)) + s

def hex2cistr(h):
    # hex to complete string of int
    # convert hexadecimal number to binary string
    # cut the first 2 character (0b) and complete to 25 character (5 * 5)
    return complete(str(bin(int(h,16)))[2:])

def colorize(text, color):
    # colorize the string
    return f"{colors.colors[color]}{text}{colors.Stop}"

def hsv2ansi(h,s,v):

    r,g,b = hsv_to_rgb(h,s,v)

    return f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"

def gradient(clockstr,**kwargs):
    
    # TODO: circular gradient
    hue_start,hue_spread,saturation_start,saturation_spread = kwargs["hue_start"],kwargs["hue_spread"],kwargs["saturation_start"],kwargs["saturation_spread"]
    lines = clockstr.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    totalrc = cols + rows

    a = []
    for i,row in enumerate(lines):
        b = ""
        for j,c in enumerate(row):
            irow = i/rows
            jcol = j/cols
            totalij = i + j

            if kwargs["gradient-style"] == "horizontal":
                h = hsv2ansi(hue_start + hue_spread*jcol, saturation_start + saturation_spread*irow, 1)

            elif kwargs["gradient-style"] == "vertical":
                h = hsv2ansi(hue_start + hue_spread*irow, saturation_start + saturation_spread*jcol, 1)

            elif kwargs["gradient-style"] == "diagonal":
                h = hsv2ansi(hue_start + totalij*hue_spread/totalrc, totalij*saturation_spread/totalrc + saturation_start, 1)
            
            elif kwargs["gradient-style"] == "reverse-diagonal":
                h = hsv2ansi(hue_start + (totalrc - j + i)*hue_spread/totalrc, (totalrc - j + i)*saturation_spread/totalrc + saturation_start, 1)
            
            b += f"{h}{c}{colors.Stop}"
        a.append(b)
    
    return "\n".join(a)

def colorize_characters(chars,color):
    # colorizes lines by given color (lines from splitby5)
    return [colorize(i,color) for i in chars]

def splitby5(s):
    # splits the string by 5 characters
    return [s[j:j+5] for j in range(0, len(s), 5)]

def convef(n,**kwargs):
    # converts the string with ones and zeros to given characters
    return n.replace("0",kwargs["empty-character"]).replace("1",kwargs["full-character"])

def mergeLines(t,spacing):
    # merges the converted and splitted text lines by lines with spacing
    # and joins with new line character (\n)
    
    #                              using zip to
    #                              get same line for
    #                              all chars                    5 line
    #                                   |                         |
    #                                   v                         v
    rt = "\n".join([spacing.join(list(zip(*t))[i]) for i in range(5)])
    return rt

def clock(ctime,**kwargs):

    # for every char in current time convert to string by hex2cistr
    # then convert them to empty - full chars
    # then split by 5
    # then merge
    # colorize lines (before merging or after merging)
    style = kwargs["coloring"]
    spacing = kwargs["spacing"]
    if style == "default":

        lines = [colorize_characters(splitby5(convef(hex2cistr(hex(characters[c])),**kwargs)),colors.character_colors[c]) for c in ctime]
        ml = mergeLines(lines,spacing)

    elif style == "gradient":
        
        lines = [splitby5(convef(hex2cistr(hex(characters[c])),**kwargs)) for c in ctime]
        ml = gradient(mergeLines(lines,spacing),**kwargs)
        
    return ml

def align(cl, size, **kwargs):
    # w:
    # 1 2 3
    # 4 5 6 
    # 7 8 9
    w = kwargs["position"]
    lenspacing = len(kwargs["spacing"])

    col, row = size

    if kwargs["clock-mode"] in ["seconds","s"]:

        clock_row_length = 40 + 7 * lenspacing # 8 (character) * 5 (width of character) + 7 (spacing) * length of the spacing string

    elif kwargs["clock-mode"] in ["microseconds","ms"]:

        clock_row_length = 75 + 9 * lenspacing # 15 (character) * 5 (width of character) + 9 (spacing) * length of the spacing string

    if w == "default" or w == "1" or w == 1:
        w = "top-left"
    elif w == "2" or w == 2:
        w = "top-center"
    elif w == "3" or w == 3:
        w = "top-right"
    elif w == "4" or w == 4:
        w = "center-left"
    elif w == "center" or w == "5" or w == 5:
        w = "center-center"
    elif w == "6" or w == 6:
        w = "center-right"
    elif w == "7" or w == 7:
        w = "bottom-left"
    elif w == "8" or w == 8:
        w = "bottom-center"
    elif w == "9" or w == 9:
        w = "bottom-right"

    v,h = w.split("-")

    if v == "top":
        top_padding = ""
    elif v == "center":
        top_padding = int((row - 5)/2) * "\n"
    elif v == "bottom":
        top_padding = int(row - 5) * "\n"

    if h == "left":
        left_padding = ""
    elif h == "center":
        left_padding = int((col - clock_row_length) / 2) * " "
    elif h == "right":
        left_padding = int(col - clock_row_length) * " "

    return top_padding + "\n".join([left_padding + t for t in cl.split("\n")])

if __name__ == "__main__":

    clock_settings = {
        "clock-mode": "s",
        "hue_start":0,
        "hue_spread":0.1,
        "saturation_start":1,
        "saturation_spread":0.0,
        "spacing": " ",
        "position": 5,
        "coloring": "gradient",
        "empty-character": " ",
        "full-character": fonts.fonts["full-block"],
        "gradient-style": "diagonal",
    }

    try:

        clearConsole()
        while True:


            tsize = os.get_terminal_size()
            if clock_settings["clock-mode"] in ["seconds","s"]:
                timestr = "%H:%M:%S"
            elif clock_settings["clock-mode"] in ["microseconds","ms"]:
                timestr = "%H:%M:%S:%f"

            current_time = datetime.now().strftime(timestr)

            sclock = clock(current_time,**clock_settings)
            aclock = align(sclock,tsize,**clock_settings)

            print("\033[2J\033[?25l\033[0;0H" + aclock, flush=True)

            if clock_settings["clock-mode"] in ["seconds","s"]:
                time.sleep(1)

    except KeyboardInterrupt:

        print('Clock is stopped!')
    