import wx
import os

#NOTE: each control should use only once. If use more, they will break the form, and should add one to boxer right after we create it.
class ComposerFrame(wx.Frame):
	"""Frame for mail composer"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(500,400))

		#Setting up the menu bar
		fileMenu = wx.Menu()
		menuAbout = fileMenu.Append(wx.wx.ID_ABOUT, "&About", "Information about this program")
		menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

		#Create the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		self.SetMenuBar(menuBar)
		
		#Set menu events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		#Status bar
		self.CreateStatusBar()

		#Show frame
		self.Show()

	def OnAbout(self, e):
		aboutDialog = wx.MessageDialog(self, "XuppyMail - a simple mail client ")
		aboutDialog.ShowModal()
		aboutDialog.Destroy()

	def OnExit(self, e):
		self.Close(True) #Close the frame




class ComposerPanel(wx.Panel):
	"""Panel for mail composer"""
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		#Create some sizer
		mainVSizer = wx.BoxSizer(wx.VERTICAL)
		buttonHSizer = wx.BoxSizer(wx.HORIZONTAL)
		fromHSizer = wx.BoxSizer(wx.HORIZONTAL)
		recvHSizer = wx.BoxSizer(wx.HORIZONTAL)
		subjectHSizer = wx.BoxSizer(wx.HORIZONTAL)
		

		self.fromLbl = wx.StaticText(self, label="From:")
		fromHSizer.Add(self.fromLbl, 0, wx.EXPAND)
		##From text control
		self.fromTc = wx.TextCtrl(self, size=(-1,-1))
		fromHSizer.Add(self.fromTc, 1, wx.EXPAND)


		self.recvLbl = wx.StaticText(self, label="Recipients:")
		recvHSizer.Add(self.recvLbl, 0, wx.EXPAND)
		#Receivers text control
		self.recvTc = wx.TextCtrl(self, size=(-1, -1))
		recvHSizer.Add(self.recvTc, 1, wx.EXPAND)

		self.subjectLbl = wx.StaticText(self, label="Subject:")
		subjectHSizer.Add(self.subjectLbl, 0, wx.EXPAND)
		#Subject tc
		self.subjectTc = wx.TextCtrl(self, size=(-1, -1)) 
		subjectHSizer.Add(self.subjectTc, 1, wx.EXPAND)

		#Content tc - multiline
		self.contentTc = wx.TextCtrl(self, style=wx.TE_MULTILINE)

		#3 buttons Clear - Send - Cancel
		self.clearBtn = wx.Button(self, label="Clear")
		buttonHSizer.Add(self.clearBtn, 0)
		self.sendBtn = wx.Button(self, label="Send")
		buttonHSizer.Add(self.sendBtn, 0)
		self.cancelBtn = wx.Button(self, label="Cancel")
		buttonHSizer.Add(self.cancelBtn, 0)

		mainVSizer.Add(fromHSizer, 0, wx.EXPAND)
		mainVSizer.Add(recvHSizer, 0, wx.EXPAND)
		mainVSizer.Add(subjectHSizer, 0, wx.EXPAND)
		mainVSizer.Add(self.contentTc, 1, wx.EXPAND)
		mainVSizer.Add(buttonHSizer, 0, wx.ALL, 5)
		self.SetSizerAndFit(mainVSizer)

app = wx.App(False)
frame = ComposerFrame(None, "XuppyMail")
dframe = wx.Frame(None)
composer = ComposerPanel(frame)
frame.Show()
app.MainLoop()
