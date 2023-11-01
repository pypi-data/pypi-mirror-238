# Obstacle Detection Sensing
# 2023/06/18:  
#  
# hardware: BM-501 
#     
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
# v0.0.1
#===========================================
# output: V17,V89,V10
# 

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
	timeInCPUcycle = 0
	numDetectedObj = 0
	numTLVs = 0
	subframeNumber = 0
	numStaticDetectedObj = 0
	
class ObstacleDS:
	magicWordR =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']  #ori
	magicWord  =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']  #use
	
	
	typeList = [1,7,8,9,10,11] 
	X_CALI_DEGREE = 4.85
	INSTALL_HEIGHT = 0
	V_COMBINE = True
	port = ""
	hdr = header
	r = False
	
	# provide csv file dataframe
	# real-time 
	v1_col_names_rt   = ['fN','type','range','elv','angle','doppler','sx','sy','sz']
	v7_col_names_rt   = ['fN','type','snr','noise']
	v8_col_names_rt   = ['fN','type','X','Y','Z','doppler']
	v9_col_names_rt   = ['fN','type','snr','noise']
	v10_col_names_rt  = ['fN','type','tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ']
	v11_col_names_rt  = ['fN','type','Association']
	v17_col_names_rt =  ['fN','type','range','elv','angle','doppler','sx','sy','sz','snr','noise','Association']
	v89_col_names_rt =  ['fN','type','X','Y','Z','doppler','snr','noise']
	
	vxx_col_names = ['fN','type','i0','i1','i2','i3','i4', 'i5','i6' ,'i7','i8','i9']  
	# read from file for trace point clouds
	fileName = ''
	
	sim_startFN = 0
	sim_stopFN  = 0 
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm  = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port):
		
		self.port = port
		print("\n\n\n(jb)mmWave ODS initial")
		print("(jb)version:v0.1.0")
		print("(jb)For Hardware:BM-501")
		print("(jb)Hardware: BM501")
		print("(jb)Firmware:")
		print("(jb)UART Baud Rate:921600")
		print("(jb)Output: V17,V89 and V10 data:(RAW)\n")
		print('v17: Detected Object(Dynamic Points\t\nv89: Static Detected Object(Static Points)')
		print('v10: Tracked Object\n\n')
		
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	
	def headerShow(self):
		print("\n\n\n******* Header ********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("time in CPU cycles:\t{:d} us".format(self.hdr.timeInCPUcycle))
		print("number of Detected object:\t{:d}".format(self.hdr.numDetectedObj))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("number of staic Detected object:\t%d "%(self.hdr.numStaticDetectedObj))
		print("***End Of Header***\n") 
			

	#for class internal use
	def tlvTypeInfo(self,dtype,count,dShow):
		
		sbyte = 8  #tlvHeader Struct = 8 bytes
		unitByte = 20 
		dataByte = 2
		pString = ""
		nString = "numOfPoints :"
		stateString = "Vx-unit"
		retCnt = count
		nPoint = 0
		
		if dtype == 1:  #chk ok ods
			unitByte = 0  
			dataByte= 16 #point bytes= 16bytes (range(4),angle(4),elv(4),doppler(4))
			pString = "Detected Object (Dynamic Points)"
			stateString = "V1"
			nPoint = count/dataByte
			retCnt = count
		
		elif dtype == 7:  #chk ok ods
			unitByte = 0  #pointUnit= 0
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 4    #pointStruct 4bytes:(snr(2),noise(2))
			pString = "Detected Object (Dynamic Points) Side Info"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V7"
		
		elif dtype == 8: #chk ok ods
			unitByte = 0  
			dataByte= 16 #point bytes= 16bytes (X(4),Y(4),Z(4),doppler(4))
			pString = "Static Detected Object (Static Points)"
			stateString = "V8"
			nPoint = count/dataByte
			retCnt = count
			
		elif dtype == 9: #chk ok ods
			unitByte = 0  #pointUnit= 0
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 4    #pointStruct 4bytes:(snr(2),noise(2))
			pString = "Static Detected Object (Static Points) Side Info"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V9"
			
		elif dtype == 10: #chk ok ods
			unitByte = 0  #pointUnit= 0
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 40    #pointStruct 40bytes:(snr(2),noise(2))
			pString = "Tracked Object List"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V10"
			
		elif dtype == 11: #point to Track Assocition
			unitByte = 0  #pointUnit= 0
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 1    #pointStruct 40bytes:(snr(2),noise(2))
			pString = "Point to Track Assocition"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V11"

		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle' 

		#dShow = True
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}Bytes):  \tv{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))
			print("StateString= {}".format(stateString))  
			print("---------------------")
		
		return unitByte,stateString, sbyte, dataByte,retCnt, int(nPoint)
		
	def list2df(self,dck,l1,l7,l8,l9,l10,l11):
		ll1  = pd.DataFrame(l1,columns=self.v1_col_names_rt)
		ll7  = pd.DataFrame(l7,columns=self.v7_col_names_rt)
		ll8  = pd.DataFrame(l8,columns=self.v8_col_names_rt) 
		ll9  = pd.DataFrame(l9,columns=self.v9_col_names_rt) 
		ll10 = pd.DataFrame(l10,columns=self.v10_col_names_rt) 
		ll11 = pd.DataFrame(l11,columns=self.v11_col_names_rt) 
		 
		return (dck,ll1,ll7,ll8,ll9,ll10,ll11)  
	'''
	v10_col_names_rt  = ['fN','type','tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ']
	v11_col_names_rt  = ['fN','type','Association']
	v17_col_names_rt =  ['fN','type','range','elv','angle','doppler','sx','sy','sz','snr','noise','Association']
	v89_col_names_rt =  ['fN','type','X','Y','Z','doppler','snr','noise']
	'''
	def list2df_(self,dck,l1,l7,l8,l9,l10,l11):
		
		ll17s = [v[:1] +('v17',) + v[2:] + a[2:] + b[2:] for v, a, b in zip(l1, l7, l11)]
		#ll89s = [v + a[2:] for v, a  in zip(l8, l9)]
		ll89s = [v[:1] +('v89',) + v[2:] + a[2:] for v, a  in zip(l8, l9)]
		 
		v17o   = pd.DataFrame(ll17s,columns=self.v17_col_names_rt) 
		v89o  = pd.DataFrame(ll89s,columns=self.v89_col_names_rt) 
		v10o  = pd.DataFrame(l10,columns=self.v10_col_names_rt) 
		 
		return (dck,v17o,v89o,v10o)  

	def x_calibrate(self,x,y):
		return  x + np.array(y) * np.tan(np.deg2rad(self.X_CALI_DEGREE))
		
		
	def v17Combine(self,v1 = None, v7 = None, v11 = None):
		v17 = [(*t1,  *t7) for t1,  t7 in zip(v1, v7)] 
		v17 = [t + (item,) for t, item in zip(v17, v11)]
		return v17
	
	def v89Combine(self,v8 = None, v9 = None):
		return [(*t8, *t9) for t8, t9 in zip(v8, v9)]
		
	def combine(self, dck,v1,v7,v8,v9,v10,v11):
		if self.V_COMBINE:
			v89 = self.v89Combine(v8 = v8, v9 = v9)
			v17 = self.v17Combine(v1 = v1, v7 =v7, v11 =v11)
			return (dck,v17,v89,v10)
		else:
			return (dck,v1,v7,v8,v9,v10,v11)
			
	stateR = 0
	stateF = 0
	def state_machineR(self,byte, magic_word):
		print(f"R:input= {byte} magic_word[{self.stateR}] = {magic_word[self.stateR]}   " ) 
		if byte == magic_word[self.stateR]:
			self.stateR += 1
			if self.stateR == len(magic_word):
				self.stateR = 0  # Reset the state machine
				return True
		else:
			self.stateR = 0  # Reset the state if the byte doesn't match the expected pattern
		return False
	
	def state_machineF(self,byte, magic_word): 
		print(f"B:input= {byte} magic_word[{self.stateF}] = {magic_word[self.stateF]}   " ) 
		if byte == magic_word[self.stateF]:
			self.stateF += 1
			if self.stateF == len(magic_word):
				self.stateF = 0  # Reset the state machine
				return True
		else:
			self.stateF = 0  # Reset the state if the byte doesn't match the expected pattern
		return False
