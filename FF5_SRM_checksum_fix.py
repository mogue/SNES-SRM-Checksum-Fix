"""
	Fix hacked FFV SRM files
	2017, by m06

	Usage: python FF5_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tFinal Fantasy V SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python FF5_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek( slot * 0x700 )
	checksum = 0
	data = array.array("H")
        data.fromfile(f, 0x300)
        for word in data:
            checksum += word
            if  checksum > 0xFFFF: # CARRY
		checksum = checksum & 0xFFFF
		checksum += 1
        f.seek( 0x1FF0 + (slot * 2) )
	f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"
