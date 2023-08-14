import re
import time
import s3lcd
import random
import hardware.tft_config as tft_config
import vga1_bold_16x32 as big
import machine
from common import setup_file, quotes_dir

tft = tft_config.config(tft_config.WIDE)
tft.init()

font = big
height = tft.height()
width = tft.width()

foreground = s3lcd.WHITE
background = s3lcd.BLACK
tft.fill(background)
tft.show()

first_visible_line = height - font.HEIGHT

colors = [
    s3lcd.GREEN,
    s3lcd.CYAN,
    s3lcd.MAGENTA,
    s3lcd.YELLOW,
    s3lcd.WHITE,
    s3lcd.BLUE,
    s3lcd.RED,
]


BUTTON_PIN_1 = 0
BUTTON_PIN_2 = 14
button1 = machine.Pin(BUTTON_PIN_1, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON_PIN_2, machine.Pin.IN, machine.Pin.PULL_UP)

all_random_colors = False
colors = [  s3lcd.RED,
            s3lcd.GREEN,
            s3lcd.BLUE,
            s3lcd.CYAN,
            s3lcd.MAGENTA,
            s3lcd.YELLOW,
            s3lcd.WHITE,
]



def color_generator(color_list):
    while True:
        for one_color in color_list:
            yield one_color

def quote_type_generator(my_dispatch_table):
    while True:
        yield from my_dispatch_table  

def check_button1():
    """ value 1 is unpressed, 0 is pressed """
    global foreground
    if not button1.value():
        foreground = next(my_colors)
            
def check_button2():
    """ value 1 is unpressed, 0 is pressed """
    if not button2.value():
        set_quote_type()
    
def set_quote_type(dst_quote_type=None):
    
    if quote_type == 1:
       dst_quote_type = 2
    if quote_type == 2:   
       dst_quote_type = 3
    if quote_type == 3:
       dst_quote_type = 1
       
    with open(f"{quotes_dir}/quote_type.txt",'w') as fh:
        fh.write(f"QUOTE_TYPE={dst_quote_type}")
    import machine
    machine.reset()


def get_quote_type():
    with open(f"{quotes_dir}/quote_type.txt") as fh:
        quotes_content = fh.readline()
        _, quote_type = quotes_content.split("=")
        return quote_type

def split_file_into_strings(file_path, max_length=19):

    for line in open(file_path, "r"):
        strings = []
        line = line.strip()
        parts = line.split("-")
        """
        0 "The future belongs to those who believe in the beauty of their dreams." 
        1  Eleanor Roosevelt
        0 "Believe you can and you're halfway there." 
        1  Theodore Roosevelt
        """
        for index, quote_part in enumerate(parts):
            if index == 1:
                author = quote_part.strip()
                strings.append("-" + author)
            else:
                actual_quote = quote_part.strip()
                process_line(actual_quote, strings, max_length)
        yield strings


def process_line(actual_quote, strings, max_length):

    words = actual_quote.split()
    current_string = ""

    for word in words:
        if len(current_string) + len(word) + 1 <= max_length:
            current_string += " " + word
        else:
            strings.append(current_string.strip())
            current_string = word

    if current_string:
        if re.match(r".*[bcdfghjklmnpqrstvwxyz]$", current_string):
            strings.append(current_string.rsplit(" ", 1)[0].strip())
            strings.append(current_string.rsplit(" ", 1)[-1].strip())
        else:
            strings.append(current_string.strip())


def one_ata_time():
    """Each quote will start on the bottom left of the screen and scroll up to the top
    and effectively 'fade away'
    The next quote will only proceed once the first is GONE
    """
    left_right = 8

    def do_more():
        tft.text(
            font,
            f"{one_quote_line}",
            left_right,
            first_visible_line,
            foreground,
            background,
        )
        """ The number of characters/lines that will fit on a screen is height/font.HEIGHT      """
        """ That's the number of times we need to scroll the line up by a unit of x in scroll() """
        for num_times in range(height / font.HEIGHT):
            for _ in range(font.HEIGHT):
                tft.scroll(0, -1)
                tft.show()

    while True:

        
        """
        Scroll the Type first ...
        """
        if quote_type == 1:
            text=f"!Famous Quotes!"
        if quote_type == 2:
            text=f"~Bhuddist Quotes~"
        if quote_type == 3:
            text=f":) Happiness Quotes"
            
        tft.text(font, text, left_right, first_visible_line, foreground, background)
        for num_times in range(height / font.HEIGHT):
                for _ in range(font.HEIGHT):
                    tft.scroll(0, -1)
                    tft.show()


        quotes = split_file_into_strings(dispatch_table.get(quote_type,  2))

        for one_quote in quotes:
            
            for one_quote_line in one_quote:
                
                check_button1()
                check_button2()
                
                if one_quote_line.startswith('"'):
                    
                    tft.text(
                        font,
                        f"{one_quote_line}",
                        left_right,
                        first_visible_line,
                        foreground,
                        background,
                    )
                    
                    for _ in range(font.HEIGHT):
                        tft.scroll(0, -1)
                        tft.show()

                elif one_quote_line.startswith("-"):
                    
                    tft.text(
                        font,
                        f"{one_quote_line}",
                        left_right,
                        first_visible_line,
                        foreground,
                        background,
                    )
                    
                    do_more()
                
                else:
                
                    tft.text(
                        font,
                        f"{one_quote_line}",
                        left_right,
                        first_visible_line,
                        foreground,
                        background,
                    )
                    tft.show()
                    
                    for _ in range(font.HEIGHT):
                        tft.scroll(0, -1)
                        tft.show()


import gc
gc.collect()

dispatch_table = {
    1: f"{quotes_dir}/quotes.txt",
    2: f"{quotes_dir}/buddhist.txt",
    3: f"{quotes_dir}/happy.txt",
}

my_colors          = color_generator(colors)
new_quote_type_gen = quote_type_generator(dispatch_table)
        
"""  Type comes out of the file as a str """
quote_type = int(get_quote_type())
one_ata_time()
