import wx
class ExamplePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self,parent)
		self.quote = wx.StaticText(self, label="hehe", size=(200,-1))
		self.Show()

		self.logger = wx.TextCtrl(self, pos=(300,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

		#button
		self.button = wx.Button(self, label="save", pos=(200,325))
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

		#editcontrol
		self.lblname = wx.StaticText(self, label="From: ", pos=(20,60))
		self.recv = wx.TextCtrl(self, value="enter receiver", pos=(150,60), size=(140,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.recv)
		self.Bind(wx.EVT_CHAR, self.EvtChar, self.recv)

	def EvtText(self, event):
		self.logger.AppendText('EvtText: %s\n' % event.GetString())

	def EvtChar(self, event):
		self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
		event.Skip()

	def OnClick(self, event):
		self.logger.AppendText('Click on object with ID %d \n' % event.GetId())

app = wx.App(False)
frame = wx.Frame(None)
nb = wx.Notebook(frame)

nb.AddPage(ExamplePanel(nb), "Absolute position")
nb.AddPage(ExamplePanel(nb), "Page two")
nb.AddPage(ExamplePanel(nb), "Page three")

frame.Show()
app.MainLoop()
