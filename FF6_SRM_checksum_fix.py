"""
	Fix hacked FFVIj/FFIIIus SRM files
	2013, by m06

	Usage: python FF6_SRM_fix.py /path/to/save_file.srm

"""

print "\n\tFinal Fantasy VI SRM checksum fix\n"

from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python FF6_SRM_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for i in range(3):
	checksum = 0
        for b in f.read(0x9FE):
            checksum += unpack('i', b + '\x00\x00\x00')[0]
        f.seek(0x9FE + (i*0xA00))
        f.write( pack('B', checksum & 0xFF) )
        f.write( pack('B', (checksum >> 8) & 0xFF) )

        print "Checksum for save slot " + str(i+1) + ": " + str(checksum)

print"Done!

""""






""""
