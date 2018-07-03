"""
	Fix hacked Secret of Mana SRM files
	2017, by m06

	Usage: python SoM_SRM_checksum_fix.py /path/to/save_file.srm

	Secret of Mana duplicates all data in the first 1kb of the file in the second half of the 2kb SRM file.
	Using this script you will only need to edit the first half and the second will be duplicated for you.
"""

print "\n\tSecret of Mana SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python SoM_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek( 3 + (slot * 0x400) )
	checksum = 0
	data = array.array("B")
        data.fromfile(f, 0x2B8)
        for byte in data:
            checksum += byte
	checksum &= 0xFFFF

        f.seek( 1 + (slot * 0x400) )
	f.write( pack('H', checksum ) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

    f.seek(0)
    chk = array.array("B")
    chk.fromfile(f, 0xFFE)
    f.seek(0x1000)
    f.write( chk )
    print "Duplicated 1kb to the second half of file."

print"Done!"

"""
Disassembly by me:

c75cdc phx           ; Push X         
c75cdd rep #$20      ; 16-bit Accumulator         
c75cdf lda #$02b8    ; Save file size
c75ce2 sta $a171     ; Store it
c75ce5 stz $a173     ; Reset checksum
c75ce8 lda $306003,x ; Load word 
c75cec and #$00ff    ; Filter byte
c75cef clc           ; Clear carry    
c75cf0 adc $a173     ; Add to checksum
c75cf3 sta $a173     ; Store checksum
c75cf6 inx           ; Next byte         
c75cf7 dec $a171     ; Decrement size
c75cfa bne $5ce8     ; Loop
"""
