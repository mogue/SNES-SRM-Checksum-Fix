"""
	Fix hacked Secret of Evermore SRM files
	2015, by m06

	Usage: python SoE_SRM_checksum_fix.py /path/to/save_file.srm

"""

print "\n\tSecret of Evermore SRM checksum fix\n"

from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python SoE_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek(4 + (slot * 0x331))
	checksum = 0x43F
	temp = checksum + unpack('B', f.read(1))[0]
        for b in f.read(0x32E):
	    temp &= 0xFF
            checksum &= 0xFF00
	    checksum |= temp
            checksum <<= 1
            if  checksum > 0xFFFF: # Carry
                checksum -= 0xFFFF
            temp = checksum + unpack('B', b)[0]

        f.seek( 2 + (slot * 0x331) )
        f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"
