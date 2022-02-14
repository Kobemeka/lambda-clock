import os
from datetime import datetime
import time

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

def splitby5(s):
    # splits the string by 5 characters
    return [s[j:j+5] for j in range(0, len(s), 5)]

def convef(n,empty = " ",full = "\u25A0"):
    # converts the string with ones and zeros to given characters    
    return n.replace("0",empty).replace("1",full)

def mergeLines(t,spacing = "  "):
    # merges the converted and splitted text lines by lines with spacing
    # and joins with new line character (\n)
    
    #                              using zip to
    #                              get same line for
    #                              all chars                    5 line
    #                                   |                         |
    #                                   v                         v
    rt = "\n".join([spacing.join(list(zip(*t))[i]) for i in range(5)])
    return rt

def clock(ctime):
    '''
    actually we do this:

    t = []
    for c in ctime:
        char = hex2cistr(hex(characters[c]))
        conv = convef(char)
        sp5 = splitby5(conv)
        t.append(sp5)
    '''

    # for every char in current time convert to string by hex2cistr
    # then convert them to empty - full chars
    # then split by 5
    # then merge
    t = [splitby5(convef(hex2cistr(hex(characters[c])))) for c in ctime]
    ml = mergeLines(t)
    return ml

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

if __name__ == "__main__":
    try:
        while True:
            clearConsole()
            current_time = datetime.now().strftime("%-H:%M:%S")
            print(clock(current_time))
            time.sleep(1)
    except KeyboardInterrupt:
        print('Clock is stopped!')
    