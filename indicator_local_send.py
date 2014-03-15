#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
from subprocess import *
import sys

class AppIndicatorExample:
    def __init__(self):
        self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon("/usr/share/pixmaps/messenger_icon.png")

        # create a menu
        self.menu = gtk.Menu()

        self.online = True
        Popen(["python", "/usr/share/local_send/server.py"])

        # create items for the menu - labels, checkboxes, radio buttons and images are supported:
        

        self.check = gtk.ImageMenuItem("Go Offline")
        self.check.show()
        self.menu.append(self.check)
        # self.check.set_active(False)
        self.check.connect("activate", self.toggle_status)


        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        self.menu.append(image)
                    
        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self, widget, data=None):
        if call(["fuser", "8003/udp"], stdout=PIPE, stderr=PIPE) == 0:
            pid = check_output(["fuser" , "8003/udp"],stderr=PIPE).strip()
            call(["kill", "-9", pid])
        gtk.main_quit()

    def toggle_status(self, widget):
        if self.online == True:
            widget.set_label("Go Online")
            if call(["fuser", "8003/udp"], stdout=PIPE, stderr=PIPE) == 0:
                pid = check_output(["fuser" , "8003/udp"],stderr=PIPE).strip()
                call(["kill", "-9", pid], stdout=PIPE, stderr=PIPE)
            self.online = False
        else:
            Popen(["python", "/usr/share/local_send/server.py"], stdout=PIPE, stderr=PIPE)
            widget.set_label("Go Offline")
            self.online = True


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    if call(["fuser", "8003/udp"], stdout=PIPE, stderr=PIPE) == 0:
        sys.exit(0)
    indicator = AppIndicatorExample()
    main()