import board
import busio
import displayio
import terminalio
from adafruit_display_text import label

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import Oled, OledDisplayMode

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP11, board.GP12, board.GP13)
keyboard.row_pins = (board.GP8, board.GP9, board.GP10)
keyboard.diode_orientation = DiodeOrientation.COL2ROW


encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.GP14, board.GP15, board.GP16),
)

encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),),
]


displayio.release_displays()

i2c = busio.I2C(board.GP3, board.GP2)
oled = Oled(
    i2c=i2c,
    width=128,
    height=64,
    flip=False,
    mode=OledDisplayMode.TXT,
)

keyboard.modules.append(oled)


keyboard.keymap = [
    [
        KC.COPY, KC.PASTE, KC.CUT,
        KC.UNDO, KC.REDO, KC.ENTER,
        KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PREV_TRACK,
    ]
]


def oled_task():
    oled.clear()
    oled.write_line("KMK Macropad", 0)
    oled.write_line("Layer 0", 1)

keyboard.after_matrix_scan = oled_task


keyboard.go()
