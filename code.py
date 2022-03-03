import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems


class Button:
    _keyboard = Keyboard(usb_hid.devices)

    def __init__(
        self, board_pin, keycodes, debounce_interval=0.01, pull=digitalio.Pull.UP
    ):
        self._board_pin = board_pin
        self._keycodes = keycodes
        self._pin = digitalio.DigitalInOut(board_pin)
        self._pin.direction = digitalio.Direction.INPUT
        self._pin.pull = pull
        self._debouncer = Debouncer(self._pin, debounce_interval)
        if pull == digitalio.Pull.UP:
            self._fell_action = Button._keyboard.press
            self._rose_action = Button._keyboard.release
        else:
            self._rose_action = Button._keyboard.press
            self._fell_action = Button._keyboard.release

    def update(self):
        debouncer = self._debouncer
        debouncer.update()
        if debouncer.fell:
            self._fell_action(*self._keycodes)
        elif debouncer.rose:
            self._rose_action(*self._keycodes)


buttons = [
    Button(board.GP0, [Keycode.A]),
    Button(board.GP1, [Keycode.B]),
]

while True:
    for b in buttons:
        b.update()
