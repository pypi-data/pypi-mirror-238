# Overhead People Counting 3D - ISK & AOP Raw Data (OHPC)
# ver:2.0
# 2022/04/19
# 
# parsing People Counting 3D data use AOP-ISK
# hardware:(Batman-201)ISK IWR6843 ES2.0 & BM-501 AOP
#    Fireware version: I470
# Fit : wall mount
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8 Raw data
# v0.0.1 : 2020/06/19 release
#          (1)Output list data
# v0.1.0 : 2021/04/01 
#          (1)Output DataFrame
# v0.1.1 : 2021/08/12
#           (doppler and range swap in V6 output)
# v0.1.2 : 2021/09/17
#           v7 dataframe:'tid' move to front of 'ec0'
# v2.0 : 2022/04/19
#          pc3_v2: add ec[16],g,confidenceLevel
#          this version lib same as pc3OVH 
#
# v2.0.1: 2022/06/10 v6 add sx,sy,sz
#
# v2.0.2: 2022/06/13 added azimuth offset
#                    azi_offset
# v2.0.3: 2023/06/30 add playback read v2


import serial
import time
import struct
import pandas as pd
import numpy as np

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	subframeNumber = 0
	chirpMargin = 0
	frameMargin = 0 
	trackProcessTime = 0
	uartSendTime = 0
	numTLVs = 0
	checksum = 0

class unitS:
	elevationUnit:float = 0.0
	azimuthUnit : float = 0.0
	dopplerUnit :float = 0.0
	rangeUnit :float = 0.0
	snrUnit :float = 0.0

class Pc3_v2:
	#magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	u = unitS
	frameNumber = 0
	azi_offset = 0.0
	
	# provide csv file dataframe
	# real-time 
	v6_col_names_rt = ['fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz'] 
	v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
	v8_col_names_rt = ['fN','type','targetID']
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
	#v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
	v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi'] #v0.1.2
	v8_col_names = ['time','fN','type','targetID']
	sim_startFN = 0
	sim_stopFN  = 0 
	vxx_col_names = ['fN','type','i0','i1','i2','i3','i4', 'i5','i6','i7', 'i8','i9','i10','i11']
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm  = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port, degree = None):
		self.port = port
		self.azi_offset = 0.0 if degree == None else degree * 3.14159/180.0
		
		print("(jb)People Counting 3D v2.0 (Wall Mount) initial")
		print("(jb)vsersion:v2.0")
		print("(jb)For Hardware:Batman-201(ISK) & BM-501 (AOP)")
		print("(jb)Hardware: IWR-6843 & AOP")
		print("(jb)Firmware: PC3-I470")
		print("(jb)UART Baud Rate:921600")
		print("Output: V6,V7,V8 data:(RAW)")
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("******* Header ********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.trackProcessTime))
		print("UART Send Time:\t{:d} us".format(self.hdr.uartSendTime))
		print("Inter-chirp Processing Margin:\t{:d} us".format(self.hdr.chirpMargin))
		print("Inter-frame Processing Margin:\t{:d} us".format(self.hdr.frameMargin))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("Check Sum   :\t{:x}".format(self.hdr.checksum))
		print("***End Of Header***") 
			
	#for class internal use
	def tlvTypeInfo(self,dtype,count,dShow):
		
		sbyte = 8  #tlvHeader Struct = 8 bytes
		unitByte = 20 
		dataByte = 0
		pString = ""
		nString = "numOfPoints :"
		stateString = "V6-unit"
		if dtype == 6:
			unitByte = 20  #pointUnit= 20bytes (elvUnit(4),aziUnit(4),dopplerUnit(4),rangeUnit(4),snrUnit(4))
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 8    #pointStruct 8bytes:(elevation(1),azimuth(1),doppler(2),range(2),snr(2))
			pString = "Point Cloud TLV and pointUnit"
			nString = ""
		elif dtype == 7:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8 	   #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte = 112  #target struct 112 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi)  
			pString = "Target Object TLV"
			nString = "numOfObjects:"
			stateString = "V7"
		elif dtype == 8:
			unitByte = 0 #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte = 1 #targetID = 1 byte
			pString = "Target Index TLV"
			nString = "numOfIDs"
			stateString = "V8"
		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 
		retCnt = count - unitByte -sbyte
		nPoint = retCnt / sbyte
		#dShow = True
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}B):  \t{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))  
		
		return unitByte,stateString, sbyte, dataByte,retCnt, int(nPoint)
		
	def list2df(self,dck,l6,l7,l8):
		ll6 = pd.DataFrame(l6,columns=self.v6_col_names_rt)
		ll7 = pd.DataFrame(l7,columns=self.v7_col_names_rt)
		ll8 = l8 #pd.DataFrame(l8,columns=self.v8_col_names_rt)
		return (dck,ll6,ll7,ll8)

