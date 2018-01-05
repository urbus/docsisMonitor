"""
Docsis Modem Monitoring Tools
Coded By Martin Verret
using Python 3.6
14/12/2017
verret.martin@gmail.com
"""
"""
TODO:
-GUI
-Meter
-Graph
-manage multiple modem at once(LIST)
-Multi modem Graph
- Log session data into xlsx file
-Tools: ping
-Tools: Spectrum???
-variation in time(ex from start to end of monitoring, signal have change of 5 db
"""

import modemLib
from oidLib import oid
import _thread as thread
import wx
import time

version = 0.1

class gui(wx.MDIParentFrame):
	"""
	class that contain the main gui
	"""
	"""
	TODO:
	-add Tool bar
	-Context Menu
	"""
	
	
	def __init__(self):
		wx.Frame.__init__(self, None, title="Docsis Monitor {0}".format(version))
		self.menu()
		self.Show()
		self.Maximize()
		self.modem = None
		self.startWindows()
				
	def menu(self):
		"""
		Display Menu
		"""
		menubar = wx.MenuBar()
		
		fileMenu = wx.Menu()
		viewMenu = wx.Menu()
		modemMenu = wx.Menu()
		
		quitItem = fileMenu.Append(wx.ID_EXIT, 'Quitter', "Quitter l'application")#create the quit menu button
		
		modemInfo = viewMenu.Append(wx.ID_ANY, 'Info Modem', 'Afficher les informations du modem')#create the modem info menu button in vview menu
		headendInfo = viewMenu.Append(wx.ID_ANY, 'Info Headend', 'Afficher les informations du headend')#create the headend info menu button in view menu
		rfInfo = viewMenu.Append(wx.ID_ANY, 'Info RF', 'Afficher les informations RF')
		
		connect = modemMenu.Append(wx.ID_ANY, "Connecter...", "Se connecter au modem")
		
		
		menubar.Append(fileMenu, '&Fichier')#create the file menu
		menubar.Append(viewMenu, 'Affichage')
		menubar.Append(modemMenu, "Modem")
		self.SetMenuBar(menubar)
		
		self.Bind(wx.EVT_MENU, self.exit, quitItem)
		
		self.Bind(wx.EVT_MENU, self.modemInfo, modemInfo)
		self.Bind(wx.EVT_MENU, self.headendInfo, headendInfo)
		self.Bind(wx.EVT_MENU, self.rfInfo, rfInfo)
		
		self.Bind(wx.EVT_MENU, self.connectModem, connect)
		
		
	def startWindows(self):
		"""
		function to automatically start windows on open
		"""
		#self.modemInfo(None)
		#self.headendInfo(None)
		#self.rfInfo(None)
		
	def connectModem(self ,e):
		"""
		Function to set the ip of the modem we want to monitor
		"""
		
		text= wx.TextEntryDialog(self, "Veuillez entrer l'adresse IP du modem", "", style= wx.OK | wx.CANCEL | wx.STAY_ON_TOP)#wx.Statictext(connectModemWindow, -1, style=wx.ALIGN_CENTER)
	
		if text.ShowModal() == wx.ID_OK:
			modemIP = text.GetValue()
			testString = modemIP.split(".")
			i = 0
			if len(testString) == 4:
				for value in testString:
					if (len(value) <= 3) and (int(value) >= 0) and (int(value) < 255):
						i += 1
			if i == 4:
				self.modem = modemLib.modem(modemIP)
			else:
				wrongIP = wx.MessageDialog(self, 'Adresse IP Invalide', 'Erreur', style=wx.ICON_ERROR | wx.OK | wx.STAY_ON_TOP)
				wrongIP.ShowModal()
					
		text.Destroy()
		
		#connectModemWindow.Show()
	def loopFunction(self, function, args, updateRate, parentFunction):
		"""
		function to loop another function
		"""	
		global rfInfoLoop
		global headendInfoLoop
		global modemInfoLoop
		
		rfInfoLoop = True
		headendInfoLoop = True
		modemInfoLoop = True
		
		bool = True
		while bool:	
			
			if not rfInfoLoop and parentFunction == "rfInfo":
				bool = False
			elif not headendInfoLoop and parentFunction == "headendInfo":
				bool = False
			elif not modemInfoLoop and parentFunction == "modemInfo":
				bool = False
			else:	
				function(*args)
				time.sleep(updateRate)
					
	def rfInfo(self, e):
		"""
		function to open the headend info window
		"""
		global rfInfoLoop 
		#rfInfoLoop = True
		def dynamicSlow(self, list):
			"""
			function to show data that need a slow update rate
			"""
			list.SetItem(0, 1, str(self.modem.downstreamChannelID()))
			list.SetItem(0, 2, "{0} MHz".format(self.modem.downstreamFreq()))
			list.SetItem(0, 3, "{0} MHz".format(self.modem.downstreamWidth()))
			
			list.SetItem(1, 1, str(self.modem.upstreamChannelID()))
			list.SetItem(1, 2, "{0} MHz".format(self.modem.upstreamFreq()))
			list.SetItem(1, 3, "{0} MHz".format(self.modem.upstreamWidth()))
			
			
						
		def dynamicFast(self, list):
			"""
			function to show data that need a fast update rate
			"""
		def stopLoop(e):
			global rfInfoLoop
			rfInfoLoop = False
						
		while self.modem == None:
			self.connectModem(None)
		
		rfInfoWindow = wx.MDIChildFrame(self, title="Info RF", size=(405,120), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		list = wx.ListCtrl(rfInfoWindow, style=wx.LC_REPORT)
		
		list.InsertColumn(0, "")
		list.InsertColumn(1, "ID Canal")
		list.InsertColumn(2, "Fréquence")
		list.InsertColumn(3, "Largeur de bande")
		#list.InsertColumn(4, "Modulation")#i don't have this data yet
		
		list.InsertItem(0, "Downstream")
		list.InsertItem(1, "Upstream")
		
		list.SetColumnWidth(3, 135)
			
		#field with dynamic data, must be updated frequently
		thread.start_new_thread(self.loopFunction, (dynamicSlow, (self, list), 10, "rfInfo"))
		#thread.start_new_thread(self.loopFunction, (dynamicFast, (self, list), 0.5))
		
		meter = self.meterBarWidget(self, -1, -30, 30, 0, (100,100))#test for meter bar
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(list, 0, wx.ALL| wx.EXPAND, 5)
		rfInfoWindow.SetSizer(sizer)
		rfInfoWindow.SetPosition((420,225))
		rfInfoWindow.Bind(wx.EVT_CLOSE, stopLoop)
		rfInfoWindow.Show()		
		
	def headendInfo(self, e):
		"""
		function to open the headend info window
		"""
		global headendInfoLoop
		#headendInfoLoop = True
		def dynamicSlow(self, list):
			"""
			function to show data that need a slow update rate
			"""
			list.SetItem(0, 1, "N/A")#"Some data i don't have yet")
			list.SetItem(1, 1, self.modem.timeServer())
			list.SetItem(2, 1, self.modem.dhcpServer())
			list.SetItem(3, 1, self.modem.tftpServer())
			list.SetItem(5, 1, self.modem.configFile())
			
		def dynamicFast(self, list):
			"""
			function to show data that need a fast update rate
			"""
			netTime = self.modem.networkTime()
			list.SetItem(4, 1,"{0}-{1}-{2}, {3}:{4}:{5}.{6} UTC {7}{8}:{9}".format(netTime[2], netTime[1], netTime[0], netTime[3], netTime[4], netTime[5], netTime[6], netTime[7], netTime[8], str(netTime[9]).zfill(2)))
			#year, month, day, hours, minutes, seconds, deciSeconds, utcDirection, hoursFromUTC, minutesFromUTC

		def stopLoop(e):
			global headendInfoLoop
			headendInfoLoop = False
		
		while self.modem == None:
			self.connectModem(None)
		
		headendInfoWindow = wx.MDIChildFrame(self, title="Info Headend", size=(400,170), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		list = wx.ListCtrl(headendInfoWindow, style=wx.LC_REPORT | wx.LC_NO_HEADER)
		
		list.InsertColumn(0, "Data", format=wx.LIST_FORMAT_CENTER)#will not be shown 
		list.InsertColumn(1, "Value")#will not be shown
		
		list.SetColumnWidth(0, 135)
		list.SetColumnWidth(1, 230)
		
		list.InsertItem(0, "IP du routeur")
		list.InsertItem(1, "IP du serveur TFTP")
		list.InsertItem(2, "IP du serveur DHCP")
		list.InsertItem(3, "IP du serveur de temps")
		list.InsertItem(4, "Temps réseau")
		list.InsertItem(5, "Fichier de configuration")
		
		#field with dynamic data, must be updated frequently
		thread.start_new_thread(self.loopFunction, (dynamicSlow, (self, list), 5, "headendInfo"))
		thread.start_new_thread(self.loopFunction, (dynamicFast, (self, list), 0.05, "headendInfo"))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(list, 0, wx.ALL| wx.EXPAND, 5)
		headendInfoWindow.SetSizer(sizer)
		headendInfoWindow.SetPosition((10,225))
		headendInfoWindow.Bind(wx.EVT_CLOSE, stopLoop)
		headendInfoWindow.Show()
		
	def modemInfo(self, e):
		"""
		function to show  modem info
		"""
		global modemInfoLoop
		modemInfoLoop = True
		def dynamicFast(self, list):
			"""
			function to print dynamic data that must be updated frequently
			"""
			if self.modem.ethStatus() == "UP":
				ethStatus = "Connecté"
			elif self.modem.ethStatus() == "DOWN":
				ethStatus = "Déconnecté"
			else:
				ethStatus = "Timeout"
				
			if self.modem.standbyMode() == True:
				standby = "Activé"
			elif self.modem.standbyMode() == False:
				standby = "Désactivé"
			else:
				standby = "Timeout"
				
			uptime = self.modem.uptime()
			if uptime == "Timeout":
				value = "Timeout"
			else:
				value = "{0} Jours, {1} Heures, {2} Minutes, {3} Secondes".format(uptime[0], uptime[1], uptime[2], uptime[3])
				
			list.SetItem(5, 1, ethStatus)
			list.SetItem(6, 1, standby)
			list.SetItem(7, 1, value)
			
		def dynamicSlow(self, list):
			"""
			function to fill server with dynamic update
			"""
			list.SetItem(0, 1, self.modem.version())
			list.SetItem(1, 1, self.modem.model())
			list.SetItem(2, 1, self.modem.IP)
			list.SetItem(3, 1, self.modem.dhcpIP())
			list.SetItem(4, 1, self.modem.hwAddress())

		def stopLoop(e):
			global modemInfoLoop
			modemInfoLoop = False
			print("stopLoop")
			modemInfoWindow.Destroy()
		
		while self.modem == None:
			self.connectModem(None)
			
		
		modemInfoWindow = wx.MDIChildFrame(self, title="Info Modem", size=(800,205), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		list = wx.ListCtrl(modemInfoWindow, style=wx.LC_REPORT | wx.LC_NO_HEADER)
		
		list.InsertColumn(0, "Data", format=wx.LIST_FORMAT_CENTER)#will not be shown 
		list.InsertColumn(1, "Value")#will not be shown
		list.InsertItem(0, "Version")
		list.SetColumnWidth(1, 640)
		list.InsertItem(1, 'Modele')
		list.InsertItem(2, 'IP Cible')
		list.InsertItem(3, 'IP Assigné par DHCP')
		list.SetColumnWidth(0, 125)
		list.InsertItem(4, 'Adresse MAC')
		list.InsertItem(5, 'Port LAN')
		list.InsertItem(6, 'Standby')
		list.InsertItem(7, 'Uptime')
		
		#field with dynamic data, must be updated frequently
		thread.start_new_thread(self.loopFunction, (dynamicSlow, (self, list), 5, "modemInfo"))
		thread.start_new_thread(self.loopFunction, (dynamicFast, (self, list), 0.05, "modemInfo"))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(list, 0, wx.ALL| wx.EXPAND, 5)
		modemInfoWindow.SetSizer(sizer)
		modemInfoWindow.SetPosition((10,10))
		modemInfoWindow.Bind(wx.EVT_CLOSE, stopLoop, modemInfoWindow)		
		modemInfoWindow.Show()
						
	def exit(self, e):
		"""
		function to exit the program
		"""
		self.Close()
		
	class meterBarWidget(wx.Panel):

		def __init__(self, parent, id, min, max, level, pos1):
			wx.Panel.__init__(self, parent, id, size=((200*3)+4,50))
			
			self.level = level
			self.min = min
			self.max = max
			self.parent = parent
			self.SetBackgroundColour('#000000')
			
			self.Bind(wx.EVT_PAINT, self.meter)
			
		def meter(self, event):
			dc = wx.PaintDC(self)
			
			
			greenOn = '#36ff27'
			greenOff = '#075100'
			redOn = '#ff3627'
			redOff= '#510700'
			yellowOn= '#fffb27'
			yellowOff = '#465100'
			
			dc.SetDeviceOrigin(0,50)
			dc.SetAxisOrientation(True, True)
							
			def getData(self):
				"""
				Function to get Data
				"""
				pos = self.level + abs(self.min)#signal position
				rect = pos / ((self.max-self.min)/200) #each rectangle have a value of

				for i in range(1, 200):
					if i > rect:
						dc.SetBrush(wx.Brush(greenOff))
						dc.DrawRectangle(i*3, 10, 4, 30)
						
					else:
						dc.SetBrush(wx.Brush(greenOn))
						dc.DrawRectangle(i*3, 10, 4, 30)
						
			getData(self)

if __name__ == "__main__":
	#modem1 = modemLib.modem("10.10.22.2")
	#print(modem1.IP)
	#print(modem1.maxCPE())
	#screen = gui()
	app = wx.App()
	window = gui()
	app.MainLoop()
