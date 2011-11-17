import smtplib #TODO change to Mine later
import poplib #TODO change to mine later
import wx
import os

#TODO attach file
#TODO Implement Pop3
#TODO split to many separate files
#NOTE: each control should use only once. If use more, they will break the form, and should add one to boxer right after we create it.
class ComposerFrame(wx.Frame):
	"""Frame for mail composer"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(600,400))

		#Setting up the menu bar
		fileMenu = wx.Menu()
		menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
		#menuLogin = fileMenu.Append(wx.ID_ANY, "&Login", "Login")
		menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

		#Create the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		self.SetMenuBar(menuBar)
		
		#Set menu events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		#self.Bind(wx.EVT_MENU, self.OnLogin, menuLogin)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		#Status bar
		self.CreateStatusBar()
		self.SetStatusText("Not login")

		#Show frame
		self.Show()

	def OnAbout(self, e):
		aboutDialog = wx.MessageDialog(self, "XuppyMail - a simple mail client ")
		aboutDialog.ShowModal()
		aboutDialog.Destroy()
	
	#def OnLogin(self, e):
	#	loginDialog = wx.PasswordEntryDialog(self, "Login")
	#	loginDialog.ShowModal()
	#	loginDialog.Destroy()

	def OnExit(self, e):
		self.Close(True) #Close the frame


#Composer panel tab
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

		#buttons Clear - Send 
		self.clearBtn = wx.Button(self, label="Clear")
		self.Bind(wx.EVT_BUTTON, self.ClearClick, self.clearBtn)
		buttonHSizer.Add(self.clearBtn, 0)

		self.sendBtn = wx.Button(self, label="Send")
		self.Bind(wx.EVT_BUTTON, self.SendClick, self.sendBtn)
		buttonHSizer.Add(self.sendBtn, 0)

		mainVSizer.Add(fromHSizer, 0, wx.EXPAND)
		mainVSizer.Add(recvHSizer, 0, wx.EXPAND)
		mainVSizer.Add(subjectHSizer, 0, wx.EXPAND)
		mainVSizer.Add(self.contentTc, 1, wx.EXPAND)
		mainVSizer.Add(buttonHSizer, 0, wx.ALL, 5)

		self.SetSizerAndFit(mainVSizer)

	def SendClick(self, event):
		"""Send mail """
		sender = self.fromTc.GetValue()
		recp = self.recvTc.GetValue()
		msg = self.contentTc.GetValue()
		#TODO need a parser to parse email address to host address
		s = smtplib.SMTP('localhost')
		s.sendmail(sender, recp, msg)
		#TODO change status bar if mail sented

	def ClearClick(self, event):
		"""Clear content control"""
		self.contentTc.Clear()

#Inbox panel tab
class InboxPanel(wx.Panel):
	"""Inbox panel tab"""
	def __init__(self, parent):
		wx.Panel.__init__(self,parent)
		self.popObject = None

		#Sizers
		inboxVSizer = wx.BoxSizer(wx.VERTICAL)
		gridSizer = wx.GridBagSizer(hgap=5, vgap=5)
		bindHSizer = wx.BoxSizer(wx.HORIZONTAL)
		loginHSizer = wx.BoxSizer(wx.HORIZONTAL)

		#Login : host, port, user, pass
		self.hostLbl = wx.StaticText(self, label="Host:")
		self.hostTc = wx.TextCtrl(self, size=(-1,-1))
		bindHSizer.Add(self.hostLbl, 0, wx.EXPAND)
		bindHSizer.Add(self.hostTc, 1, wx.EXPAND)

		self.portLbl = wx.StaticText(self, label="Port:")
		self.portTc = wx.TextCtrl(self, size=(-1,-1))
		bindHSizer.Add(self.portLbl, 0, wx.EXPAND)
		bindHSizer.Add(self.portTc, 1, wx.EXPAND)

		#Login
		self.userLbl = wx.StaticText(self, label="Username:")
		self.userTc = wx.TextCtrl(self, size=(-1,-1))
		loginHSizer.Add(self.userLbl, 0, wx.EXPAND)
		loginHSizer.Add(self.userTc, 1, wx.EXPAND)

		self.passLbl = wx.StaticText(self, label="Password:")
		self.passTc = wx.TextCtrl(self, size=(-1,-1), style=wx.TE_PASSWORD)
		self.loginBtn = wx.Button(self, label="Login")
		self.Bind(wx.EVT_BUTTON, self.LoginClick, self.loginBtn)

		loginHSizer.Add(self.passLbl, 0, wx.EXPAND)
		loginHSizer.Add(self.passTc, 1, wx.EXPAND)
		loginHSizer.Add(self.loginBtn, 0, wx.EXPAND)


		inboxVSizer.Add(bindHSizer, 0, wx.EXPAND)
		inboxVSizer.Add(loginHSizer, 0, wx.EXPAND)


		#Multiline text control
		self.logTc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		inboxVSizer.Add(self.logTc, 1, wx.EXPAND)

		#LIST
		self.listBtn = wx.Button(self, label="LIST")
		self.Bind(wx.EVT_BUTTON, self.ListClick, self.listBtn)

		#STAT
		self.statBtn = wx.Button(self, label="STAT")
		self.Bind(wx.EVT_BUTTON, self.StatClick, self.statBtn)

		#RETR
		self.retrTc = wx.TextCtrl(self, size=(-1,-1))
		self.retrBtn = wx.Button(self, label="RETR")
		self.Bind(wx.EVT_BUTTON, self.RetrClick, self.retrBtn)

		#DELE
		self.deleTc = wx.TextCtrl(self, size=(-1,-1))
		self.deleBtn = wx.Button(self, label="DELE")
		self.Bind(wx.EVT_BUTTON, self.DeleClick, self.deleBtn)

		gridSizer.Add(self.retrTc, pos=(0,0))
		gridSizer.Add(self.retrBtn, pos=(0,1))
		gridSizer.Add(self.deleTc, pos=(0,2))
		gridSizer.Add(self.deleBtn, pos=(0,3))
		gridSizer.Add(self.listBtn, pos=(0,5))
		gridSizer.Add(self.statBtn, pos=(0,6))

		inboxVSizer.Add(gridSizer, 0, wx.ALIGN_RIGHT)

		self.SetSizerAndFit(inboxVSizer)

	def PrintSl(self):
		"""Print a separate line """
		sp = '-' * 20 + '*' * 10 + '-' * 20 + '\n'
		self.logTc.AppendText(sp)
	
	def ListClick(self, event):
		"""Send LIST POP3's command"""
		if self.loginStatus:
			listMsg = list(self.popObject.list())
			l = list(listMsg)
			parsed = ''
			for i in l:
				parsed += str(i) + '\n'
			self.logTc.AppendText(parsed)

	def StatClick(self, event):
		"""Send STAT command"""
		if self.loginStatus:
			statMsg = list(self.popObject.stat())
			parsed = 'You have ' + str(statMsg[0]) + ' mails = ' + str(statMsg[1]) + ' bytes\n'
			self.logTc.AppendText(parsed)

	def RetrClick(self, event):
		"""Send RETR command"""
		#TODO add check if a message is deleted
		if self.loginStatus:
			retrMsg = self.popObject.retr(int(self.retrTc.GetValue()))
			parsed = ''
			for i in retrMsg:
				if isinstance(i, list):
					for k in i:
						parsed += k + '\n'
				else: parsed += str(i) + '\n'

			self.logTc.AppendText(parsed)
			self.PrintSl()
			
	def DeleClick(self, event):
		"""Send DELE command"""
		if self.loginStatus:
			deleMsg = self.popObject.dele(int(self.deleTc.GetValue()))
			self.logTc.AppendText(deleMsg)

	def LoginClick(self, event):
		"""Create POP3 object which connect to specified host, port and login"""
		host = self.hostTc.GetValue()
		port = self.portTc.GetValue()
		username = self.userTc.GetValue()
		passwd = self.passTc.GetValue()

		#TODO check port empty
		self.popObject = poplib.POP3(host, int(port))

		#this var help check whether user logged in or not
		self.loginStatus = False

		userMsg = self.popObject.user(username)
		passMsg = self.popObject.pass_(passwd)

		self.logTc.AppendText(self.popObject.getwelcome() + '\n')
		self.logTc.AppendText('USER: ' + username + '\n' + userMsg + '\n')
		self.logTc.AppendText('PASS: ' + passMsg + '\n')

		self.loginStatus = passMsg.__eq__('+OK Logged in.')
		if self.loginStatus:
			#Set all text control to immutable
			self.hostTc.SetEditable(False)
			self.portTc.SetEditable(False)
			self.userTc.SetEditable(False)
			self.passTc.SetEditable(False)
			#get current frame and set status text
			self.GetParent().GetParent().SetStatusText('Logged in') 


app = wx.App(False)
frame = ComposerFrame(None, "XuppyMail")
#composer = ComposerPanel(frame)
nb = wx.Notebook(frame)

nb.AddPage(InboxPanel(nb), "Inbox")
nb.AddPage(ComposerPanel(nb), "Composer")
app.MainLoop()
