import os
from datetime import datetime
import time

characters = {"1": "046108e","2": "0e8889f","3": "1e0f83e","4": "118f821","5": "0f8783e","6": "0e87a2e","7": "1e11110","8": "0e8ba2e","9": "0e8bc2e","0": "0e8c62e",":": "0020080"}

def clock(ctime):
    # leading zeros when converting
    # https://stackoverflow.com/a/17157819

    # splitby5:
    # https://stackoverflow.com/a/9475538

    return "\n".join(["  ".join(list(zip(*[map(''.join, zip(*[iter(bin(int('1'+characters[c],16))[6:].replace("0"," ").replace("1","\u25A0"))]*5)) for c in ctime]))[i]) for i in range(5)])


if __name__ == "__main__":

    try:
        while True:
            os.system('cls' if os.name=='nt' else 'clear')

            print(clock(datetime.now().strftime("%-H:%M:%S")))
            time.sleep(1)
    except KeyboardInterrupt:
        print('Clock is stopped!')
    