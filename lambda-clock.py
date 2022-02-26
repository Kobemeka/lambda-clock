import os
from datetime import datetime
import time
from colorsys import hsv_to_rgb
from random import random
import argparse

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
    " ": 0x00000,
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
    hue_start,hue_spread,saturation_start,saturation_spread = kwargs["hue_start"],kwargs["hue_spread"],kwargs["saturation-start"],kwargs["saturation-spread"]
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

        lines = [splitby5(convef(hex2cistr(hex(characters[c])),**kwargs)) for c in ctime]
        ml = mergeLines(lines,spacing)
        
    elif style == "predefined":

        lines = [colorize_characters(splitby5(convef(hex2cistr(hex(characters[c])),**kwargs)),colors.character_colors[c]) for c in ctime]
        ml = mergeLines(lines,spacing)

    elif style == "gradient":
        
        lines = [splitby5(convef(hex2cistr(hex(characters[c])),**kwargs)) for c in ctime]
        ml = gradient(mergeLines(lines,spacing),**kwargs)
        
    return ml

def align(cl, size, **kwargs):
    w = kwargs["position"]
    lenspacing = len(kwargs["spacing"])

    col, row = size

    if kwargs["clock-format"] == "s":

        clock_row_length = 40 + 7 * lenspacing
    elif kwargs["clock-format"] == "ms":

        clock_row_length = 75 + 9 * lenspacing

    elif kwargs["clock-format"] == "m":

        clock_row_length = 25 + 4 * lenspacing
    
    elif kwargs["clock-format"] == "ds":

        clock_row_length = 95 + 18 * lenspacing

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
    parser = argparse.ArgumentParser(description="Digital Clock Options")

    parser.add_argument("-m","--format", type=str, default="s", help="format of the clock", choices=["m","s","ms","ds"])
    parser.add_argument("-p","--position", default=5, help="position of the clock",choices=range(1,10))
    parser.add_argument("-c","--coloring", type=str, default="gradient", help="how to color the clock",choices=["gradient","default"])
    parser.add_argument("-s","--spacing", type=str, default="empty", help="spacing character for clock",choices=fonts.fonts.keys())
    parser.add_argument("-e","--echar", type=str, default="empty", help="the empty cell character",choices=fonts.fonts.keys())
    parser.add_argument("-f","--fchar", type=str, default="full-block", help="the full cell character",choices=fonts.fonts.keys())
    parser.add_argument("--gstyle", type=str, default="horizontal", help="gradient style",choices=["horizontal","vertical","diagonal","reverse-diagonal"])
    parser.add_argument("--hstart", type=float, default=0.0, help="hue start value for gradient")
    parser.add_argument("--hspread", type=float, default=0.1, help="hue spread value for gradient")
    parser.add_argument("--sstart", type=float, default=1.0, help="saturation start value for gradient")
    parser.add_argument("--sspread", type=float, default=0.0, help="saturation spread value for gradient")
    
    args = parser.parse_args()

    clock_settings = {
        "clock-format": args.format,
        "position": args.position,
        "coloring": args.coloring,
        "spacing": fonts.fonts[args.spacing],
        "empty-character": fonts.fonts[args.echar],
        "full-character": fonts.fonts[args.fchar],
        "gradient-style": args.gstyle,
        "hue_start": float(args.hstart),
        "hue_spread": float(args.hspread),
        "saturation-start": float(args.sstart),
        "saturation-spread": float(args.sspread),
    }

    try:

        clearConsole()
        while True:


            tsize = os.get_terminal_size()
            if clock_settings["clock-format"] == "s":
                timestr = "%H:%M:%S"

            elif clock_settings["clock-format"] == "ms":
                timestr = "%H:%M:%S:%f"

            elif clock_settings["clock-format"] == "m":
                timestr = "%H:%M"

            elif clock_settings["clock-format"] == "ds":
                timestr = "%d:%m:%Y %H:%M:%S"

            current_time = datetime.now().strftime(timestr)

            sclock = clock(current_time,**clock_settings)
            aclock = align(sclock,tsize,**clock_settings)

            print("\033[2J\033[?25l\033[0;0H" + aclock, flush=True) # clear screen + hide cursor + position cursor to 0, 0

            if clock_settings["clock-format"] == "s":
                time.sleep(1)
            elif clock_settings["clock-format"] == "m":
                time.sleep(60)

    except KeyboardInterrupt:

        print('\033[?25hClock is stopped!') # show cursor
    