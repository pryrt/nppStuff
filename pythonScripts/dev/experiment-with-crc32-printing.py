from Npp import *
import zlib

console.show()
console.clear()
for (filename, bufferID, index, view) in notepad.getFiles():
	crc = zlib.crc32(filename)
	console.write( '{:010X} {:010X} "{}"\n'.format( crc, crc & 0xFFFFFFFF , filename ) )

for crc in (-1234567891, -987654321, 1234567891, 987654321):
    console.write( '{:010X} {:010X} "{}"\n'.format( crc, crc & 0xFFFFFFFF , crc ) )
