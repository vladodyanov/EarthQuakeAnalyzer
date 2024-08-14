import wx
from gui import SeismicAnalysisApp

if __name__ == '__main__':
    app = wx.App()
    frame = SeismicAnalysisApp()
    app.MainLoop()