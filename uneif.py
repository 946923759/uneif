#!/usr/bin/env python3.10
import sys
import struct
from hashlib import md5

def writeImage(data:bytes,fileName:str):
	print("Writing out "+fileName)
	with open(fileName,'wb') as f:
		f.write(data)

with open(sys.argv[1], 'rb') as f:
	insidePNG = False
	pngData:bytes = b''

	while True:
	
		while f.peek(1)[:4] != b'\x89\x50\x4E\x47':
			tmp = f.read(1)
			if not tmp:
				print("no more data")
				sys.exit(0)
		print("Found PNG!")
		pngHeader = f.read(8)
		print(pngHeader)
		pngData=pngHeader

		#sys.exit(0)
		while True:
			chunkLenBytes = f.read(4)
			chunkLen = struct.unpack('>I',chunkLenBytes)[0]
			pngData+=chunkLenBytes
			pngData+=f.read(4) #Chunk type, we don't need this
			pngData+=f.read(chunkLen)
			pngData+=f.read(4) #CRC, we don't need this

			if chunkLen==0:
				writeImage(pngData,md5(pngData).hexdigest()+".png")
				print("Hit end of PNG")
				#sys.exit(0)
				break

		

			# if insidePNG:
			# 	bytes2=f.read(4)
			# 	if bytes2==b'IEND':
			# 		pngData+= bytes2 + f.read(4)
			# 		writeImage(pngData,md5(pngData).hexdigest()+".png")
			# 		insidePNG=False
			# 		sys.exit(0)
			# 	elif bytes2 == b'\x89\x50\x4E\x47':
			# 		print("Found beginning of new PNG? Missing end chunk?")
			# 		writeImage(pngData,md5(pngData).hexdigest()+".png")
			# 		pngData=bytes2
			# 	else:
			# 		pngData += f.read(4)