import wx
class ExamplePanel(wx.Panel):
	def __init__(self, parent):
	    wx.Panel.__init__(self, parent)
	
	    # create some sizers
	    mainSizer = wx.BoxSizer(wx.VERTICAL)
	    grid = wx.GridBagSizer(hgap=5, vgap=5)
	    hSizer = wx.BoxSizer(wx.HORIZONTAL)
	
	    self.quote = wx.StaticText(self, label="Your quote: ")
	    grid.Add(self.quote, pos=(0,0))
	
	    # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
	    self.content = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)
	
	    # A button
	    self.button =wx.Button(self, label="Save")
	    self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
	
	    # the edit control - one line version.
	    self.lblname = wx.StaticText(self, label="Your name :")
	    grid.Add(self.lblname, pos=(1,0))
	    self.editname = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
	    grid.Add(self.editname, pos=(1,1))
	    self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
	    self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
	
	    # add a spacer to the sizer
	    grid.Add((10, 40), pos=(2,0))
	
	
	    hSizer.Add(grid, 0, wx.ALL, 5)
	    hSizer.Add(self.content)
	    mainSizer.Add(hSizer, 0, wx.ALL, 5)
	    mainSizer.Add(self.button, 0, wx.CENTER)
	    self.SetSizerAndFit(mainSizer)


	def OnClick(self, event):
		self.content.AppendText('Click on object %s\n' % event.GetId())

	def EvtText(self, event):
		self.content.AppendText("EvtText: %s\n" % event.GetString())

	def EvtChar(self, event):
		self,content.AppendText("EvtChar: %s\n" % event.GetKeyCode())
		event.Skip()

app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
