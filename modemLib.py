from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import *
from oidLib import oid
import time
import binascii
"""
TODO:
-Speed usage calculation for download and upload
"""


class modem:
	"""
	class to handle all the modem related information:
	-error rate for both
	-download and upload speed
	"""
	def __init__(self, IP):
		"""
		init function, must receive Modem Private IP as VAR
		"""
		self.IP = IP
		self.community = "public"
		self.snmpPort = 161
		#print(IP)
		#print(self.snmpGet("1.3.6.1.2.1.69.1.3.3.0"))
		
	def snmpGet(self, oid):
		"""
		function to query snmp for data
		
		"""
		data = getCmd(SnmpEngine(),
		CommunityData(self.community),
		UdpTransportTarget((self.IP, self.snmpPort)),
		ContextData(),
		ObjectType(ObjectIdentity(oid))
		)
				
		errorIndication, errorStatus, errorIndex, varBinds = next(data)
		
		
		if errorIndication:
			if str(errorIndication) == "No SNMP response received before timeout":
				return "Timeout"#if we receive an timeout error message return timeout
			else:
				print(type(errorIndication))
				
		elif errorStatus:
			print('%s at %s' % (
								 errorStatus.prettyPrint(),
								 errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
							   )
				  )
		else:
			for varBind in varBinds:
				return varBind
				#print(' = '.join([x.prettyPrint() for x in varBind]))
				
	def snmpNext(self, oid):
		"""
		function to query snmp for data
		
		"""
		data = nextCmd(SnmpEngine(),
		CommunityData(self.community),
		UdpTransportTarget((self.IP, self.snmpPort)),
		ContextData(),
		ObjectType(ObjectIdentity(oid))
		)
				
		errorIndication, errorStatus, errorIndex, varBinds = next(data)
		
		
		if errorIndication:
			if str(errorIndication) == "No SNMP response received before timeout":
				return "Timeout"#if we receive an timeout error message return timeout
			else:
				print(type(errorIndication))
				
		elif errorStatus:
			print('%s at %s' % (
								 errorStatus.prettyPrint(),
								 errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
							   )
				  )
		else:
			#for varBind in varBinds:
			return varBinds
				#print(' = '.join([x.prettyPrint() for x in varBind]))
	
	def dhcpIP(self):
		"""
		function to get ip from modem
		"""
		data = self.snmpGet(oid.dhcpIP)
		if data == "Timeout":
			return data
		else:
			modemIP = str(data).split("=")[1].replace(" ","")
			return modemIP
								
	def uptime(self):
		"""
		funtction to get modem uptime
		"""
		data = self.snmpGet(oid.uptime)
		if data == "Timeout":
			return data
		else:		
			timeticks = int(str(data).split("=")[1])
			d = int(timeticks / 8640000)
			h = int((timeticks % 8640000) / 360000)
			m = int(((timeticks % 8640000) % 360000) / 6000)
			s = int((((timeticks % 8640000) % 360000) % 6000) / 100)
			return (d, h, m, s)	
			#print("Uptime: {0} jours, {1} heures, {2} minutes, {3} secondes".format(d, h, m, s))
		
	def downloadSpeed(self):
		"""
		function to get data speed from number of octet
		"""
		data = self.snmpGet(oid.downloadOctets)
		if data == "Timeout":
			return data
		else:
			dataCount1 = int(str(data).split("=")[1])
			time1 = time.time()
			time.sleep(0.5)
			data2 = self.snmpGet(oid.downloadOctets)
			if data2 == "Timeout":
				return data2
			else:
				dataCount2 = int(str(data2).split("=")[1])
				time2 = time.time()
				downSpeed = (dataCount2 - dataCount1) * 8/ (time2 - time1)
				return downSpeed
		
	def downstreamPower(self):
		"""
		function to get downstrem Power from modem
		"""
		data = self.snmpGet(oid.downstreamSignal)
		if data == "Timeout":
			return data
		else:
			downstreamPwr = float(str(data).split("=")[1])/10
			return downstreamPwr 
			
	def uploadSpeed(self):
		"""
		function to get data speed from number of octet
		"""
		data = self.snmpGet(oid.uploadOctets)
		if data == "Timeout":
			return data
		else:
			dataCount1 = int(str(data).split("=")[1])
			time1 = time.time()
			time.sleep(0.5)
			data2 = self.snmpGet(oid.uploadOctets)
			if data2 == "Timeout":
				return data2
			else:
				dataCount2 = int(str(data2).split("=")[1])
				time2 = time.time()
				upSpeed = (dataCount2 - dataCount1) * 8/ (time2 - time1)
				return upSpeed
		
	def upstreamPower(self):
		"""
		function to get upstrem Power from modem
		"""
		data = self.snmpGet(oid.upstreamSignal)
		if data == "Timeout":
			return data
		else:
			upstreamPwr = float(str(data).split("=")[1])/10
			return upstreamPwr
		
	def downstreamSNR(self):
		"""
		function to get downstream SNR from modem
		"""
		data = self.snmpGet(oid.downstreamSNR)
		if data == "Timeout":
			return data
		else:
			SNR = float(str(data).split("=")[1])/10
			return SNR
		
	def ethStatus(self):
		"""
		function to get status of eth interface
		"""
		data = self.snmpGet(oid.ethUp)
		if data == "Timeout":
			return data
		else:
			status = int(str(data).split("=")[1])
			if status == 1:
				status = "UP"
			elif status == 2:
				status = "DOWN"
			else:
				status = "Testing"
				
			return status
		
	def hwAddress(self):
		"""
		function to get hardware address(mac) from modem
		"""
		data = self.snmpGet(oid.macAddress)
		if data == "Timeout":
			return data
		else:
			mac = str(data).split("=")[1].replace(" ", "")
			
			mac = mac[2:]#remove the 0x
			
			mac = ":".join([mac[:2],mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12]])
			
			return mac
		
	def configFile(self):
		"""
		Function to get the config file name of the modem
		"""
		data = self.snmpGet(oid.configFile)
		if data == "Timeout":
			return data
		else:
			config = str(data).split("=")[1].replace(" ","")
			
			return config
		
	def model(self):
		"""
		function to get model number from modem
		"""
		data = self.snmpGet(oid.model)
		if data == "Timeout":
			return data
		else:
			model = str(data).split("=")[1].replace(" ","")
			
			return model
		
	def standbyMode(self):
		"""
		function to look if standby mode is on or off
		"""
		data = self.snmpGet(oid.standby)
		if data == "Timeout":
			return data
		else:
			standby = int(str(data).split("=")[1])
			
			if standby == 1:
				standby = True
			elif standby == 2:
				standby = False
				
			return standby
	
	def version(self):
		"""
		function to get the sysDesc line that inform us of the version
		"""
		data = self.snmpGet(oid.version)
		if data == "Timeout":
			return data
		else:
			modemVersion = str(data).split("=")[1].replace(" ","")
			
			return modemVersion
		
	def upstreamWidth(self):
		"""
		function to get upstream width from modem
		"""
		data = self.snmpGet(oid.upstreamWidth)
		if data == "Timeout":
			return data
		else:
		
			upWidth = int(str(data).split("=")[1].replace(" ",""))/1000000
			return upWidth
			
	def upstreamFreq(self):
		"""
		Functino to get the upstream frequency
		"""
		data = self.snmpGet(oid.upstreamFreq)
		if data == "Timeout":
			return data
		else:
			upFreq = int(str(data).split("=")[1].replace(" ",""))/1000000
			
			return upFreq
			
	def upstreamChannelID(self):
		"""
		Function to get channel ID from modem
		"""
		data = self.snmpGet(oid.upstreamChannelID)
		if data == "Timeout":
			return data
		else:
			upChannelID = int(str(data).split("=")[1].replace(" ",""))
			
			return upChannelID
			
	def downstreamWidth(self):
		"""
		function to get downstream width from modem
		"""
		data = self.snmpGet(oid.downstreamWidth)
		if data == "Timeout":
			return data
		else:
		
			downWidth = int(str(data).split("=")[1].replace(" ",""))/1000000
			return downWidth
			
	def downstreamFreq(self):
		"""
		Functino to get the downstream frequency
		"""
		data = self.snmpGet(oid.downstreamFreq)
		if data == "Timeout":
			return data
		else:
			downFreq = int(str(data).split("=")[1].replace(" ",""))/1000000
			
			return downFreq
			
	def downstreamChannelID(self):
		"""
		Function to get downstream channel ID from modem
		"""
		data = self.snmpGet(oid.downstreamChannelID)
		if data == "Timeout":
			return data
		else:
			downChannelID = int(str(data).split("=")[1].replace(" ",""))
			
			return downChannelID
			
	def timeServer(self):
		"""
		function to get time server ip
		"""
		data = self.snmpGet(oid.timeServerIP)
		if data == "Timeout":
			return data
		else:
			ntpServer = str(data).split("=")[1].replace(" ","")
			return ntpServer
			
	def dhcpServer(self):
		"""
		function to get dhcp server ip
		"""
		data = self.snmpGet(oid.dhcpServerIP)
		if data == "Timeout":
			return data
		else:
			dhcpServerIP = str(data).split("=")[1].replace(" ","")
			return dhcpServerIP
			
	def tftpServer(self):
		"""
		function to get tftp server ip
		"""
		data = self.snmpGet(oid.tftpServerIP)
		if data == "Timeout":
			return data
		else:
			bootServer = str(data).split("=")[1].replace(" ","")
			return bootServer
			
	def networkTime(self):
		"""
		Function to get Network Time from modem
		"""
		data = self.snmpGet(oid.networkTime)
		if data == "Timeout":
			return data
		else:
			netTime = str(data).split("=")[1].replace(" ","")[2:]
			year = int(netTime[1:4], 16)
			month = int(netTime[4:6], 16)
			day = int(netTime[6:8], 16)
			hours = int(netTime[8:10], 16)
			minutes = int(netTime[10:12], 16)
			seconds = int(netTime[12:14], 16)
			deciSeconds = int(netTime[14:16], 16)#could be not shown
			utcDirection = binascii.unhexlify(str.encode(netTime[16:18])).decode()
			hoursFromUTC = int(netTime[18:20], 16)
			minutesFromUTC = int(netTime[20:22], 16)
			return [year, month, day, hours, minutes, seconds, deciSeconds, utcDirection, hoursFromUTC, minutesFromUTC]
			