#
# TLV: Type-Length-Value
# read TLV data
# Usuage:
# (dck,v1,v7,v8,v9,v10,v11)  = radar.tlvRead(True,df = 'DataFrame')
# input:
#     disp: True:print message
#	  False: hide printing message
#  
# output:(return parameter)
# (pass_fail,v1,v7,v8,v9,v10,v11)
#  pass_fail: True: Data available    False: Data not available
#  v1: Detected Object(Dynamic Points
#  v7: Detected Object(Dynamic Points) Side Info 
#  v8: Static Detected Object(Static Points) 
#  v9: Static Detected Object(Static Points) Side Info
#  v10: Tracked Object List
#  v11: Point to Track Association 
#
 
	def tlvRead(self,disp,df = None ):
		self.magicWord = self.magicWordR if self.r else self.magicWord
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		escapeCount = 0
		dataBytes = 0
		numOfPoints = 0
		numOfPointsCnt = 0
		tlvCount = 0
		pbyte = 16
		
		v1 = ([])
		v7 = ([])
		v8 = ([])
		v9 = ([])
		v10 = ([])
		v11 = ([])
		
		v17 = ([])
		v89 = ([])
		
		v1df = ([])
		v7df = ([])
		v8df = ([])
		v9df = ([])
		v10df = ([])
		v11df = ([])
		
		v17simo = []
		
		nextState = False
		while True:
			try:
				ch = self.port.read()
			except:
				return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
				
			if lstate == 'idle':
				#print(f"ch = {ch}  magicWord[{idx}]= {self.magicWord[idx]}     state={lstate}")
				
				if ch == self.magicWord[idx]:
					idx += 1
					if idx == 8:
						#print("=================== magic word ==================================")
						idx = 0
						lstate = 'header'
						rangeProfile = b""
						sbuf = b""
						self.escapeCount = 0
				else:
					#print("not: magicWord state:")
					idx = 0
					rangeProfile = b""
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
				
			elif lstate == 'header':
				 
				sbuf += ch
				idx += 1
				escapeCount += 1
				if idx == 36: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					
					try: 
						(self.hdr.version,self.hdr.totalPackLen,
						self.hdr.platform,self.hdr.frameNumber,
						self.hdr.timeInCPUcycle,self.hdr.numDetectedObj,
						self.hdr.numTLVs,self.hdr.subframeNumber,self.hdr.numStaticDetectedObj) = struct.unpack('9I', sbuf)
						self.frameNumber = self.hdr.frameNumber
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					#print("tlvCount:{:}".format(tlvCount))
					if self.hdr.numTLVs == 0:
						return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 64: #44
					idx = 0
					sbuf = b''
					lstate = 'idle'
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						if self.dbg == True:
							print("-------------------------")
							print("(TL)--tlvNum:{:d}: tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in self.typeList or self.tlvLength > 20000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
						
					
						
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					
					if self.dbg == True:
						print("(TL) unitByteCount={}  lstate ={} , bytes(type+len)={} dataBytes= {} lenCount ={} numOfPoint={}".format(unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints))
					#if ttype == 10:
					#	print("--pointCloud:((tlvLength({:d})-pointUnit(20)-tlvStruct(8))/8={:d}".format(self.tlvLength,numOfPoints))
					if self.sm == True:
						print("(TL:tlvCount:{:d})=>({:})".format(tlvCount,lstate))
					
					tlvCount -= 1
					#print("(TL->type:{:})--tlvNum:{:d}: tlvCount({:d})".format(ttype,self.hdr.numTLVs,tlvCount))
					idx = 0  
					sbuf = b""
					numOfPointsCnt = 0
					
					if ttype == 1 and self.tlvLength == 0 and tlvCount != 0:
						if self.dbg == True:
							print("========type=1 lenth = 0 ===========================================")
						idx = 0
						lstate = 'idle'
						
					if self.escapeCount > self.hdr.totalPackLen:
						if self.dbg == True:
							print("(ESC)========type={:} ========self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
						idx = 0
						sbuf = b''
						lstate = 'idle'
					
					
			elif lstate == 'V1' or lstate == 'V8' or lstate == 'V10': #v1 chk ok 
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						#v1:raed
						#v8:XYZD
						if lstate == 'V1' or lstate == 'V8':
							(r,a,e,d) = struct.unpack('4f', sbuf)
							if lstate == 'V8':
								if self.dbg == True:
									print("(V8)=> (npts={:2d}: lenCnt={:4d})(idx:({:4d}) X:{:.4f} Y:{:.4f} Z:{:.4f} d:{:.4f}".format(numOfPoints,lenCount,idx,r,a,e,d))
								if (df == 'DataFrame'):
									v8df.append((self.hdr.frameNumber,'v8',r,a,e + self.INSTALL_HEIGHT,d)) 
								else:
									v8.append((r,a,e + self.INSTALL_HEIGHT,d))
							
							if lstate == 'V1':
								
								sz = r * np.sin(e)
								sx  = r * np.cos(e) * np.sin(a)
								sy  = r * np.cos(e) * np.cos(a)
								 
								
								if self.dbg == True:
									print("(V1)=> (npts={:2d}: lenCnt={:4d})(idx:({:4d}) r:{:.4f} e:{:.4f} a:{:.4f} d:{:.4f}".format(numOfPoints,lenCount,idx,r,e,a,d,sx,sy,sz))
								if (df == 'DataFrame'):
									v1df.append((self.hdr.frameNumber,'v1',r,e,a,d,sx,sy,s + self.INSTALL_HEIGHTz)) 
								else:
									v1.append((r,e,a,d,sx,sy,sz + self.INSTALL_HEIGHT))
						
						if lstate == 'V10':
							(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ) = struct.unpack('I9f', sbuf)
							 
							if self.dbg == True:
								print("(V10)=> (npts={:2d}: lenCnt={:4d})(idx:({:4d}) posX:{:.4f} ...accY:{:.4f} accZ:{:.4f}".format(numOfPoints,lenCount,idx,posX,accY,accZ))
						
							if (df == 'DataFrame'):
								v10df.append((self.hdr.frameNumber,'v10',tid,posX,posY,posZ + self.INSTALL_HEIGHT,velX,velY,velZ,accX,accY,accZ)) 
							else:
								v10.append((tid,posX,posY,posZ + self.INSTALL_HEIGHT ,velX,velY,velZ,accX,accY,accZ))
					
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
						
					except:
						if self.dbg == True:
							print(f"(1-8.1)Improper Type: {lstate}  Value structure found: ")
						
						return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
				
				if idx == lenCount:
					if disp == True:
						print("v1[{:d}]".format(len(v1)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V1:{:d})=>(idle) :true".format(tlvCount))
						
						return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V1:{:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
				
					
			elif lstate == 'V7' : 
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				if (idx%dataBytes == 0):
					
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(snr,noise) = struct.unpack('2H', sbuf)
						if (df == 'DataFrame'):
							v7df.append((self.hdr.frameNumber,'v7',snr,noise))
						else:
							v7.append((snr,noise))
						
						if self.dbg == True:
							print("(V7)=> (npts={:2d}: lenCnt={:4d})(idx:({:4d}) snr:{:.4f} noise:{:.4f}".format(numOfPoints,lenCount,idx,snr,noise))
							
						sbuf = b""
					
					except:
						if self.dbg == True:
							print(f"(7.1)Improper Type {lstate} Value structure found: ")
						
						return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
					
					if tlvCount <= 0: # Back to idle
						if self.sm == True:
							print("({}):tlvCount({:d})) lenCount:{}=>(idle)".format(lstate,tlvCount,lenCount))
						lstate = 'idle'
						return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
					
				if idx == lenCount:
					if disp == True:
						print("v7[len:{:d}]".format(len(v7)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V7:{:d})=>(idle) :true".format(tlvCount))
						
						return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V7:{:d})=>(TL)".format(tlvCount))
							
					
				elif idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					print("(ESC)========type={:} lenth = 0 =============self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
			
			elif lstate == 'V9': #chk ok ods
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				
				if (idx%dataBytes == 0):
					numOfPointsCnt += 1
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(snr,noise) = struct.unpack('2H', sbuf)
						if (df == 'DataFrame'):
							v9df.append((self.hdr.frameNumber,'v9',snr,noise))
						else:
							v9.append((snr,noise))
							
						if self.dbg == True:
							print("(V9)=> (npts={:2d}: nptsCnt= {:2d} lenCnt={:4d})(idx:({:4d}) snr:{:.4f} noise:{:.4f}".format(numOfPoints,numOfPointsCnt,lenCount,idx,snr,noise))
						sbuf = b""
					
					except:
						if self.dbg == True:
							print("(9.1)Improper Type 7 Value structure found: ")
						
						return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
					
				if idx == lenCount:
					if disp == True:
						print("v9[len:{:d}]".format(len(v9)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V9:{:d})=>(idle) :true".format(tlvCount))
						return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V9:{:d})=>(TL)".format(tlvCount))
				
				
				if idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					print("(ESC)========type={:} lenth = 0 =============self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
			
			elif lstate == 'V11':
				idx += 1
				#v11.append(ord(ch))
				
				if (df == 'DataFrame'):
					v11df.append((self.hdr.frameNumber,'v11',ord(ch)))
				else:
					v11.append(ord(ch))
					
				if idx == lenCount:
					if disp == True:
						print(f"(V11) ==> {v11}")
						print("=====V11 End====")
					sbuf = b""
					idx = 0
					lstate = 'idle'
					if self.sm == True:
						print("(V11:{:d})=>(idle)".format(tlvCount))
					
					
					return self.list2df(True,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(True,v1,v7,v8,v9,v10,v11)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					return self.list2df(False,v1df,v7df,v8df,v9df,v10df,v11df) if (df == 'DataFrame') else self.combine(False,v1,v7,v8,v9,v10,v11)
		
					
	#v17_col_names_rt =  ['fN','type','range','elv','angle','doppler','sx','sy','sz','snr','noise','Association']
	#v89_col_names_rt =  ['fN','type','X','Y','Z','doppler','snr','noise']
	def getRecordData(self,frameNum):
		s_fn =  frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v17d = self.v17simo[(self.v17simo.fN ==  s_fn)]
		v17o = v17d.loc[:,['range','elv','angle','doppler','sx','sy','sz','snr','noise','Association','fN']].apply(pd.to_numeric)
		
		v89d = self.v89simo[(self.v89simo.fN == s_fn)]
		v89o = v89d.loc[:,['X','Y','Z','doppler','snr','noise','fN']].apply(pd.to_numeric)
		
		v10d = self.v10simo[(self.v10simo.fN == s_fn)]
		v10o = v10d.loc[:,['tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','fN']].apply(pd.to_numeric)
		
		return(v17o,v89o,v10o)
		

	def readFile(self,fileName):
		#fileName = "pc32021-03-19-10-02-17.csv"  
		#df = pd.read_csv(fileName, error_bad_lines=False, warn_bad_lines=False) 
		self.fileName = fileName 
		df = pd.read_csv(self.fileName)
		
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df.info())
		#print(df.info(memory_usage="deep")) 
		
		self.v89simo = df[df['type'] == 'v89'].drop(['i6', 'i7', 'i8', 'i9'], axis=1).rename(columns={'i0': 'X', 'i1': 'Y', 'i2': 'Z', 'i3': 'doppler', 'i4': 'snr', 'i5': 'noise'})
		#print("======v89simo=========")
		#print(self.v89simo)
		
		self.v17simo = df[df['type'] == 'v17'].rename(columns={'i0': 'range', 'i1': 'elv', 'i2': 'angle', 'i3': 'doppler', 'i4': 'sx', 'i5': 'sy', 'i6': 'sz', 'i7': 'snr', 'i8': 'noise', 'i9': 'Association'})
		#print("======v17simo=========")
		#print(self.v17simo)
		
		#v10_col_names_rt  = ['fN','type','tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ']
		self.v10simo = df[df['type'] == 'v10'].rename(columns={'i0': 'tid', 'i1': 'posX', 'i2': 'posY', 'i3': 'posZ', 'i4': 'velX', 'i5': 'velY', 'i6': 'velZ', 'i7': 'accX', 'i8': 'accY', 'i9': 'accZ'})
		#print("======v10simo=========")
		#print(self.v10simo)
		
		self.sim_startFN = int(df['fN'].values[1])
		self.sim_stopFN  = int(df['fN'].values[-1])
		
		#print(f'self.sim_startFN  = {self.sim_startFN} self.sim_stopFN = {self.sim_stopFN} ')
		
		return (self.sim_startFN,self.sim_stopFN,self.v17simo,self.v89simo,self.v10simo)
	
	
	def recording_ods(self,writer= None,v17=None,v89=None, v10 = None,fn = None):
		if v17 is not None:
			if len(v17) > 0:
				v17l = v17
				for i in v17l: 
					item = [fn,'v17'] + list(i)
					writer.writerow(item)
		
		if v89 is not None:
			if len(v89) > 0:
				v89l = v89
				for i in v89l: 
					item = [fn,'v89'] + list(i)
					writer.writerow(item)
		 
		if v10 is not None:
			if len(v10) > 0:
				v10l = v10
				for i in v10l: 
					item = [fn,'v10'] + list(i)
					writer.writerow(item)


