#!/usr/bin/python


# def scan_code(vid=0x0581, pid=0x0115):

#     try:
#         print("Opening the device")

#         h = hid.device()
#         h.open(vid, pid)

#         print(f"Manufacturer: {h.get_manufacturer_string()}")
#         print(f"Product: {h.get_product_string()}")
#         print(f"Serial No: {h.get_serial_number_string()}")

#         # enable non-blocking mode
#         h.set_nonblocking(1)

#         qr_code = []
#         try:
#             while True:

#                 d = h.read(8)
#                 if any(d):
#                     val = usb_codes.get(d[2])
#                     if d[0] == 2:
#                         qr_code += val[1]
#                         print(val[1], end="")
#                     else:
#                         qr_code += val[0]
#                         print(val[0], end="")

#                     if qr_code[-1] == "\n":
#                         break

#         except KeyboardInterrupt:
#             logging.debug("Keyboard interrupt")

#         except Exception as err:
#             logging.error(err)

#         print("Closing the device")
#         h.close()

#     except IOError as ex:
#         print(ex)
#         print("You probably don't have the hard-coded device.")


# USB keyboard HID key codes
# -*- coding: utf-8 -*-
usb_codes = {
    0x04: ["a", "A"],
    0x05: ["b", "B"],
    0x06: ["c", "C"],
    0x07: ["d", "D"],
    0x08: ["e", "E"],
    0x09: ["f", "F"],
    0x0A: ["g", "G"],
    0x0B: ["h", "H"],
    0x0C: ["i", "I"],
    0x0D: ["j", "J"],
    0x0E: ["k", "K"],
    0x0F: ["l", "L"],
    0x10: ["m", "M"],
    0x11: ["n", "N"],
    0x12: ["o", "O"],
    0x13: ["p", "P"],
    0x14: ["q", "Q"],
    0x15: ["r", "R"],
    0x16: ["s", "S"],
    0x17: ["t", "T"],
    0x18: ["u", "U"],
    0x19: ["v", "V"],
    0x1A: ["w", "W"],
    0x1B: ["x", "X"],
    0x1C: ["y", "Y"],
    0x1D: ["z", "Z"],
    0x1E: ["1", "!"],
    0x1F: ["2", "@"],
    0x20: ["3", "#"],
    0x21: ["4", "$"],
    0x22: ["5", "%"],
    0x23: ["6", "^"],
    0x24: ["7", "&"],
    0x25: ["8", "*"],
    0x26: ["9", "("],
    0x27: ["0", ")"],
    0x28: ["\n", "\n"],
    0x29: ["[ESC]", "[ESC]"],
    0x2A: ["[BACKSPACE]", "[BACKSPACE]"],
    0x2B: ["\t", "\t"],
    0x2C: [" ", " "],
    0x2D: ["-", "_"],
    0x2E: ["=", "+"],
    0x2F: ["[", "{"],
    0x30: ["]", "}"],
    0x31: ["',\"|"],
    0x32: ["#", "~"],
    0x33: ";:",
    0x34: "'\"",
    0x36: ",<",
    0x37: ".>",
    0x38: "/?",
    0x39: ["[CAPSLOCK]", "[CAPSLOCK]"],
    0x3A: ["F1"],
    0x3B: ["F2"],
    0x3C: ["F3"],
    0x3D: ["F4"],
    0x3E: ["F5"],
    0x3F: ["F6"],
    0x41: ["F7"],
    0x42: ["F8"],
    0x43: ["F9"],
    0x44: ["F10"],
    0x45: ["F11"],
    0x46: ["F12"],
    0x4F: ["\xe2\x86\x92", "\xe2\x86\x92"],
    0x50: ["\xe2\x86\x90", "\xe2\x86\x90"],
    0x51: ["\xe2\x86\x93", "\xe2\x86\x93"],
    0x52: ["\xe2\x86\x91", "\xe2\x86\x91"],
}

ctrl_code = {
    0x01: "KEY_MOD_LCTRL",
    0x02: "KEY_MOD_LSHIFT",
    0x04: "KEY_MOD_LALT",
    0x08: "KEY_MOD_LMETA",
    0x10: "KEY_MOD_RCTRL",
    0x20: "KEY_MOD_RSHIFT",
    0x40: "KEY_MOD_RALT",
    0x80: "KEY_MOD_RMETA",
}


