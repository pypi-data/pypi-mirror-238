import os as os2, time, string, sys, platform, binascii, codecs, base64

class OS:
	def GetOSInfo():
		print(f"OS Device Identifier : {os2.name}")
		print(f"OS : {platform.system()}")
	def ClearScreen():
		if os2.name.lower() == "nt":
			os2.system("cls")
		else:
			os2.system("clear")
class ANSI:
	def ListColors():
		for color in range(256):
			print(f"\033[38;5;{color}m{color}\033[0m ", end='')
	def ColoredOutput(color, text=""):
		print(f"\033[38;5;{color}m{text}")
	def ResetColors():
		print("\033[0m")
class Message:
	def Error(errtext="Unspecified Error"):
		print(f"\033[0;37m[\033[1;31mX\033[0;37m] \033[1;31m{errtext}\033[0m")
	def Warn(warntext="Unspecified Warning"):
		print(f"\033[0;37m[\033[1;33m!\033[0;37m] \033[1;33m{warntext}\033[0m")
	def Info(infotext="Unspecified Information"):
		print(f"\033[0;37m[\033[1;34mi\033[0;37m] \033[1;34m{infotext}\033[0m")
class Encoding:
	class b16:
		def encode16(txtinput):
			output = base64.b16encode(bytes(txtinput, 'utf-8')).decode('utf-8')
			return output
		def decode16(b16input):
			output = base64.b16decode(bytes(b16input, 'utf-8')).decode('utf-8')
			return output
	class b32:
		def encode32(txtinput):
			output = base64.b32encode(bytes(txtinput, 'utf-8')).decode('utf-8')
			return output
		def decode32(b32input):
			output = base64.b32decode(bytes(b32input, 'utf-8')).decode('utf-8')
			return output
	class b64:
		def encode64(txtinput):
			output = base64.b64encode(bytes(txtinput, 'utf-8')).decode('utf-8')
			return output
		def decode64(b64input):
			output = base64.b64decode(bytes(b64input, 'utf-8')).decode('utf-8')
			return output
	class hex:
		def encodeHex(txtinput):
			output = binascii.hexlify(bytes(txtinput, 'utf-8')).decode('utf-8')
			return output
		def decodeHex(hexinput):
			output = binascii.unhexlify(bytes(hexinput, 'utf-8')).decode('utf-8')
			return output
	class binary:
		def encodeBin(txtinput):
			output = ''.join(format(i, '08b') for i in bytearray(txtinput, encoding ='utf-8'))
			return output
		def decodeBin(bininput):
			integer = integer = int(bininput, base=2)
			output = integer.to_bytes((integer.bit_length() + 7)//8, 'big').decode()
			return output


functionInfo = []

class Debugging:
	def endedIn(func):
		def wrapper(*args, **kwargs):
			s_time = time.perf_counter()
			result = func(*args, **kwargs)
			e_time = time.perf_counter()
			f_time = round(e_time - s_time, 8)
			print(f"[function %s finished in %.8f; exit code %s]" % (func.__name__, f_time, result))
			return result
		return wrapper
	
	def fullInfo(func):
		global functionInfo
		info = {"name": func.__name__, "running": "No", "FPID": "None"}
		functionInfo.append(info)
		infoIndex = functionInfo.index(info)
		def wrapper(*args, **kwargs):
			info = {"name": func.__name__, "running": "Yes", "FPID": infoIndex}
			functionInfo[infoIndex] = info
			exitcode = func(*args, **kwargs)
			info = {"name": func.__name__, "running": f"Exited (return code {exitcode})", "FPID": "None"}
			functionInfo[infoIndex] = info
			return exitcode
		return wrapper
	def GetFunctionInfo(functionName, raiseException=True):
		global functionInfo
		found = False
		for info in functionInfo:
			if info.get('name') == functionName:
				found = True
				fname = info.get('name')
				frunning = info.get('running')
				break
			else:
				continue
		if not found and raiseException:
			err = "Function %s not found: did you forget the @fastpython.Debugging.fullInfo decorator? Set \"raiseException\" to False when calling this function to disable this error." % functionName
			raise FPYErrors.FunctionNotFoundByName(err)
		elif found:
			print("Function Name: %s" % fname)
			print("Is Running   : %s" % frunning)
class FPYErrors:
	class FunctionNotFoundByName(Exception):
		pass
			





if __name__=="__main__":
	print("Ooops, you ran the wrong file.\n\nCreate a new file and import this one to use it. It will not work here.")
	sys.exit(1)
