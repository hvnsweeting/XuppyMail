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
		gridSizer = wx.GridBagSizer(hgap=5, vgap=5)
		buttonHSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.fromLbl = wx.StaticText(self, label="From:")
		gridSizer.Add(self.fromLbl, pos=(0,0))
		#From text control
		self.fromTc = wx.TextCtrl(self, size=(-1,-1))
		gridSizer.Add(self.fromTc, pos=(0,1))


		self.recvLbl = wx.StaticText(self, label="Recipients:")
		gridSizer.Add(self.recvLbl, pos=(1,0))
		#Receivers text control
		self.recvTc = wx.TextCtrl(self, size=(-1, -1))
		gridSizer.Add(self.recvTc, pos=(1,1))

		self.subjectLbl = wx.StaticText(self, label="Subject:")
		gridSizer.Add(self.subjectLbl, pos=(2,0))
		#Subject tc
		self.subjectTc = wx.TextCtrl(self, size=(-1, -1)) 
		gridSizer.Add(self.subjectTc, pos=(2,1))

		#Content tc - multiline
		self.contentTc = wx.TextCtrl(self, style=wx.TE_MULTILINE)



		#3 buttons Clear - Send - Cancel
		self.clearBtn = wx.Button(self, label="Clear")
		buttonHSizer.Add(self.clearBtn, 0)
		self.sendBtn = wx.Button(self, label="Send")
		buttonHSizer.Add(self.sendBtn, 0)
		self.cancelBtn = wx.Button(self, label="Cancel")
		buttonHSizer.Add(self.cancelBtn, 0)

		mainVSizer.Add(gridSizer, 0, wx.ALL, 5)
		mainVSizer.Add(self.contentTc, 1, wx.EXPAND)
		mainVSizer.Add(buttonHSizer, 0, wx.ALL, 5)
		self.SetSizerAndFit(mainVSizer)

app = wx.App(False)
frame = ComposerFrame(None, "XuppyMail")
dframe = wx.Frame(None)
composer = ComposerPanel(frame)
frame.Show()
app.MainLoop()
