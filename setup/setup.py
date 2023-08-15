import time
import network
essid="Quotes"
ap = network.WLAN(network.AP_IF)
ap.config(essid=essid, password='')
ap.active(True)
ip_addr = ap.ifconfig()[0]

import hardware.tft_config as tft_config
import vga1_bold_16x32 as big
tft = tft_config.config(tft_config.WIDE)
tft.init()

font = big
height = tft.height()
width  = tft.width()

import s3lcd
foreground = s3lcd.WHITE
background = s3lcd.BLACK

tft.fill(background)
tft.show()

tft.text(font, f"Setup at"          , 5 , 5  , foreground, background)
tft.text(font, f"http://{ip_addr}"  , 5 , 55 , foreground, background)
tft.text(font, f"Wifi ssid:{essid}" , 5 , 95 , foreground, background)
tft.show()
tft.deinit()




