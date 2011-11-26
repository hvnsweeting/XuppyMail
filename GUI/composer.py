import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #add XuppyMail to path
from lib import mysmtp#, pop3lib 
import download
import poplib as pop3lib
import email
from email.mime.text import MIMEText
import wx
import aparser

#import smtplib 
#import poplib 
#TODO attach file
#TODO cut off the long subject
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
		recvHSizer = wx.BoxSizer(wx.HORIZONTAL)
		fromHSizer = wx.BoxSizer(wx.HORIZONTAL)
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
		s = mysmtp.SMTP('localhost')
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
		#this var help check whether user logged in or not
		self.loginStatus = False

		#Sizers
		inboxVSizer = wx.BoxSizer(wx.VERTICAL)
		gridSizer = wx.GridBagSizer(hgap=5, vgap=5)
		loginHSizer = wx.BoxSizer(wx.HORIZONTAL)
		bindHSizer = wx.BoxSizer(wx.HORIZONTAL)
		subjectHSizer = wx.BoxSizer(wx.HORIZONTAL)
		fromHSizer = wx.BoxSizer(wx.HORIZONTAL)
		attachHSizer = wx.BoxSizer(wx.HORIZONTAL)
		downloadGridSizer = wx.GridBagSizer(hgap=5, vgap=5)

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

	#	#LIST
	#	self.listBtn = wx.Button(self, label="LIST")
	#	self.Bind(wx.EVT_BUTTON, self.ListClick, self.listBtn)

	#	#STAT
	#	self.statBtn = wx.Button(self, label="STAT")
	#	self.Bind(wx.EVT_BUTTON, self.StatClick, self.statBtn)

		#RSET
		self.rsetBtn = wx.Button(self, label="RSET")
		self.Bind(wx.EVT_BUTTON, self.RsetClick, self.rsetBtn)

		#RETR
		self.retrTc = wx.TextCtrl(self, size=(-1,-1))
		self.retrBtn = wx.Button(self, label="RETR")
		self.Bind(wx.EVT_BUTTON, self.RetrClick, self.retrBtn)

		#DELE
		self.deleTc = wx.TextCtrl(self, size=(-1,-1))
		self.deleBtn = wx.Button(self, label="DELE")
		self.Bind(wx.EVT_BUTTON, self.DeleClick, self.deleBtn)

		#Subject
		self.subjectLbl = wx.StaticText(self, label='Subject')
		subjectHSizer.Add(self.subjectLbl, 0, wx.EXPAND)
		self.subjectTc = wx.TextCtrl(self, style=wx.TE_READONLY)
		subjectHSizer.Add(self.subjectTc, 1, wx.EXPAND)

		#From:
		self.fromLbl = wx.StaticText(self, label='From')
		fromHSizer.Add(self.fromLbl, 0, wx.EXPAND)
		self.fromTc = wx.TextCtrl(self, style=wx.TE_READONLY)
		fromHSizer.Add(self.fromTc, 1, wx.EXPAND)
		
		#Attach
		self.attachLbl = wx.StaticText(self, label='Attachment: 0 file(s)')
		attachHSizer.Add(self.attachLbl, 0, wx.EXPAND)
		self.attachTc = wx.TextCtrl(self, style=wx.TE_READONLY)
		attachHSizer.Add(self.attachTc, 1, wx.EXPAND)

		#Read mail panel
		self.readTc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		#Download
		self.downloadLbl = wx.StaticText(self, label='File #')
		self.downloadTc = wx.TextCtrl(self)

		self.downloadBtn = wx.Button(self, label="Download")
		self.Bind(wx.EVT_BUTTON, self.DownloadClick, self.downloadBtn)

		self.downloadAllBtn = wx.Button(self, label="Download All")
		self.Bind(wx.EVT_BUTTON, self.DownloadAllClick, self.downloadAllBtn)

		downloadGridSizer.Add(self.downloadLbl, pos=(0,0))
		downloadGridSizer.Add(self.downloadTc, pos=(0,1))
		downloadGridSizer.Add(self.downloadBtn, pos=(0,2))
		downloadGridSizer.Add(self.downloadAllBtn, pos=(0,3))

		gridSizer.Add(self.retrTc, pos=(0,0))
		gridSizer.Add(self.retrBtn, pos=(0,1))
		gridSizer.Add(self.deleTc, pos=(0,2))
		gridSizer.Add(self.deleBtn, pos=(0,3))
	#	gridSizer.Add(self.listBtn, pos=(0,5))
	#	gridSizer.Add(self.statBtn, pos=(0,6))
		gridSizer.Add(self.rsetBtn, pos=(0,7))

		inboxVSizer.Add(gridSizer, 0, wx.ALIGN_RIGHT)

		#inboxVSizer.Add(wx.StaticLine(self, ), 0, wx.ALL|wx.EXPAND, 5)
		inboxVSizer.Add(subjectHSizer, 0, wx.EXPAND)
		inboxVSizer.Add(fromHSizer, 0, wx.EXPAND)
		inboxVSizer.Add(attachHSizer, 0, wx.EXPAND)
		inboxVSizer.Add(self.readTc, 1, wx.EXPAND)
		inboxVSizer.Add(downloadGridSizer, 0, wx.ALIGN_RIGHT)

		self.SetSizerAndFit(inboxVSizer)

	def PrintSl(self):
		"""Print a separate line """
		sp = '-' * 20 + '*' * 10 + '-' * 20 + '\n'
		self.logTc.AppendText(sp)
	
