import PythonQt
from PythonQt import QtCore, QtGui, QtUiTools
from ddapp import lcmUtils
from ddapp import applogic as app
from ddapp.utime import getUtime
from ddapp.timercallback import TimerCallback

import numpy as np
import math
from time import time
from copy import deepcopy
from multisense import command_t

def addWidgetsToDict(widgets, d):

    for widget in widgets:
        if widget.objectName:
            d[str(widget.objectName)] = widget
        addWidgetsToDict(widget.children(), d)

class WidgetDict(object):

    def __init__(self, widgets):
        addWidgetsToDict(widgets, self.__dict__)


class MultisensePanel(object):

    def __init__(self, driver):

        self.driver = driver

        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(':/ui/ddMultisense.ui')
        assert uifile.open(uifile.ReadOnly)

        self.widget = loader.load(uifile)

        self.ui = WidgetDict(self.widget.children())
        self._updateBlocked = True

        self.updateTimer = TimerCallback()
        self.updateTimer.callback = self.updatePanel
        self.updateTimer.start()

        self.widget.sendButton.setEnabled(True)

        #internal data, queued up to be sent
        self.queued_data = {}
        self.sent_data = {}

        self.queued_data['neckPitch'] = 0
        self.queued_data['spinRate'] = 3
        self.queued_data['scanDuration'] = 10
        self.queued_data['headCamFps'] = 5
        self.queued_data['headCamGain'] = 1.0
        self.queued_data['autoGain'] = True
        self.queued_data['ledOn'] = False
        self.queued_data['ledBrightness'] = 0.0

        for key in self.queued_data.keys():
            self.sent_data[key] = None

        #connect the callbacks
        self.widget.neckPitchSpinner.valueChanged.connect(self.neckPitchChange)
        self.widget.spinRateSpinner.valueChanged.connect(self.spinRateChange)
        self.widget.scanDurationSpinner.valueChanged.connect(self.scanDurationChange)

        self.widget.headCamFpsSpinner.valueChanged.connect(self.headCamFpsChange)
        self.widget.headCamGainSpinner.valueChanged.connect(self.headCamGainChange)
        self.widget.headAutoGainCheck.clicked.connect(self.headCamAutoGainChange)
        self.widget.ledOnCheck.clicked.connect(self.ledOnCheckChange)
        self.widget.ledBrightnessSpinner.valueChanged.connect(self.ledBrightnessChange)

        self.widget.sendButton.clicked.connect(self.sendButtonClicked)

        self.updatePanel()

    def ledBrightnessChange(self, event):
        self.queued_data['ledBrightness'] = self.widget.ledBrightnessSpinner.value

    def ledOnCheckChange(self, event):
        self.queued_data['ledOn'] = self.widget.ledOnCheck.isChecked()

    def headCamAutoGainChange(self, event):
        self.queued_data['autoGain'] = self.widget.headAutoGainCheck.isChecked()

    def neckPitchChange(self, event):
        self.queued_data['neckPitch'] = self.widget.neckPitchSpinner.value

    def headCamFpsChange(self, event):
        self.queued_data['headCamFps'] = self.widget.headCamFpsSpinner.value

    def headCamGainChange(self, event):
        self.queued_data['headCamGain'] = self.widget.headCamGainSpinner.value

    def spinRateChange(self, event):
        if self.queued_data['spinRate'] == self.widget.spinRateSpinner.value:
            return
        else:
            self.queued_data['spinRate'] = self.widget.spinRateSpinner.value

            #calculate spin duration
            if self.queued_data['spinRate'] == 0.0:
                self.queued_data['scanDuration'] = 240.0
            if self.queued_data['spinRate'] != 0.0 and not self.queued_data['scanDuration'] == 60.0 / self.queued_data['spinRate'] / 2.0:
                self.queued_data['scanDuration'] = 60.0 / self.queued_data['spinRate'] / 2.0
                if self.queued_data['scanDuration'] > 240.0:
                    self.queued_data['scanDuration'] = 240.0
                self.widget.scanDurationSpinner.value = self.queued_data['scanDuration']

    def scanDurationChange(self, event):
        if self.queued_data['scanDuration'] == self.widget.scanDurationSpinner.value:
            return
        else:
            self.queued_data['scanDuration'] = self.widget.scanDurationSpinner.value

            #Calculate spin rate
            if not self.queued_data['spinRate'] == 60.0 / self.queued_data['scanDuration'] / 2.0:
                self.queued_data['spinRate'] = 60.0 / self.queued_data['scanDuration'] / 2.0
                self.widget.spinRateSpinner.value = self.queued_data['spinRate']

    def sendButtonClicked(self, event):
        self.publishCommand(self.queued_data)
        self.sent_data = deepcopy(self.queued_data)

    def updatePanel(self):
        if not self.widget.isVisible():
            return

        if self.checkNewData():
            self.widget.sendButton.setEnabled(False)
        else:
            self.widget.sendButton.setEnabled(True)

    def checkNewData(self):
        match = True
        for key in self.queued_data.keys():
            if self.queued_data[key] != self.sent_data[key]:
                match = False

        return match

    def publishCommand(self, data):
        command = command_t
        print 'sending'

        command.utime = time()
        command.fps = 1 #float
        command.gain = 1.0#float
        command.rpm = 1#float
        command.agc = 1 #autogain, -1 ignore, 0 for off, 1 for on
        command.leds_flash = False #bool, false for no flash
        command.leds_duty_cycle = 0#float, 0 for off, 100 for fully on

def init(driver):

    global panel
    global dock

    panel = MultisensePanel(driver)
    dock = app.addWidgetToDock(panel.widget)
    dock.hide()

    return panel
