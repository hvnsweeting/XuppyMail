#!/usr/bin/env python
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Hello World")

		self.button = Gtk.Button(label="Click here")
		self.button.connect("clicked", self.on_button_clicked)
		self.add(self.button)
fu

	def on_button_clicked(self, widget):
		print "Hello thon"

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
