#!/usr/bin/env python
import wx
import os

class EditorFrame(wx.Frame):
	"""Frame for a editor"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400,300))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

		#setting up the menu
		filemenu = wx.Menu()
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open file")
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "By FAMILUG team")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

		#creating the menuBar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File") #Adding file menu to the menubar
		self.SetMenuBar(menuBar)

		#set events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)

		#show frame
		self.Show(True)

	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "Text editor by FAMILUG", "Cute editor", wx.OK)
		dlg.ShowModal() #show it
		dlg.Destroy() #destroy when finish
	
	def OnExit(self, e):
		self.Close(True) #Close the frame

	def onOpen(self, e):
		"""Open a file"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK: #user cannot do anything on app util click ok or cancel
			#dlg.ShowModal() return ID of button pressed
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()

app = wx.App(False) 
frame = EditorFrame(None, 'Simple editor')
app.MainLoop()
