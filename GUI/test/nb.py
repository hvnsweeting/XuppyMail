import wx

app = wx.App(False)
frame = wx.Frame(None,title="Hehe")
nb = wx.Notebook(frame)

nb.AddPage(wx.Panel(nb),"Page 1")
nb.AddPage(wx.Panel(nb),"Page 2")
frame.Show()
app.MainLoop()
