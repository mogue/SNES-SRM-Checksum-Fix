"""
	Fix hacked Lufia & The Fortress of Doom SRM files
	2017, by m06

	Usage: python Lufia_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tLufia & The Fortress of Doom SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python Lufia_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(3):
	f.seek( 8 + (slot * 0x800) )
	checksum = 0x6502
	data = array.array("H")
        data.fromfile(f, 0x3FC)
        for word in data:
            checksum += word
            if  checksum > 0xFFFF: # CARRY
		checksum &= 0xFFFF
        f.seek( 6 + (slot * 0x800) )
	f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"
