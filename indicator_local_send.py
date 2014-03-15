#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import appindicator

class AppIndicatorExample:
    def __init__(self):
        self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon("distributor-logo")

        # create a menu
        self.menu = gtk.Menu()

        self.online = True

        # create items for the menu - labels, checkboxes, radio buttons and images are supported:
        

        self.check = gtk.ImageMenuItem("Go Online")
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
        gtk.main_quit()

    def toggle_status(self, widget):
        if self.online == True:
            widget.set_label("Go Offline")
            self.online = False
        else:
            widget.set_label("Go Online")
            self.online = True


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    indicator = AppIndicatorExample()
    main()