"""
	Fix hacked FFIV SRM files
	2017, by m06

	Usage: python FF4_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tFinal Fantasy IV SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python FF4_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek( slot * 0x800 )
	checksum = 0
	data = array.array("B")
        data.fromfile(f, 0x7FA)
        lastbyte = None
        for byte in data:
            if  lastbyte is None:
		lastbyte = byte
		continue
            word = (byte << 8) + lastbyte
            checksum += word
            lastbyte = byte
            if  checksum > 0xFFFF: # CARRY
		checksum = checksum & 0xFFFF
		checksum += 1
        f.seek( ( (slot+1) * 0x800) - 4 )
	f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"
