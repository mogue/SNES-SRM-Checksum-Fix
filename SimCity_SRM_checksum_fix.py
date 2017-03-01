"""
	Fix hacked Sim City SRM files
	2015, by m06

	Usage: python SimCity_SRM_checksum_fix.py /path/to/save_file.srm

"""

print "\n\tSim City SRM checksum fix\n"

from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python SimCity_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for i in range(2):
	f.seek(16 + (i*16368))
	checksum = 0
        for b in f.read(16368):
            checksum += unpack('i', b + '\x00\x00\x00')[0]
        f.seek(10 + (i*2))
        f.write( pack('B', checksum & 0xFF) )
        f.write( pack('B', (checksum >> 8) & 0xFF) )
        f.seek(32752 + 10 + (i*2))
        f.write( pack('B', checksum & 0xFF) )
        f.write( pack('B', (checksum >> 8) & 0xFF) )

        print "Checksum for save slot " + str(i+1) + ": " + str(checksum)

    checksum = 0
    f.seek(0)
    for b in f.read(14):
        checksum += unpack('i', b + '\x00\x00\x00')[0]
    f.seek(14)
    f.write( pack('B', checksum & 0xFF) )
    f.write( pack('B', (checksum >> 8) & 0xFF) )
    f.seek(32752 + 14)
    f.write( pack('B', checksum & 0xFF) )
    f.write( pack('B', (checksum >> 8) & 0xFF) )
    print "Checksum for Header: " + str(checksum)


print"Done!"
