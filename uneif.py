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



# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org/>