#	def ListClick(self, event):
#		"""Send LIST POP3's command"""
#		if self.loginStatus:
#			listMsg = list(self.popObject.list())
#			l = list(listMsg)
#			parsed = ''
#			for i in l:
#				parsed += str(i) + '\n'
#			self.logTc.AppendText(parsed)

	def RsetClick(self, event):
		"""Send RSET command"""
		if self.loginStatus:
			rsetMsg = self.popObject.rset() + "\n"
			self.logTc.AppendText(rsetMsg)

#	def StatClick(self, event):
#		"""Send STAT command"""
#		if self.loginStatus:
#			statMsg = list(self.popObject.stat())
#			parsed = 'You have ' + str(statMsg[0]) + ' mails = ' + str(statMsg[1]) + ' bytes\n'
#			self.logTc.AppendText(parsed)

	def RetrClick(self, event):
		"""Send RETR command"""
		#TODO add check if a message is deleted
		if self.loginStatus:
			i = int(self.retrTc.GetValue())
			form = map(lambda i : str(i) + '\n', self.popObject.retr(i)[1])
			self.msg = ('',''.join(form))[1]
			info = aparser.parse(self.msg)
			self.subjectTc.SetValue(info['subject'])
			self.fromTc.SetValue(info['from'])
			self.readTc.SetValue(info['body'])
			self.attachLbl.SetLabel('Attachment: %d file(s)' % len(info['attachments']))
			s = ''
			for a in info['attachments']:
				s += str(info['attachments'].index(a)) + '.' + a.name + '  '
			self.attachTc.SetValue(s)
			
	def DeleClick(self, event):
		"""Send DELE command"""
		if self.loginStatus:
			deleMsg = self.popObject.dele(int(self.deleTc.GetValue())) + "\n"
			self.logTc.AppendText(deleMsg)

	def PrintLoggedIn(self, username, userMsg, passMsg):
		"""Print welcome, user, list of msg"""
		self.logTc.AppendText(self.popObject.getwelcome() + '\n')
		self.logTc.AppendText('Welcome back, ' + username + '!\n')
		statMsg = list(self.popObject.stat())
		parsed = 'You have ' + str(statMsg[0]) + ' mails = ' + str(statMsg[1]) + ' bytes\n'
		self.logTc.AppendText(parsed)

		#print info of all email
		for i in range(1, statMsg[0]+1):
			#add \n char to all string
			form = map(lambda i : str(i) + '\n', self.popObject.retr(i)[1])
			msg = ('',''.join(form))[1]
			info = aparser.parse(msg)
			s = (str(i), info['date'].split()[0], info['from'], info['subject'], str(len(info['attachments'])))
			string = '%s %s %20.20s "%30.30s" Att %s' % s
			#print string + '\n'
			self.logTc.AppendText(string + '\n')

	def LoginClick(self, event):
		"""Create POP3 object which connect to specified host, port and login"""
		host = self.hostTc.GetValue()
		port = self.portTc.GetValue()
		username = self.userTc.GetValue()
		passwd = self.passTc.GetValue()

		#TODO: remove this when done
		host = 'localhost'
		port = '110'
		username = 'famihug'
		passwd = 'loved@le'

		#TODO check port empty
		self.popObject = pop3lib.POP3(host, int(port))

		#this var help check whether user logged in or not
		self.loginStatus = False

		userMsg = self.popObject.user(username)
		passMsg = self.popObject.pass_(passwd)

		self.loginStatus = passMsg.__eq__('+OK Logged in.')
		if self.loginStatus:
			#Set all text control to immutable
			self.hostTc.SetEditable(False)
			self.portTc.SetEditable(False)
			self.userTc.SetEditable(False)
			self.passTc.SetEditable(False)
			#get current frame and set status text
			self.GetParent().GetParent().SetStatusText('Logged in') 
			#Print welcome info
			self.PrintLoggedIn(username, userMsg, passMsg)

	def DownloadClick(self, e):
		download.download(email.message_from_string(self.msg), '/home/famihug/out/', self.downloadTc.GetValue())

	def DownloadAllClick(self, e):
		download.download(email.message_from_string(self.msg), '/home/famihug/out/', 1000)

		#TODO use quit() TO DELETE MSG
		#self.popObject.quit()


	


app = wx.App(False)
frame = ComposerFrame(None, "XuppyMail")
#composer = ComposerPanel(frame)
nb = wx.Notebook(frame)

nb.AddPage(InboxPanel(nb), "Inbox")
nb.AddPage(ComposerPanel(nb), "Composer")
app.MainLoop()
