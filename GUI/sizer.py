import os
import wx

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		self.dirname = ''

		wx.Frame.__init__(self, parent, title=title, size=(200,-1)) #-1 is using default
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar() #create status bar at the bottom of the window

		#Setting up the menu
		filemenu = wx.Menu()
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file to edit")
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Info about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

		#Create the menubar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)
		
		#events
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		self.buttons = []
		for i in range(0,6):
			self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
			self.sizer2.Add(self.buttons[i], 1, wx.EXPAND) #first arg is control, second if resize ratio (1,2,3). If = 0 : no resize.:w

		#use some sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.control, 1, wx.EXPAND)
		self.sizer.Add(self.sizer2, 0, wx.EXPAND)

		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show()

	def OnAbout(self,e):
		dlg = wx.MessageDialog(self, "A simple editor", "About", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self,e):
		self.Close(True)

	def OnOpen(self,e):
		"""Open a file"""
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFileName()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()