usb_hid_codes = {
    0x00: "KEY_NONE",  # No key pressed
    0x01: "KEY_ERR_OVF",  #  Keyboard Error Roll Over - used for all slots if too many keys are pressed ("Phantom key")
    0x02: "FAIL",  # Keyboard POST Fail
    0x03: "ERROR",  # Keyboard Error Undefined
    0x04: "KEY_A",  # Keyboard a and A
    0x05: "KEY_B",  # Keyboard b and B
    0x06: "KEY_C",  # Keyboard c and C
    0x07: "KEY_D",  # Keyboard d and D
    0x08: "KEY_E",  # Keyboard e and E
    0x09: "KEY_F",  # Keyboard f and F
    0x0A: "KEY_G",  # Keyboard g and G
    0x0B: "KEY_H",  # Keyboard h and H
    0x0C: "KEY_I",  # Keyboard i and I
    0x0D: "KEY_J",  # Keyboard j and J
    0x0E: "KEY_K",  # Keyboard k and K
    0x0F: "KEY_L",  # Keyboard l and L
    0x10: "KEY_M",  # Keyboard m and M
    0x11: "KEY_N",  # Keyboard n and N
    0x12: "KEY_O",  # Keyboard o and O
    0x13: "KEY_P",  # Keyboard p and P
    0x14: "KEY_Q",  # Keyboard q and Q
    0x15: "KEY_R",  # Keyboard r and R
    0x16: "KEY_S",  # Keyboard s and S
    0x17: "KEY_T",  # Keyboard t and T
    0x18: "KEY_U",  # Keyboard u and U
    0x19: "KEY_V",  # Keyboard v and V
    0x1A: "KEY_W",  # Keyboard w and W
    0x1B: "KEY_X",  # Keyboard x and X
    0x1C: "KEY_Y",  # Keyboard y and Y
    0x1D: "KEY_Z",  # Keyboard z and Z
    0x1E: "KEY_1",  # Keyboard 1 and !
    0x1F: "KEY_2",  # Keyboard 2 and @
    0x20: "KEY_3",  # Keyboard 3 and #
    0x21: "KEY_4",  # Keyboard 4 and $
    0x22: "KEY_5",  # Keyboard 5 and %
    0x23: "KEY_6",  # Keyboard 6 and ^
    0x24: "KEY_7",  # Keyboard 7 and &
    0x25: "KEY_8",  # Keyboard 8 and *
    0x26: "KEY_9",  # Keyboard 9 and (
    0x27: "KEY_0",  # Keyboard 0 and )
    0x28: "KEY_ENTER",  # Keyboard Return (ENTER)
    0x29: "KEY_ESC",  # Keyboard ESCAPE
    0x2A: "KEY_BACKSPACE",  # Keyboard DELETE (Backspace)
    0x2B: "KEY_TAB",  # Keyboard Tab
    0x2C: "KEY_SPACE",  # Keyboard Spacebar
    0x2D: "KEY_MINUS",  # Keyboard - and _
    0x2E: "KEY_EQUAL",  # Keyboard = and +
    0x2F: "KEY_LEFTBRACE",  # Keyboard [ and {
    0x30: "KEY_RIGHTBRACE",  # Keyboard ] and }
    0x31: "KEY_BACKSLASH",  # Keyboard \ and |
    0x32: "KEY_HASHTILDE",  # Keyboard Non-US # and ~
    0x33: "KEY_SEMICOLON",  # Keyboard ; and :
    0x34: "KEY_APOSTROPHE",  # Keyboard ' and "
    0x35: "KEY_GRAVE",  # Keyboard ` and ~
    0x36: "KEY_COMMA",  # Keyboard , and <
    0x37: "KEY_DOT",  # Keyboard . and >
    0x38: "KEY_SLASH",  # Keyboard / and ?
    0x39: "KEY_CAPSLOCK",  # Keyboard Caps Lock
    0x3A: "KEY_F1",  # Keyboard F1
    0x3B: "KEY_F2",  # Keyboard F2
    0x3C: "KEY_F3",  # Keyboard F3
    0x3D: "KEY_F4",  # Keyboard F4
    0x3E: "KEY_F5",  # Keyboard F5
    0x3F: "KEY_F6",  # Keyboard F6
    0x40: "KEY_F7",  # Keyboard F7
    0x41: "KEY_F8",  # Keyboard F8
    0x42: "KEY_F9",  # Keyboard F9
    0x43: "KEY_F10",  # Keyboard F10
    0x44: "KEY_F11",  # Keyboard F11
    0x45: "KEY_F12",  # Keyboard F12
    0x46: "KEY_SYSRQ",  # Keyboard Print Screen
    0x47: "KEY_SCROLLLOCK",  # Keyboard Scroll Lock
    0x48: "KEY_PAUSE",  # Keyboard Pause
    0x49: "KEY_INSERT",  # Keyboard Insert
    0x4A: "KEY_HOME",  # Keyboard Home
    0x4B: "KEY_PAGEUP",  # Keyboard Page Up
    0x4C: "KEY_DELETE",  # Keyboard Delete Forward
    0x4D: "KEY_END",  # Keyboard End
    0x4E: "KEY_PAGEDOWN",  # Keyboard Page Down
    0x4F: "KEY_RIGHT",  # Keyboard Right Arrow
    0x50: "KEY_LEFT",  # Keyboard Left Arrow
    0x51: "KEY_DOWN",  # Keyboard Down Arrow
    0x52: "KEY_UP",  # Keyboard Up Arrow
    0x53: "KEY_NUMLOCK",  # Keyboard Num Lock and Clear
    0x54: "KEY_KPSLASH",  # Keypad /
    0x55: "KEY_KPASTERISK",  # Keypad *
    0x56: "KEY_KPMINUS",  # Keypad -
    0x57: "KEY_KPPLUS",  # Keypad +
    0x58: "KEY_KPENTER",  # Keypad ENTER
    0x59: "KEY_KP1",  # Keypad 1 and End
    0x5A: "KEY_KP2",  # Keypad 2 and Down Arrow
    0x5B: "KEY_KP3",  # Keypad 3 and PageDn
    0x5C: "KEY_KP4",  # Keypad 4 and Left Arrow
    0x5D: "KEY_KP5",  # Keypad 5
    0x5E: "KEY_KP6",  # Keypad 6 and Right Arrow
    0x5F: "KEY_KP7",  # Keypad 7 and Home
    0x60: "KEY_KP8",  # Keypad 8 and Up Arrow
    0x61: "KEY_KP9",  # Keypad 9 and Page Up
    0x62: "KEY_KP0",  # Keypad 0 and Insert
    0x63: "KEY_KPDOT",  # Keypad . and Delete
    0x64: "KEY_102ND",  # Keyboard Non-US \ and |
    0x65: "KEY_COMPOSE",  # Keyboard Application
    0x66: "KEY_POWER",  # Keyboard Power
    0x67: "KEY_KPEQUAL",  # Keypad =
    0x68: "KEY_F13",  # Keyboard F13
    0x69: "KEY_F14",  # Keyboard F14
    0x6A: "KEY_F15",  # Keyboard F15
    0x6B: "KEY_F16",  # Keyboard F16
    0x6C: "KEY_F17",  # Keyboard F17
    0x6D: "KEY_F18",  # Keyboard F18
    0x6E: "KEY_F19",  # Keyboard F19
    0x6F: "KEY_F20",  # Keyboard F20
    0x70: "KEY_F21",  # Keyboard F21
    0x71: "KEY_F22",  # Keyboard F22
    0x72: "KEY_F23",  # Keyboard F23
    0x73: "KEY_F24",  # Keyboard F24
    0x74: "KEY_OPEN",  # Keyboard Execute
    0x75: "KEY_HELP",  # Keyboard Help
    0x76: "KEY_PROPS",  # Keyboard Menu
    0x77: "KEY_FRONT",  # Keyboard Select
    0x78: "KEY_STOP",  # Keyboard Stop
    0x79: "KEY_AGAIN",  # Keyboard Again
    0x7A: "KEY_UNDO",  # Keyboard Undo
    0x7B: "KEY_CUT",  # Keyboard Cut
    0x7C: "KEY_COPY",  # Keyboard Copy
    0x7D: "KEY_PASTE",  # Keyboard Paste
    0x7E: "KEY_FIND",  # Keyboard Find
    0x7F: "KEY_MUTE",  # Keyboard Mute
    0x80: "KEY_VOLUMEUP",  # Keyboard Volume Up
    0x81: "KEY_VOLUMEDOWN",  # Keyboard Volume Down
    # 0x82  Keyboard Locking Caps Lock
    # 0x83  Keyboard Locking Num Lock
    # 0x84  Keyboard Locking Scroll Lock
    0x85: "KEY_KPCOMMA",  # Keypad Comma
    # 0x86  Keypad Equal Sign
    0x87: "KEY_RO",  # Keyboard International1
    0x88: "KEY_KATAKANAHIRAGANA",  # Keyboard International2
    0x89: "KEY_YEN",  # Keyboard International3
    0x8A: "KEY_HENKAN",  # Keyboard International4
    0x8B: "KEY_MUHENKAN",  # Keyboard International5
    0x8C: "KEY_KPJPCOMMA",  # Keyboard International6
    # 0x8d  Keyboard International7
    # 0x8e  Keyboard International8
    # 0x8f  Keyboard International9
    0x90: "KEY_HANGEUL",  # Keyboard LANG1
    0x91: "KEY_HANJA",  # Keyboard LANG2
    0x92: "KEY_KATAKANA",  # Keyboard LANG3
    0x93: "KEY_HIRAGANA",  # Keyboard LANG4
    0x94: "KEY_ZENKAKUHANKAKU",  # Keyboard LANG5
    # 0x95  Keyboard LANG6
    # 0x96  Keyboard LANG7
    # 0x97  Keyboard LANG8
    # 0x98  Keyboard LANG9
    # 0x99  Keyboard Alternate Erase
    # 0x9a  Keyboard SysReq/Attention
    # 0x9b  Keyboard Cancel
    # 0x9c  Keyboard Clear
    # 0x9d  Keyboard Prior
    # 0x9e  Keyboard Return
    # 0x9f  Keyboard Separator
    # 0xa0  Keyboard Out
    # 0xa1  Keyboard Oper
    # 0xa2  Keyboard Clear/Again
    # 0xa3  Keyboard CrSel/Props
    # 0xa4  Keyboard ExSel
    # 0xb0  Keypad 00
    # 0xb1  Keypad 000
    # 0xb2  Thousands Separator
    # 0xb3  Decimal Separator
    # 0xb4  Currency Unit
    # 0xb5  Currency Sub-unit
    0xB6: "KEY_KPLEFTPAREN",  # Keypad (
    0xB7: "KEY_KPRIGHTPAREN",  # Keypad )
    # 0xb8  Keypad {
    # 0xb9  Keypad }
    # 0xba  Keypad Tab
    # 0xbb  Keypad Backspace
    # 0xbc  Keypad A
    # 0xbd  Keypad B
    # 0xbe  Keypad C
    # 0xbf  Keypad D
    # 0xc0  Keypad E
    # 0xc1  Keypad F
    # 0xc2  Keypad XOR
    # 0xc3  Keypad ^
    # 0xc4  Keypad %
    # 0xc5  Keypad <
    # 0xc6  Keypad >
    # 0xc7  Keypad &
    # 0xc8  Keypad &&
    # 0xc9  Keypad |
    # 0xca  Keypad ||
    # 0xcb  Keypad :
    # 0xcc  Keypad #
    # 0xcd  Keypad Space
    # 0xce  Keypad @
    # 0xcf  Keypad !
    # 0xd0  Keypad Memory Store
    # 0xd1  Keypad Memory Recall
    # 0xd2  Keypad Memory Clear
    # 0xd3  Keypad Memory Add
    # 0xd4  Keypad Memory Subtract
    # 0xd5  Keypad Memory Multiply
    # 0xd6  Keypad Memory Divide
    # 0xd7  Keypad +/-
    # 0xd8  Keypad Clear
    # 0xd9  Keypad Clear Entry
    # 0xda  Keypad Binary
    # 0xdb  Keypad Octal
    # 0xdc  Keypad Decimal
    # 0xdd  Keypad Hexadecimal
    0xE0: "KEY_LEFTCTRL",  # Keyboard Left Control
    0xE1: "KEY_LEFTSHIFT",  # Keyboard Left Shift
    0xE2: "KEY_LEFTALT",  # Keyboard Left Alt
    0xE3: "KEY_LEFTMETA",  # Keyboard Left GUI
    0xE4: "KEY_RIGHTCTRL",  # Keyboard Right Control
    0xE5: "KEY_RIGHTSHIFT",  # Keyboard Right Shift
    0xE6: "KEY_RIGHTALT",  # Keyboard Right Alt
    0xE7: "KEY_RIGHTMETA",  # Keyboard Right GUI
    0xE8: "KEY_MEDIA_PLAYPAUSE",
    0xE9: "KEY_MEDIA_STOPCD",
    0xEA: "KEY_MEDIA_PREVIOUSSONG",
    0xEB: "KEY_MEDIA_NEXTSONG",
    0xEC: "KEY_MEDIA_EJECTCD",
    0xED: "KEY_MEDIA_VOLUMEUP",
    0xEE: "KEY_MEDIA_VOLUMEDOWN",
    0xEF: "KEY_MEDIA_MUTE",
    0xF0: "KEY_MEDIA_WWW",
    0xF1: "KEY_MEDIA_BACK",
    0xF2: "KEY_MEDIA_FORWARD",
    0xF3: "KEY_MEDIA_STOP",
    0xF4: "KEY_MEDIA_FIND",
    0xF5: "KEY_MEDIA_SCROLLUP",
    0xF6: "KEY_MEDIA_SCROLLDOWN",
    0xF7: "KEY_MEDIA_EDIT",
    0xF8: "KEY_MEDIA_SLEEP",
    0xF9: "KEY_MEDIA_COFFEE",
    0xFA: "KEY_MEDIA_REFRESH",
    0xFB: "KEY_MEDIA_CALC",
}
