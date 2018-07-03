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


"""
Disassembly from KingMike at RHDN

 $00/9429 A0 FC 03    LDY #$03FC              A:0070 X:616E Y:0000
 $00/942C A6 1F       LDX $1F    [$00:001F]   A:0070 X:616E Y:03FC
 $00/942E A9 02 65    LDA #$6502              A:0070 X:0000 Y:03FC
 $00/9431 18          CLC                     A:6502 X:0000 Y:03FC
 $00/9432 7D 08 00    ADC $0008,x[$70:0008]   A:6502 X:0000 Y:03FC
 $00/9435 E8          INX                     A:4AE7 X:0000 Y:03FC
 $00/9436 E8          INX                     A:4AE7 X:0001 Y:03FC
 $00/9437 88          DEY                     A:4AE7 X:0002 Y:03FC
 $00/9438 D0 F7       BNE $F7    [$9431]      A:4AE7 X:0002 Y:03FB
 $00/943A AA          TAX                     A:592C X:07F8 Y:0000
 $00/943B 7A          PLY                     A:592C X:592C Y:0000
 $00/943C AB          PLB                     A:592C X:592C Y:0000
 $00/943D 28          PLP                     A:592C X:592C Y:0000
 $00/943E 60          RTS                     A:592C X:592C Y:0000

"""
