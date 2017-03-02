#!/usr/bin/python
# coding: utf-8

import wx
from math import *

class CalcFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(300, 200), style=wx.DEFAULT_FRAME_STYLE^(wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)
        boxsizer = wx.BoxSizer(wx.VERTICAL)
        gridbox =wx.GridSizer(rows=6, cols=5, hgap=1, vgap=1)
        self.equation=""

        self.textprint = wx.TextCtrl(panel, -1, '', style=wx.TE_RIGHT|wx.TE_READONLY)
        self.bgFont = wx.Font(25, wx.SWISS, wx.NORMAL, wx.BOLD, face=u'Roboto')

        self.textprint.SetFont(self.bgFont)
        self.textprint.SetBackgroundColour((210, 210, 210))
        self.textprint.SetForegroundColour((15, 15, 15))

        self.buttonData = '% ^ sqrt pi AC sin ( ) e DEL cos 7 8 9 / tan 4 5 6  * ln 1 2 3 - log10 0 . = +'.split()

        buttonLength = len(self.buttonData)
        for i in range(buttonLength):
            labels = '%s' % self.buttonData[i]
            buttonItem = wx.Button(panel, i, labels)
            self.createHandler(buttonItem, labels)
            gridbox.Add(buttonItem, 0, flag=wx.EXPAND)

        boxsizer.Add(self.textprint, 1, flag=wx.EXPAND)
        boxsizer.Add(gridbox, 5, flag=wx.EXPAND)
        panel.SetSizerAndFit(boxsizer)

    def createHandler(self, button, labels):
        item = 'DEL AC ='
        if labels not in item:
            self.Bind(wx.EVT_BUTTON, self.OnAppend, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.OnDel, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)

    def OnAppend(self, event):
        eventbutton = event.GetEventObject()
        label = eventbutton.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)

    def OnDel(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        self.textprint.Clear()
        self.equation = ''

    def OnTarget(self, event):
        string = self.equation
        if '^' in string:
            string = string.replace('^', '**')
        if 'ln' in string:
            string = string.replace('ln', 'log')
        try:
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(str(target))
        except SyntaxError:
            dlg = wx.MessageDialog(self, u'格式错误', u'请注意', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

class App(wx.App):
    def OnInit(self):
        self.frame = CalcFrame(u'计算器')
        self.frame.Center()
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()