#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
#     df: 
# output:(return parameter)
# (pass_fail, v6, v7, v8)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud infomation
#  v7: Target Object information
#  v8: Target Index information
#  
# 
#
	def tlvRead(self,disp,df = None):
		
		#print("---tlvRead---")
		#ds = dos
		typeList = [6,7,8]
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		numOfPoints = 0
		tlvCount = 0
		pbyte = 16
		v6 = ([])
		v7 = ([])
		v8 = ([])
		v6df = ([])
		v7df = ([])
		v8df = ([])
		
		while True:
			try:
				ch = self.port.read()
			except:
				#return (False,v6,v7,v8)
				#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6,v7,v8)
				return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[idx]:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx += 1
					if idx == 8:
						 
						idx = 0
						lstate = 'header'
						rangeProfile = b""
						sbuf = b""
				else:
					#print("not: magicWord state:")
					idx = 0
					rangeProfile = b""
					#return (False,v6,v7,v8)
					#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 40: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,
						self.hdr.frameNumber,self.hdr.subframeNumber,
						self.hdr.chirpMargin,self.hdr.frameMargin,self.hdr.trackProcessTime,self.hdr.uartSendTime,
						self.hdr.numTLVs,self.hdr.checksum) = struct.unpack('9I2H', sbuf)
						self.frameNumber = self.hdr.frameNumber
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						#return (False,v6,v7,v8)
						#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					#print("tlvCount:{:}".format(tlvCount))
					if self.hdr.numTLVs == 0:
						#return (True,v6,v7,v8)
						#return (True,v6,v7,v8) if (df == None) else self.list2df(True,v6df,v7df,v8df)
						return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 44:
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8)
					#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#print("--tlvNum:{:d}: tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							#return (False,v6,v7,v8)
							#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
							return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						#return (False,v6,v7,v8)
						#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					#if ttype == 6:
					#	print("--pointCloud:((tlvLength({:d})-pointUnit(20)-tlvStruct(8))/8={:d}".format(self.tlvLength,numOfPoints))
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
			
			elif lstate == 'V6-unit':
				sbuf += ch
				idx += 1
				if idx == unitByteCount :
					#print(":".join("{:02x}".format(c) for c in sbuf))
					#print("unitByte:{:d}".format(len(sbuf)))
					try:
						self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit = struct.unpack('5f', sbuf)
						#print("Unit  ==> elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit))
						sbuf = b""
						idx = 0
						lstate = 'V6'				
					except:
						if self.dbg == True:
							print("(6.0)Improper Type 6 unit Value structure found: ")
						#return (False,v6,v7,v8)
						#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
					if self.sm == True:
						print("(V6-unit:{:d})=>({:})".format(tlvCount,lstate))
						#print("(V6-unit)=>({:})".format(lstate))
					
			elif lstate == 'V6': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(e,a,d,r,s) = struct.unpack('2b3h', sbuf)
						elv = e * self.u.elevationUnit
						azi = a * self.u.azimuthUnit + self.azi_offset
						dop = d * self.u.dopplerUnit
						ran = r * self.u.rangeUnit
						snr = s * self.u.snrUnit
						#print("({:2d}:{:4d})(idx:({:4d}) elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(numOfPoints,lenCount,idx,elv,azi,dop,ran,snr))
						sz  = ran * np.sin(elv)
						sx  = ran * np.cos(elv) * np.sin(azi)
						sy  = ran * np.cos(elv) * np.cos(azi)
						
						if (df == 'DataFrame'):
							#v6df.append((self.hdr.frameNumber,'v6',elv,azi,dop,ran,snr,sx,sy,sz)) #v0.1.0
							v6df.append((self.hdr.frameNumber,'v6',elv,azi,ran,dop,snr,sx,sy,sz)) #v0.1.1
							 
						else:
							#v6.append((elv,azi,dop,ran,snr)) 
							v6.append((elv,azi,dop,ran,snr,sx,sy,sz)) #v2.0.1
						
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
						
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						#return (False,v6,v7,v8)
						#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V6:{:d})=>(idle) :true".format(tlvCount))
						#return (True,v6,v7,v8)
						#return (True,v6,v7,v8) if (df == None) else self.list2df(True,v6df,v7df,v8df)
						return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
						
					else: # Go to TL to get others type value
						lstate = 'TL' #'tlTL'
						if self.sm == True:
							print("(V6:{:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					#return (False,v6,v7,v8)
					#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6,v7,v8)
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V7:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						#(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ) = struct.unpack('I9f', sbuf)
						(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi) = struct.unpack('I27f', sbuf)
						if (df == 'DataFrame'): 
							v7df.append((self.hdr.frameNumber,'v7',posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi,tid))
							
						else:
							v7.append((tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi))
						
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						#return (False,v6,v7,v8)
						#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
						
				if idx >= lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					 
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle) :true")
						#return (True,v6,v7,v8)
						#return (True,v6,v7,v8) if (df == None) else self.list2df(True,v6df,v7df,v8df)
						return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V7)=>(TL)")

				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					#return (False,v6,v7,v8)
					#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
			elif lstate == 'V8':
				idx += 1
				v8.append(ord(ch))
				
				if idx == lenCount:
					if disp == True:
						print("=====V8 End====")						
					sbuf = b""
					idx = 0
					lstate = 'idle'
					if self.sm == True:
						print("(V8:{:d})=>(idle)".format(tlvCount))
					
					if (df == 'DataFrame'):
						v8df = [self.hdr.frameNumber,'v8']
						v8df.extend(v8)
						
					#return (True,v6,v7,v8) if (df == None) else self.list2df(True,v6df,v7df,v8df)
					return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8)
					#return (False,v6,v7,v8) if (df == None) else self.list2df(False,v6df,v7df,v8df)
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
	def v67Simlog(frameNum):
		global sim_startFN,sim_stopFN
		s_fn = frameNum + sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = v6sim[v6sim['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = v7sim[v7sim['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d)
		
	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = self.v6simo[self.v6simo['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = self.v7simo[self.v7simo['fN'] == s_fn]
		v8d = self.v8simo[self.v8simo['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d,v8d)
	
	def readFile(self,fileName):
		
		self.fileName = fileName 
		df = pd.read_csv(self.fileName)
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df.info())
		#print(df.info(memory_usage="deep")) 
		
		#    ['fN','type','elv','azimuth','range' ,'doppler','snr','sx', 'sy', 'sz']
		#     fN','type','elv', 'azimuth','range' ,'doppler','snr','sx', 'sy', 'sz'
		#[time,fN,type,   posX,    posY,    posZ,    velX,   velY , velZ, accX, accY, accZ, ec0, ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi,tid]    
		#   0   1   2       3       4        5         6       7     8     9    10    11    12   13   14  15  16  17  18 19  20   21   22  23    24   25  26   27  28 29    30

		
		self.v6simo = df[df['type'] == 'v6'].drop(['time','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid'], 
		axis=1).rename(columns={'posX':'elv','posY': 'azimuth','posZ': 'range' , 'velX' : 'doppler','velY': 'snr','velZ': 'sx' ,'accX':'sy','accY':'sz'})
		
		self.v7simo = df[df['type'] == 'v7'].drop(['time'],axis=1)
		
		self.v8simo = df[df['type'] == 'v8'].drop(['time','posY','posZ','velX','velY','velZ','accX','accY','accZ',
													'ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8',
													'ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid'],axis=1).rename(columns={'posX':'targetID'})
		
		self.sim_startFN = int(df['fN'].values[1])
		self.sim_stopFN  = int(df['fN'].values[-1])
		
		#print(f'self.sim_startFN  = {self.sim_startFN} self.sim_stopFN = {self.sim_stopFN} ')
		return (self.v6simo,self.v7simo,self.v8simo)
		
		

	
	################### v2 ############## 
	
		
	def readFile_v2(self,fileName):
		#fileName = "pc32021-03-19-10-02-17.csv"  
		#df = pd.read_csv(fileName, error_bad_lines=False, warn_bad_lines=False) 
		self.fileName = fileName 
		df = pd.read_csv(self.fileName)
		
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df.info())
		#print(df.info(memory_usage="deep")) 
		
		# vxx_col_names = ['fN','type','i0','i1','i2','i3','i4', 'i5','i6','i7     , i8',   'i9' 
		#                              (elv,azi ,dop ,ran, snr,   sx,  sy,  sz , Associate)
		self.v6simo = df[df['type'] == 'v6'].drop(['i9'], axis=1).rename(columns={'i0': 'elv', 'i1': 'azi', 'i2': 'dop', 'i3': 'range', 'i4': 'snr',
																					'i5': 'sx', 'i6': 'sy', 'i7' : 'sz' , 'i8':'Ass' })
		
		self.v7simo = df[df['type'] == 'v7'].rename(columns={'i0': 'tid', 'i1': 'posX', 'i2': 'posY', 'i3': 'posZ', 'i4': 'velX', 'i5': 'velY', 'i6': 'velZ', 'i7': 'accX', 'i8': 'accY', 'i9': 'accZ','i10':'g','i11':'c'})
		#   
		#print("======v7simo=========")
		#print(self.v7simo)
		self.sim_startFN = int(df['fN'].values[1])
		self.sim_stopFN  = int(df['fN'].values[-1])
		return (self.sim_startFN,self.sim_stopFN,self.v6simo,self.v7simo)
		
	def getRecordData_v2(self,frameNum):
		s_fn =  frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v68d = self.v6simo[(self.v6simo.fN ==  s_fn)]
		#                     eadrsxyzif
		#v68o = v68d.loc[:,['range','elv','azi','dop','sx','sy','sz','snr','Ass','fN']].apply(pd.to_numeric)
		v68o = v68d.loc[:,['elv','azi','dop','range','snr','sx','sy','sz','Ass','fN']].apply(pd.to_numeric)
		
		v7d = self.v7simo[(self.v7simo.fN ==  s_fn)]
		v7o = v7d.loc[:,['tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','fN']].apply(pd.to_numeric)
		return(v68o,v7o)
		

	def recording_pc3_v2(self,writer= None,v68=None,v7=None,fn = None):
		if v68 is not None: #v6 + v8
			if len(v68) > 0:
				v6l = v68
				for i in v6l:
					# vxx_col_names = ['fN','type','i0','i1','i2','i3','i4', 'i5','i6','i7     , i8',   'i9' 
					#                               (elv,azi,dop ,ran, snr,   sx,  sy,  sz , Associate)
					item = [fn,'v6'] + list(i)
					writer.writerow(item)
		
		if v7 is not None:
			if len(v7) > 0:
				v7l = v7
				for i in v7l:
					#
					#vxx_col_names = ['fN','type','i0','i1','i2','i3','i4', 'i5','i6','i7','i8','i9','i10','i11'    
					#							  (tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ ,'g' ,  'c'            
					#  								0   1     2    3   4   5     6    7     9   10    11    12        
					#  
					item = [fn,'v7'] + list( tuple(i[:10]) + (i[-2],i[-1])) 
					writer.writerow(item)
		 
		


